from src.services.conexao_database import conectar_database
from src.controllers.categoria_register_controller import pegar_categorias
from src.models.movimentacao import Movimentacao
from sqlite3 import Error
from typing import Dict
from datetime import datetime as dt

#1 - Pegar entradas
def adicionar_movimentacao(new_movimentacao_info: Dict) -> Dict:
    try:
        # verifica se a categoria já exite na base e valida
        validacao = __valida_movimentacao(new_movimentacao_info)
        if validacao['valido'] == False:
            return { 'success': False, 'error': validacao}
        
        # # adicionar nova movimentacao na base
        __cria_movimentacao_e_armazena(new_movimentacao_info)

        response = __formatar_resposta(new_movimentacao_info)
        return { 'success': True, 'message': response}
    except Exception as exception:
        return { 'success': False, 'error': exception}

# apagar registro
def apagar_movimentacao(idMov: int) -> Dict:
    """Função que apaga um registro do bd
    ...

    Parametros

    ----------

    :param idMov: 
        o ID da movimentação a ser deletada
    :type:  
        int
    :return: 
        Dict
    """
    idMov = idMov
    
    try:
        conn = conectar_database()
        cur = conn.cursor()
        query = f"""
        DELETE FROM TAB_MOVIMENTACOES
        WHERE ID_num = {idMov};
        """
        cur.execute(query)
        conn.commit()       
        conn.close()

        response = "registro deletado com sucesso."
        return { 'success': True, 'message': response}
    except Error as error:
        return { 'success': False, 'error': error}

def pegar_movimentacoes():
    """
    # Função que pega os registros do bd
    ...

    Parametros
    ----------
    :return: 
        Uma lista de tuplas:
            [(), (), ()]
    """

    conn = conectar_database()
    cur = conn.cursor()
    query = "SELECT * FROM view_movimentacoes"
    cur.execute(query)
    res = cur.fetchall()
    conn.close()

    return res

def pegar_caixa_inicial():
    """
    # Função que pega o valor do caixa inicial
    ...

    Parametros
    ----------
    :return: 
        Uma Scalar em uma tupla:
            ()
        Ou:
            None
    """

    conn = conectar_database()
    cur = conn.cursor()
    query = "SELECT CAIXA_INICIAL_num FROM TAB_CAIXA_INICIAL"
    cur.execute(query)
    res = cur.fetchone()
    conn.close()

    return res

def salvar_caixa_inicial(valor) -> Dict:
    try:
        validacao = __valida_caixa_inicial(valor)
        if validacao['valido'] == False:
            return { 'success': False, 'error': validacao}
        
        valor = float(str(valor).replace(',', '.'))
        cx_inicial = pegar_caixa_inicial()
        conn = conectar_database()
        cur = conn.cursor()

        if cx_inicial == None:
            cur.execute("""
            INSERT INTO TAB_CAIXA_INICIAL ( CAIXA_INICIAL_num ) 
            VALUES (?)""", (valor, ))
            conn.commit()
            conn.close()
            return { 'success': True}
        else:
            cur.execute(f"""UPDATE TAB_CAIXA_INICIAL
                            SET CAIXA_INICIAL_num = {valor}""")
            conn.commit()
            conn.close()
            return { 'success': True}
        
    except Error as error:
        return { 'success': False, 'error': error}

#2 - validar entradas
def __valida_movimentacao(new_movimentacao_info: Dict) -> Dict:
    if new_movimentacao_info['data'] == '':
        erro = 'O campo "data" não pode estar vazio!'
        return { 'valido': False, 'erro': Exception(erro) }

    elif new_movimentacao_info['categoria'] == '':
        erro = 'O campo "categoria" não pode estar vazio!'
        return { 'valido': False, 'erro': Exception(erro) }
        
    elif new_movimentacao_info['valor'] == '':
        erro = 'O campo "valor" não pode estar vazio!'
        return { 'valido': False, 'erro': Exception(erro) }
    
    elif new_movimentacao_info['tipo'] == None:
        erro = 'Um tipo precisa ser escolhido!'
        return {'valido': False, 'erro': Exception(erro) }
    
    elif len(new_movimentacao_info['obs']) > 501:
        erro = 'O campo "observação" deve ser menor que 502 caracteres'
        return {'valido': False, 'erro': Exception(erro) }
    
    try:
        valor = str(new_movimentacao_info['valor']).replace(',', '.')
        float(valor)
    except: 
        erro = 'O campo "valor" precisa ser numérico!'
        return {'valido': False, 'erro': Exception(erro) }
    
    valor = float(str(new_movimentacao_info['valor']).replace(',', '.'))
    if valor < 0:
        erro = 'O campo "valor" precisa ser maior que 0 (zero)!'
        return { 'valido': False, 'erro': Exception(erro) }

    try:
        dt.strptime(new_movimentacao_info['data'], "%d-%m-%Y")
    except:
        erro = 'Campo "data" inválido!'
        return { 'valido': False, 'erro': Exception(erro) }
    
    return {'valido': True}

#3 - criar model e adicionar no bd
def __cria_movimentacao_e_armazena(new_movimentacao_info: Dict) -> None:
    cats = pegar_categorias()
    cat = new_movimentacao_info['categoria']

    data = dt.strptime(new_movimentacao_info['data'], "%d-%m-%Y")
    data = dt.strftime(data, "%Y-%m-%d")
    tipo = new_movimentacao_info['tipo']
    categoria = [c[0] for c in cats['tuplas'] if c[1] == cat]
    categoria = categoria[0]
    obs = new_movimentacao_info['obs']
    valor = str(new_movimentacao_info['valor']).replace(',', '.')
    valor = float(valor)

    movimentacao = Movimentacao(DATA_txt=data,
                                ID_TIPO_num=tipo,
                                ID_CATEGORIA_num=categoria,
                                OBSERVACAO_txt=obs,
                                VALOR_num=valor
                                )
    
    try:
        conn = conectar_database()
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO TAB_MOVIMENTACOES (DATA_txt, ID_TIPO_num, ID_CATEGORIA_num, OBSERVACAO_txt, VALOR_num)
        VALUES (?, ?, ?, ?, ?)""", (movimentacao.DATA_txt,
                                    movimentacao.ID_TIPO_num,
                                    movimentacao.ID_CATEGORIA_num,
                                    movimentacao.OBSERVACAO_txt,
                                    movimentacao.VALOR_num))
        conn.commit()       
        conn.close()
    except Error as error:
        conn.rollback()
        raise Exception(error)

#4 - formatar respota
def __formatar_resposta(new_movimentacao_info: Dict) -> Dict:
    return {
        'count': 1,
        'type': 'Movimentação',
        'atributos': new_movimentacao_info
    }

def __valida_caixa_inicial(valor) -> Dict:
    if valor == '': # verifica se está vazio
        erro = 'O campo "caixa inicial" não pode estar vazio!'
        return {'valido': False, 'erro': Exception(erro)} #retorna
       
    try:
        valor = str(valor).replace(',', '.')
        float(valor)
    except: 
        erro = 'O campo "valor" precisa ser numérico!'
        return {'valido': False, 'erro': Exception(erro) }
    
    valor = float(str(valor).replace(',', '.'))
    if valor < 0:
        erro = 'O campo "valor" precisa ser maior que 0 (zero)!'
        return { 'valido': False, 'erro': Exception(erro) }
    
    return {'valido': True}