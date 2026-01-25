CREATE TABLE IF NOT EXISTS legislaturas (
    id SERIAL PRIMARY KEY,
    uri VARCHAR(255) NOT NULL,
    dataInicio DATE NOT NULL,
    dataFim DATE NOT NULL,
    anoEleicao INT NOT NULL
)

DROP TABLE IF EXISTS legislaturas;
