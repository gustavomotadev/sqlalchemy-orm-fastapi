CREATE DATABASE locacao;

USE locacao;

CREATE TABLE locadora (
  uuid char(36) PRIMARY KEY,
  nome varchar(100) NOT NULL,
  horario_abertura time NOT NULL,
  horario_fechamento time NOT NULL,
  endereco varchar(255) NOT NULL
);

CREATE TABLE pessoa (
  uuid CHAR(36) PRIMARY KEY,
  cnh CHAR(11) UNIQUE NOT NULL,
  tipo VARCHAR(30) NOT NULL,
  nome VARCHAR(30) NOT NULL
);

CREATE TABLE veiculo (
  uuid CHAR(36) PRIMARY KEY,
  uuid_condutor CHAR(36) NOT NULL,
  modelo VARCHAR(30) NOT NULL,
  tipo VARCHAR(30) NOT NULL,
  combustivel VARCHAR(30) NOT NULL,
  capacidade TINYINT NOT NULL,
  cor VARCHAR(30) NOT NULL,
  FOREIGN KEY (uuid_condutor)
  REFERENCES pessoa(uuid)
  ON DELETE RESTRICT
  ON UPDATE RESTRICT
);

CREATE TABLE usuario (
  uuid CHAR(36) PRIMARY KEY,
  uuid_pessoa CHAR(36) UNIQUE NOT NULL,
  login VARCHAR(20) UNIQUE NOT NULL,
  salt_senha BINARY(29) NOT NULL,
  hash_senha BINARY(60) NOT NULL,
  FOREIGN KEY (uuid_pessoa)
  REFERENCES pessoa(uuid)
  ON DELETE RESTRICT
  ON UPDATE RESTRICT
);