CREATE TABLE IF NOT EXISTS deputados (
    id SERIAL PRIMARY KEY,
    uri VARCHAR(255) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    "nomeCivil" VARCHAR(255) NOT NULL,
    "siglaSexo" CHAR(1) NOT NULL,
    "idLegislaturaInicial" INT NOT NULL,
    "idLegislaturaFinal" INT NOT NULL,
    "ufNascimento" CHAR(2),
    "municipioNascimento" VARCHAR(255),
    "dataNascimento" DATE,
    "dataFalecimento" DATE
);

DROP TABLE IF EXISTS deputados;
