CREATE TABLE IF NOT EXISTS despesas_deputado (
    id SERIAL PRIMARY KEY,
    "idDocumento" INT NOT NULL,
    mes INT NOT NULL,
    ano INT NOT NULL,
    "codigoLegislatura" INT NOT NULL,

    "nomeParlamentar" VARCHAR(255),
    "idDeputado" INT,

    descricao VARCHAR(255) NOT NULL,
    fornecedor VARCHAR(255) NOT NULL,
    "dataEmissao" DATE NOT NULL,
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
