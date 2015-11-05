DROP TABLE IF EXISTS tramitacao;
CREATE TABLE IF NOT EXISTS tramitacao (
  id serial NOT NULL,
  id_proposicao integer NOT NULL,
  data date NOT NULL,
  CONSTRAINT tramitacao_pkey PRIMARY KEY (id)
);

DROP TABLE IF EXISTS importacao_proposicao;
CREATE TABLE IF NOT EXISTS importacao_proposicao (
  id_proposicao integer NOT NULL,
  desatualizada boolean NOT NULL,
  CONSTRAINT importacao_proposicao_pkey PRIMARY KEY (id_proposicao)
);

DROP TABLE IF EXISTS autor;
CREATE TABLE IF NOT EXISTS autor (
  id serial NOT NULL,
  nome VARCHAR(1000) NULL,
  partido VARCHAR(45)  NULL,
  uf VARCHAR(4) NULL,
  CONSTRAINT autor_pkey PRIMARY KEY (id)
);

DROP TABLE IF EXISTS tipo_proposicao;
CREATE TABLE IF NOT EXISTS tipo_proposicao (
  id serial NOT NULL,
  sigla VARCHAR(45) NULL,
  descricao VARCHAR(600) NULL,
  CONSTRAINT tipo_proposicao_pkey PRIMARY KEY (id)
);

DROP TABLE IF EXISTS situacao;
CREATE TABLE IF NOT EXISTS situacao (
  id serial NOT NULL,
  descricao VARCHAR(300) NULL,
  CONSTRAINT situacao_pkey PRIMARY KEY (id)
);

DROP TABLE IF EXISTS proposicao;
CREATE TABLE IF NOT EXISTS proposicao (
  id integer NOT NULL,
  nome character varying(100),
  numero integer,
  ano integer,
  data_apresentacao date,
  data_ultimo_despacho date,
  ementa text,
  explicacao_ementa text,
  indexacao text,
  link_teor character varying(100),
  id_autor_principal integer,  
  id_tipo_proposicao integer,
  id_situacao integer,
  CONSTRAINT proposicao_pkey PRIMARY KEY (id),
  CONSTRAINT fk_proposicao_tipo_proposicao FOREIGN KEY (id_tipo_proposicao) REFERENCES tipo_proposicao (id),
  CONSTRAINT fk_proposicao_autor FOREIGN KEY (id_autor_principal) REFERENCES autor (id),
  CONSTRAINT fk_proposicao_situacao FOREIGN KEY (id_situacao) REFERENCES situacao (id)
);

DROP TABLE IF EXISTS tema;
CREATE TABLE IF NOT EXISTS tema (
  id serial NOT NULL,
  descricao character varying(100) NOT NULL,
  CONSTRAINT tema_pkey PRIMARY KEY (id)
);

DROP TABLE IF EXISTS tema_proposicao;
CREATE TABLE IF NOT EXISTS tema_proposicao (
  id_tema integer NOT NULL,
  id_proposicao integer NOT NULL,
  CONSTRAINT tema_proposicao_pkey PRIMARY KEY (id_tema, id_proposicao),
  CONSTRAINT fk_tema_proposicao_tema FOREIGN KEY (id_tema) REFERENCES tema (id),
  CONSTRAINT fk_tema_proposicao_proposicao FOREIGN KEY (id_proposicao) REFERENCES proposicao (id)
);