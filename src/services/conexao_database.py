import os
import sqlite3
from sqlite3 import Error

dbPath = os.path.dirname(__file__)
db_exists = os.path.exists(f"{dbPath}\\FX_CAIXA.db")

nomeBanco = f"{dbPath}\\FX_CAIXA.db"

# Func para criar Conexão com o banco
def conectar_database():
    """Essa função retorna uma conexao com o db SQLite"""

    conexao = None
    try:
        conexao = sqlite3.connect(nomeBanco)
        cursor = conexao.cursor()

        if not db_exists:
            # Criar tabela TAB_MOVIMENTACOES
            cursor.execute('''
            CREATE TABLE TAB_MOVIMENTACOES (
                ID_num           INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                DATA_txt         TEXT (14),
                ID_TIPO_num      INTEGER (2),
                ID_CATEGORIA_num INTEGER,
                OBSERVACAO_txt   VARCHAR (502),
                VALOR_num        REAL)
            ''')

            # Criar tabela TAB_TIPO
            cursor.execute('''
            CREATE TABLE TAB_TIPO (
                ID_num   INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                TIPO_txt VARCHAR (20))
            ''')
            
            # Criar tabela TAB_CATEGORIA
            cursor.execute('''
            CREATE TABLE TAB_CATEGORIA (
                ID_num        INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                CATEGORIA_txt VARCHAR (50) UNIQUE,
                ID_TIPO_num   INTEGER (2)  REFERENCES TAB_TIPO (ID_num))
            ''')
            
            # Criar tabela TAB_CAIXA_INICIAL
            cursor.execute('''
            CREATE TABLE TAB_CAIXA_INICIAL (
                CAIXA_INICIAL_num REAL)
            ''')
            

            # Inserir tipos na tabela TAB_TIPO
            tipos = [(1, 'SAÍDA'),
                     (2, 'ENTRADA')]
            cursor.executemany("""
                INSERT INTO TAB_TIPO (ID_num, TIPO_txt) VALUES (?, ?)
            """, tipos)      

            # Criar a visualização view_categorias
            cursor.execute('''
            CREATE VIEW view_categorias AS
            SELECT 
                C.CATEGORIA_txt AS CATEGORIA,
                T.TIPO_txt AS TIPO
            FROM TAB_CATEGORIA C
            INNER JOIN TAB_TIPO T ON C.ID_TIPO_num = T.ID_num
            ''')
            
            # Criar a visualização view_movimentacoes
            cursor.execute("""
            CREATE VIEW view_movimentacoes AS
            WITH cte AS (
            SELECT 
                M.ID_num as ID,
                M.DATA_txt as DATA,
                T.TIPO_txt as TIPO,
                C.CATEGORIA_txt as CATEGORIA,
                M.OBSERVACAO_txt as OBS,
                M.VALOR_num as VALOR,
                CASE 
                    WHEN M.ID_TIPO_num = 2 THEN M.VALOR_num
                    WHEN M.ID_TIPO_num = 1 THEN -M.VALOR_num
                    ELSE 0 
                END AS valor_ajustado
            FROM 
                TAB_MOVIMENTACOES M
                JOIN TAB_TIPO T ON M.ID_TIPO_num = T.ID_num
                JOIN TAB_CATEGORIA C ON M.ID_CATEGORIA_num = C.ID_num
            )
            SELECT
                ID,
                strftime('%d-%m-%Y', DATA) as DATA,
                TIPO,
                CATEGORIA,
                CASE
                    WHEN OBS IS NOT NULL THEN OBS
                    ELSE ''
                END as OBS,
                FORMAT('R$ %2.2f', VALOR) as VALOR,
            FORMAT('R$ %2.2f', (SELECT CAIXA_INICIAL_num FROM TAB_CAIXA_INICIAL) + SUM(valor_ajustado)
                OVER (ORDER BY DATE(DATA), ID)) AS SALDO_ATUAL
            FROM cte
            ORDER BY DATE(DATA), ID
            """)

            conexao.commit()
    except Error as err:
        print(err)

    return conexao