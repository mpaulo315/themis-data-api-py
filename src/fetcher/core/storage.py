from typing import Any, Iterable, Literal, TypeVar, TypedDict, Union
from sqlalchemy import Enum, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from sqlmodel import SQLModel
from tqdm import tqdm, trange


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
    CHUNK_SIZE = 2000

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
        for i in trange(
            0, len(items), cls.CHUNK_SIZE, desc="Inserting chunks", position=0
        ):
            batch = items[i : i + cls.CHUNK_SIZE]

            try:
                session.add_all(batch)
                session.commit()
            except Exception as e:
                session.rollback()

                for item in tqdm(
                    items, desc="Inserting items", position=1, leave=False
                ):
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
        table = model.__table__

        for col in index_elements:
            if col not in table.c:
                raise ValueError(f"Column '{col}' not found in {model.__name__}")

        for i in trange(0, len(items), cls.CHUNK_SIZE, desc="Upserting chunks"):
            batch = items[i : i + cls.CHUNK_SIZE]
            values = [item.model_dump(exclude_unset=True) for item in batch]

            stmt = insert(table).values(values)

            stmt = stmt.on_conflict_do_update(
                index_elements=index_elements,
                set_={
                    c.name: getattr(stmt.excluded, c.name)
                    for c in table.columns
                    if c.name not in index_elements
                },
            )

            try:
                session.execute(stmt)
                session.commit()

            except Exception as bulk_exc:
                session.rollback()

                for item in batch:
                    row = item.model_dump(exclude_unset=True)

                    stmt = insert(table).values(row)
                    stmt = stmt.on_conflict_do_update(
                        index_elements=index_elements,
                        set_={
                            c.name: getattr(stmt.excluded, c.name)
                            for c in table.columns
                            if c.name not in index_elements
                        },
                    )

                    try:
                        session.execute(stmt)
                        session.commit()

                    except Exception as row_exc:
                        session.rollback()

                        raise RuntimeError(f"Failed upsert for row: {row}") from row_exc

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
