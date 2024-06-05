import os
import sqlite3
from sqlite3 import Error

dbPath = os.path.dirname(__file__)
nomeBanco = f"{dbPath}\\FX_CAIXA.db"

# Func para criar Conexão com o banco
def conectar_database():
    """Essa função retorna uma conexao com o db SQLite"""
    conexao = None
    try:
        conexao = sqlite3.connect(nomeBanco)
    except Error as err:
        print(err)

    return conexao