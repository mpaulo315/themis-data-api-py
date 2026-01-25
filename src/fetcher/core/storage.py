from typing import Any, Iterable, Literal, TypeVar, TypedDict, Union
from sqlalchemy import Enum, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from sqlmodel import SQLModel


class WhereClause(TypedDict):
    column: str
    value: Any
    comparison: Literal[">", "<", "=", "!=", ">=", "<="]


class UpdateStrategy(str, Enum):
    UPSERT = "upsert"
    FULL_REPLACE = "full_replace"
    PARTIAL_REPLACE = "partial_replace"


T = TypeVar("T", bound=SQLModel)


class DatabaseStorage:
    CHUNK_SIZE = 2

    @classmethod
    def apply_strategy(
        cls,
        strategy: UpdateStrategy,
        session: Session,
        model: type[SQLModel],
        items: Iterable[T],
        index_elements: list[str] = ["id"],
        where_clause: WhereClause | None = None,
    ):

        match strategy:
            case UpdateStrategy.UPSERT:
                cls.smart_bulk_upsert(session, model, items, index_elements)
            case UpdateStrategy.FULL_REPLACE:
                cls.delete(session, model)
                cls.smart_bulk_insert(session, items)
            case UpdateStrategy.PARTIAL_REPLACE:
                if not where_clause:
                    raise ValueError(
                        "Where clause is required for partial replace strategy"
                    )

                cls.delete(session, model, where_clause)
                cls.smart_bulk_insert(session, items)

    @classmethod
    def bulk_insert(cls, session: Session, model: type[SQLModel], items: Iterable[T]):
        try:
            for i in range(0, len(items), cls.CHUNK_SIZE):
                payload = items[i : i + cls.CHUNK_SIZE]
                session.add_all(payload)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def smart_bulk_insert(cls, session: Session, items: Iterable[T]):
        for i in range(0, len(items), cls.CHUNK_SIZE):
            batch = items[i : i + cls.CHUNK_SIZE]

            try:
                session.add_all(batch)
                session.commit()
            except Exception as e:
                session.rollback()

                for item in batch:
                    try:
                        session.add(item)
                        session.commit()
                    except Exception as e:
                        session.rollback()

                        raise e

    @classmethod
    def smart_bulk_upsert(
        cls,
        session: Session,
        model: type[SQLModel],
        items: Iterable[T],
        index_elements: list[str],
    ):
        for e in index_elements:
            if not isinstance(e, str):
                raise ValueError("Index elements must be strings")
            if not hasattr(model, e):
                raise ValueError(f"Model {model.__name__} does not have attribute {e}")

        for i in range(0, len(items), cls.CHUNK_SIZE):
            batch = items[i : i + cls.CHUNK_SIZE]

            try:
                stmt = insert(model).values(batch)
                stmt.on_conflict_do_update(index_elements=index_elements, set_=batch)

                session.execute(stmt)
                session.commit()
            except Exception as e:
                session.rollback()

                for item in batch:
                    try:
                        session.add(item)
                        session.commit()
                    except Exception as e:
                        session.rollback()

                        raise e

    @classmethod
    def delete(
        cls,
        session: Session,
        model: type[SQLModel],
        where_clause: WhereClause | None = None,
    ):
        table = model.__table__

        stmt = delete(table)

        if where_clause:
            match where_clause["comparison"]:
                case ">":
                    stmt = stmt.where(
                        table.c[where_clause["column"]] > where_clause["value"]
                    )
                case "<":
                    stmt = stmt.where(
                        table.c[where_clause["column"]] < where_clause["value"]
                    )
                case "=":
                    stmt = stmt.where(
                        table.c[where_clause["column"]] == where_clause["value"]
                    )
                case "!=":
                    stmt = stmt.where(
                        table.c[where_clause["column"]] != where_clause["value"]
                    )
                case ">=":
                    stmt = stmt.where(
                        table.c[where_clause["column"]] >= where_clause["value"]
                    )
                case "<=":
                    stmt = stmt.where(
                        table.c[where_clause["column"]] <= where_clause["value"]
                    )

        session.execute(stmt)
        session.commit()
