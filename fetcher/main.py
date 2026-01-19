from camara.resources.deputado import DeputadoResource
from camara.db.session import SessionLocal

if __name__ == "__main__":
    resource = DeputadoResource("0 0 * * *")
    response = resource.fetch()
    data = resource.parse(response)
    resource.save(SessionLocal(), data)

