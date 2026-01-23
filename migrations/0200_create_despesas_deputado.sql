CREATE TABLE IF NOT EXISTS despesas_deputado (
    id SERIAL PRIMARY KEY,

    "idDocumento" INT,
    "nomeParlamentar" VARCHAR(255) NOT NULL,
    mes INT NOT NULL,
    ano INT NOT NULL,
    "codigoLegislatura" INT NOT NULL,
    "siglaUF" VARCHAR(2),
    "siglaPartido" VARCHAR(2),
    fornecedor VARCHAR(255) NOT NULL,
    "idDeputado" INT,

    descricao VARCHAR(255) NOT NULL,
    "dataEmissao" DATE,
    "valorDocumento" FLOAT NOT NULL,
    "valorGlosa" FLOAT,
    "valorLiquido" FLOAT,
    restituicao FLOAT,

    "datPagamentoRestituicao" DATE,
    "tipoDocumento" INT NOT NULL,
    "urlDocumento" VARCHAR(255),
    passageiro VARCHAR(255),
    trecho VARCHAR(255)
);


DROP TABLE IF EXISTS despesas_deputado;
