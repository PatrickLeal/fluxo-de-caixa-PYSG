from src.services.conexao_database import conectar_database
from src.models.categorias import Categoria
from sqlite3 import Error
from typing import Dict

#continuar a lógica da função
def adicionar_categoria(new_categoria_info: Dict) -> Dict:
    try:
        # verifica se a categoria já exite na base e valida
        validacao = __valida_categoria(new_categoria_info['categoria'], new_categoria_info['tipo'])
        if validacao['valido'] == False:
            return { 'success': False, 'error': validacao}
        
        # adicionar nova categoria na base
        __criar_categoria_e_armazenar(new_categoria_info)

        response = __formatar_resposta(new_categoria_info)
        return { 'success': True, 'message': response}
    except Exception as exception:
        return { 'success': False, 'error': exception}

# editar registro
def editar_categoria(categoria_updt_info: Dict) -> Dict:
    try:
        # verifica se a categoria já exite na base e valida
        validacao = __valida_categoria_updt(categoria_updt_info['updtCategoria'], categoria_updt_info['updtTipo'])
        if validacao['valido'] == False:
            return { 'success': False, 'error': validacao}
        
        # adicionar nova categoria na base
        __criar_categoria_e_atualizar(categoria_updt_info)

        response = __formatar_resposta(categoria_updt_info)
        return { 'success': True, 'message': response}
    except Exception as exception:
        return { 'success': False, 'error': exception}

def pegar_categorias() -> Dict:
    """
    ## Função que pega todas as categorias do DB
    ...

    Retorna um dict com as categorias em dois formatos => em forma de dicionário e tuplas

    * return: 

    {
        dict: { "SAIDA": [],
                "ENTRADA":[] },
        tuplas: res   
    }
    
    """
    conn = conectar_database()
    cur = conn.cursor()
    query = "SELECT * FROM view_categorias"
    cur.execute(query)
    res = cur.fetchall()

    categorias_dict = {
        "SAIDA": [],
        "ENTRADA":[]
    }
    # fazer append no dict
    for c in res:
        if c[1] == 'SAÍDA': categorias_dict['SAIDA'].append(c[0])
        else: categorias_dict['ENTRADA'].append(c[0])

    query = """
    SELECT ID_num, CATEGORIA_txt,
    CASE
        WHEN ID_TIPO_num = 1 THEN "SAÍDA"
        ELSE "ENTRADA" 
    END 
    AS TIPOS
    FROM TAB_CATEGORIA
    """
    cur.execute(query)
    res = cur.fetchall()
    conn.close()
    
    return {
        'dict':categorias_dict,
        'tuplas': res
        }

# apagar registro
def apagar_categoria(categoria: str) -> Dict:
    """
    # Função que apaga um registro do bd
    ...

    Parametros
    ----------
    :param categoria: 
        A categoria a ser deletada
    :type:  
        str
    :return: 
        None
    """
    categoria = categoria
    
    try:
        conn = conectar_database()
        cur = conn.cursor()
        query = f"""
        DELETE FROM TAB_CATEGORIA
        WHERE CATEGORIA_txt = '{categoria}';
        """
        cur.execute(query)
        conn.commit()       
        conn.close()

        response = "registro deletado com sucesso."
        return { 'success': True, 'message': response}
    except Exception as error:
        return { 'success': False, 'error': error}

def __valida_categoria(nova_categoria, tipo):
    categorias_info = pegar_categorias()
    todas_categorias = []
    for c in categorias_info['tuplas']:
        todas_categorias.append(c[0])

    if nova_categoria == '':
        erro = 'O campo "categoria" não pode estar vazio!'
        return {'valido': False, 'erro': Exception(erro) }
    
    elif nova_categoria.isdigit():
        erro = f'''
        Campo "categoria" inválido!
        Você digitou: {nova_categoria}, digite uma categoria válida.
        '''
        return {'valido': False, 'erro': Exception(erro) }
        
    elif str.upper(nova_categoria) in todas_categorias:
        erro = 'Categoria já está cadastrada!'
        return {'valido': False, 'erro': Exception(erro) }
    
    elif tipo == None:
        erro = 'Um tipo precisa ser escolhido!'
        return {'valido': False, 'erro': Exception(erro) }
    
    return {'valido': True}
        
# FORMATA A RESPOSTA
def __formatar_resposta(new_categoria_info: Dict) -> Dict:
    return {
        'count': 1,
        'type': 'Categoria',
        'atributos': new_categoria_info
    }

def __criar_categoria_e_armazenar(new_categoria_info: Dict) -> None:
    categoria = str.upper(new_categoria_info['categoria'])
    tipo = new_categoria_info['tipo']
    novaCat = Categoria(categoria, tipo)

    try:
        conn = conectar_database()
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO TAB_CATEGORIA (CATEGORIA_txt, ID_TIPO_num)
        VALUES (?, ?)""", (novaCat.CATEGORIA_txt, novaCat.ID_TIPO_num))
        conn.commit()       
        conn.close()
    except Error as error:
        conn.rollback()
        raise Exception(error)
    
def __criar_categoria_e_atualizar(categoria_updt_info: Dict) -> None:
    catAtual = categoria_updt_info['categoriaAtual']
    updtCat = str.upper(categoria_updt_info['updtCategoria'])
    updtTipo = categoria_updt_info['updtTipo']
    novaCat = Categoria(updtCat, updtTipo)

    try:
        conn = conectar_database()
        cur = conn.cursor()
        query = f"""UPDATE TAB_CATEGORIA
        SET CATEGORIA_txt = '{novaCat.CATEGORIA_txt}', ID_TIPO_num = '{novaCat.ID_TIPO_num}'
        WHERE CATEGORIA_txt = '{catAtual}';
        """
        cur.execute(query)
        conn.commit()       
        conn.close()
    except Error as error:
        conn.rollback()
        errMessage = {
            'erro': f"{error}\n\nCertifique-se de que a categoria ainda não esteja cadastrada."
        }
        raise Exception(errMessage)
    
def __valida_categoria_updt(nova_categoria, tipo):

    if nova_categoria == '':
        erro = 'O campo "categoria" não pode estar vazio!'
        return {'valido': False, 'erro': Exception(erro) }
    
    elif nova_categoria.isdigit():
        erro = f'''
        Campo "categoria" inválido!
        Você digitou: {nova_categoria}, digite uma categoria válida.
        '''
        return {'valido': False, 'erro': Exception(erro) }
    
    elif tipo == None:
        erro = 'Um tipo precisa ser escolhido!'
        return {'valido': False, 'erro': Exception(erro) }
    
    return {'valido': True}