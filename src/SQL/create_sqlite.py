import os
import sqlite3

NOME_BANCO = 'locadora.sqlite'
FOREIGN_KEY_SQL = 'PRAGMA foreign_keys=ON;'

def conectar():
        banco = sqlite3.connect(NOME_BANCO, check_same_thread=False)
        cursor = banco.cursor()
        cursor.execute(FOREIGN_KEY_SQL)
        return (banco, cursor)

if __name__ == '__main__':
    if not os.path.isfile(NOME_BANCO):
        print('Banco de dados não encontrado, novo banco será criado com valores iniciais.')
        with open('create.sql', 'r', encoding='utf8') as arquivo_sql:
            script_sql = arquivo_sql.read()
        (_,conexao) = conectar()
        conexao.executescript(script_sql)
        print('Banco de dados inicial criado.')
    else:
        print('Banco de dados encontrado.')