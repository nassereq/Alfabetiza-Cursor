-- Dimensões relacionais (padrão disciplina Banco de dados relacionais / MySQL)
-- Usar com MySQL + DBeaver; popular a partir de data/sample/*.csv ou Base dos Dados.

CREATE DATABASE IF NOT EXISTS alfabetiza
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE alfabetiza;

CREATE TABLE IF NOT EXISTS dim_uf (
  id_uf        CHAR(2)      NOT NULL,
  sigla_uf     CHAR(2)      NOT NULL,
  nome_uf      VARCHAR(60)  NOT NULL,
  PRIMARY KEY (id_uf),
  UNIQUE KEY uk_sigla (sigla_uf)
);

CREATE TABLE IF NOT EXISTS dim_municipio (
  id_municipio VARCHAR(7)   NOT NULL,
  id_uf        CHAR(2)      NOT NULL,
  sigla_uf     CHAR(2)      NOT NULL,
  nome_municipio VARCHAR(120) NOT NULL,
  PRIMARY KEY (id_municipio),
  KEY ix_mun_uf (id_uf),
  CONSTRAINT fk_mun_uf FOREIGN KEY (id_uf) REFERENCES dim_uf (id_uf)
);

CREATE TABLE IF NOT EXISTS fato_meta_brasil (
  ano          INT          NOT NULL,
  meta_pct     DECIMAL(5,2) NOT NULL,
  ponto_corte  INT          NOT NULL DEFAULT 743,
  PRIMARY KEY (ano)
);

CREATE TABLE IF NOT EXISTS fato_meta_uf (
  ano          INT          NOT NULL,
  id_uf        CHAR(2)      NOT NULL,
  sigla_uf     CHAR(2)      NOT NULL,
  meta_pct     DECIMAL(5,2) NOT NULL,
  PRIMARY KEY (ano, id_uf),
  CONSTRAINT fk_meta_uf FOREIGN KEY (id_uf) REFERENCES dim_uf (id_uf)
);

CREATE TABLE IF NOT EXISTS fato_meta_municipio (
  ano          INT          NOT NULL,
  id_municipio VARCHAR(7)   NOT NULL,
  id_uf        CHAR(2)      NOT NULL,
  meta_pct     DECIMAL(5,2) NOT NULL,
  PRIMARY KEY (ano, id_municipio),
  CONSTRAINT fk_meta_mun FOREIGN KEY (id_municipio) REFERENCES dim_municipio (id_municipio)
);

CREATE TABLE IF NOT EXISTS fato_indicador_municipio (
  ano               INT          NOT NULL,
  id_municipio      VARCHAR(7)   NOT NULL,
  id_uf             CHAR(2)      NOT NULL,
  pct_alfabetizados DECIMAL(5,2) NOT NULL,
  ponto_corte       INT          NOT NULL DEFAULT 743,
  n_avaliados       INT          NULL,
  PRIMARY KEY (ano, id_municipio),
  CONSTRAINT fk_ind_mun FOREIGN KEY (id_municipio) REFERENCES dim_municipio (id_municipio)
);

-- Exemplo de view analítica (prévia da Gold)
CREATE OR REPLACE VIEW vw_meta_vs_resultado_municipio AS
SELECT
  i.ano,
  i.id_municipio,
  m.nome_municipio,
  i.sigla_uf,
  i.pct_alfabetizados,
  mt.meta_pct,
  (i.pct_alfabetizados - mt.meta_pct) AS gap_meta_pct,
  CASE WHEN i.pct_alfabetizados >= mt.meta_pct THEN 1 ELSE 0 END AS atingiu_meta
FROM fato_indicador_municipio i
JOIN dim_municipio m ON m.id_municipio = i.id_municipio
LEFT JOIN fato_meta_municipio mt
  ON mt.ano = i.ano AND mt.id_municipio = i.id_municipio;
