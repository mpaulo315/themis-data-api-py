from camara.resources.despesas import DespesasResource
from camara.db.session import SessionLocal

if __name__ == "__main__":
    resource = DespesasResource("0 0 * * *")
    response = resource.fetch()
    data = resource.transform(response)
    resource.save(SessionLocal(), data)

