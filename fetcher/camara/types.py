class CamaraAPIResponse[T]:
    dados: T
    links: dict[str, str]