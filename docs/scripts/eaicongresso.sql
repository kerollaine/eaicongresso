DROP TABLE IF EXISTS tipo_proposicao;
CREATE TABLE IF NOT EXISTS tipo_proposicao (
  id serial NOT NULL,
  sigla VARCHAR(45) NULL,
  descricao VARCHAR(45) NULL,
  ativa BOOL NULL,
  genero VARCHAR(45) NULL,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS orgao_numerador;
CREATE TABLE IF NOT EXISTS orgao_numerador (
  id serial NOT NULL,
  sigla VARCHAR(45) NULL,
  nome VARCHAR(45) NULL,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS regime;
CREATE TABLE IF NOT EXISTS regime (
  id serial NOT NULL,
  descricao VARCHAR(45) NULL,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS apreciacao;
CREATE TABLE IF NOT EXISTS apreciacao (
  id serial NOT NULL,
  descricao VARCHAR(45) NULL,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS partido;
CREATE TABLE IF NOT EXISTS partido (
  id serial NOT NULL,
  sigla VARCHAR(45) NULL,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS tipo_autor ;
CREATE TABLE IF NOT EXISTS tipo_autor (
  id serial NOT NULL,
  descricao VARCHAR(45) NULL,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS autor;
CREATE TABLE IF NOT EXISTS autor (
  id serial NOT NULL,
  nome VARCHAR(45) NULL,
  id_partido INT NULL,
  uf VARCHAR(45) NULL,
  id_tipo_autor INT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_autor_partido FOREIGN KEY (id_partido) REFERENCES partido (id),
  CONSTRAINT fk_autor_tipo_autor FOREIGN KEY (id_tipo_autor) REFERENCES tipo_autor (id)
);

DROP TABLE IF EXISTS orgao;
CREATE TABLE IF NOT EXISTS orgao (
  id serial NOT NULL,
  sigla VARCHAR(45) NULL,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS situacao;
CREATE TABLE IF NOT EXISTS situacao (
  id serial NOT NULL,
  descricao VARCHAR(45) NULL,
  id_orgao INT NULL,
  ativa BOOL NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_situacao_orgao FOREIGN KEY (id_orgao) REFERENCES orgao (id)
);

DROP TABLE IF EXISTS proposicao;
CREATE TABLE IF NOT EXISTS proposicao (
  id serial NOT NULL,
  nome VARCHAR(45) NULL,
  id_tipo_proposicao INT NULL,
  numero INT NULL,
  ano INT NULL,
  id_orgao_numerador INT NULL,
  data_apresentacao DATE NULL,
  ementa TEXT NULL,
  explicacao_ementa TEXT NULL,
  id_regime INT NULL,
  id_apreciacao INT NULL,
  qtde_autores INT NULL,
  id_autor_principal INT NULL,
  id_situacao INT NULL,
  indexacao INT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_proposicao_tipo_proposicao FOREIGN KEY (id_tipo_proposicao) REFERENCES tipo_proposicao (id),
  CONSTRAINT fk_proposicao_orgao_numerador FOREIGN KEY (id_orgao_numerador) REFERENCES orgao_numerador (id),
  CONSTRAINT fk_proposicao_regime FOREIGN KEY (id_regime) REFERENCES regime (id),
  CONSTRAINT fk_proposicao_apreciacao FOREIGN KEY (id_apreciacao) REFERENCES apreciacao (id),
  CONSTRAINT fk_proposicao_autor FOREIGN KEY (id_autor_principal) REFERENCES autor (id),
  CONSTRAINT fk_proposicao_situacao FOREIGN KEY (id_situacao) REFERENCES situacao (id)
);

DROP TABLE IF EXISTS indexacao;
CREATE TABLE IF NOT EXISTS indexacao (
  id serial NOT NULL,
  palavra VARCHAR(45) NULL,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS proposicao_indexacao;
CREATE TABLE IF NOT EXISTS proposicao_indexacao (
  id_proposicao INT NOT NULL,
  id_indexacao INT NOT NULL,
  PRIMARY KEY (id_proposicao, id_indexacao),
  CONSTRAINT fk_proposicao_indexacao_proposicao FOREIGN KEY (id_proposicao) REFERENCES proposicao (id),
  CONSTRAINT fk_proposicao_indexacao_indexacao FOREIGN KEY (id_indexacao) REFERENCES indexacao (id)
);

DROP TABLE IF EXISTS votacao;
CREATE TABLE IF NOT EXISTS votacao (
  id serial NOT NULL,
  id_proposicao INT NULL,
  relevancia BOOL NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_votacao_proposicao FOREIGN KEY (id_proposicao) REFERENCES proposicao (id)
);

DROP TABLE IF EXISTS tramitacao;
CREATE TABLE IF NOT EXISTS tramitacao (
  id serial NOT NULL
  id_proposicao integer NOT NULL,
  data date NOT NULL,
).