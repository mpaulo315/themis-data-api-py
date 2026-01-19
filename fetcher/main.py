from camara.resources.legislatura import LegislaturaResource
from camara.db.session import SessionLocal

if __name__ == "__main__":
    resource = LegislaturaResource("0 0 * * *")
    response = resource.fetch()
    data = resource.transform(response)
    resource.save(SessionLocal(), data)

