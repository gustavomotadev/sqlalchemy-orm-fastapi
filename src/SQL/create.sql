PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

CREATE TABLE locadora (
  uuid TEXT PRIMARY KEY,
  nome TEXT NOT NULL,
  horario_abertura TEXT NOT NULL,
  horario_fechamento TEXT NOT NULL,
  endereco TEXT NOT NULL
);

CREATE TABLE pessoa (
  uuid TEXT PRIMARY KEY,
  cnh TEXT UNIQUE NOT NULL,
  tipo TEXT NOT NULL,
  nome TEXT NOT NULL
);

CREATE TABLE veiculo (
  uuid TEXT PRIMARY KEY,
  uuid_condutor TEXT NOT NULL,
  placa TEXT UNIQUE NOT NULL,
  modelo TEXT NOT NULL,
  tipo TEXT NOT NULL,
  combustivel TEXT NOT NULL,
  capacidade INTEGER NOT NULL,
  cor TEXT NOT NULL,
  FOREIGN KEY (uuid_condutor)
  REFERENCES pessoa(uuid)
  ON DELETE RESTRICT
  ON UPDATE RESTRICT
);

CREATE TABLE usuario (
  uuid TEXT PRIMARY KEY,
  uuid_pessoa TEXT UNIQUE NOT NULL,
  acesso TEXT UNIQUE NOT NULL,
  salt_senha BLOB NOT NULL,
  hash_senha BLOB NOT NULL,
  FOREIGN KEY (uuid_pessoa)
  REFERENCES pessoa(uuid)
  ON DELETE RESTRICT
  ON UPDATE RESTRICT
);

COMMIT;
