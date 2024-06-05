from time import sleep
from pprint import pprint
import PySimpleGUI as sg
from src.views.movimentacao_register_view import tela_adicionar_movimentacao, atualizar_combo, atualizar_table_mov
from src.views.categoria_register_view import tela_adicionar_categoria, atualizar_table
from src.controllers.movimentacao_register_controller import adicionar_movimentacao
from src.controllers.categoria_register_controller import * 

def start() -> None:
    sg.set_options(suppress_raise_key_errors=False, suppress_error_popups=False, suppress_key_guessing=False)

    # Cria as janelas iniciais
    jan_adicionar_movimentacao, jan_adicionar_categoria = tela_adicionar_movimentacao(), None
    linha = None # vai guardar a linha quando for deletar|editar um registro
    categoria_updt_info = {} # vai guardar as infos do registro a ser editado   

    while True:
        # comando = introduction_page()
        window, event, values = sg.read_all_windows()

        if window == jan_adicionar_movimentacao and event == sg.WIN_CLOSED:
            break        
        
        elif window == jan_adicionar_movimentacao and event in ('-TIPO_ENT-', '-TIPO_SAI-'):
            atualizar_combo(values, window)

        elif window == jan_adicionar_movimentacao and event == '-ADC_MOVIMENTACAO_BTN-':
            # aplicar o controller
            tipo = None
            if values['-TIPO_ENT-'] == True: tipo = 2
            elif values['-TIPO_SAI-']: tipo = 1
                
            categoria = values['-COMBO-']
            valor = values['-VALOR-']
            obs = values['-OBS-']
            data = values['-DATA_INPUT-']

            new_movimentacao_info = {
            'data': data,  
            'tipo': tipo, 
            'categoria': categoria, 
            'valor': valor, 
            'obs': obs
            }

            # aplicar controller
            response = adicionar_movimentacao(new_movimentacao_info)
            if response['success']:
                sg.popup("""Movimentação adicionada com sucesso.""",
                          title='Sucesso')
            else:
                sg.popup_error(f"Erro: {response['error']['erro']}", title='Erro de preenchimento')
            
            # atualizar tabela
            sleep(1)
            atualizar_table_mov(window)

        elif window == jan_adicionar_movimentacao and event == '-CALENDAR_BTN-':
            data = sg.popup_get_date()
            if data != None:
                mes, dia, ano = data
                window['-DATA_INPUT-'].update(f"{dia:0>2d}-{mes:0>2d}-{ano}")
        
        # salva a linha do registro a ser excluido
        elif '+CLICKED+' in event:
            linha = event[2][0]
            
        elif window == jan_adicionar_movimentacao and event == '-DEL_MOVIMENTACAO_BTN-':
            msg = f"""
            evento: {str(event)}
            linha: {str(linha+1)}
            """
            sg.popup(msg, title='')
       
        # ========================= JANELA CATEGORIA =========================
        # abre a janela de categoria
        elif window == jan_adicionar_movimentacao and event == '-CAT_BTN-':
            jan_adicionar_categoria = tela_adicionar_categoria()
            jan_adicionar_movimentacao.hide()

        # adiciona nova categoria
        elif window == jan_adicionar_categoria and event == '-ADC_CAT_BTN-':
            tipo = None
            if values['-TIPO_SAI-'] == True: tipo = 1
            elif values['-TIPO_ENT-'] == True: tipo = 2
            novaCat = values['-CAT_INPUT-']
            new_categoria_info = {
                'categoria': novaCat,
                'tipo': tipo
            }

            # aplicar o controller
            response = adicionar_categoria(new_categoria_info)
            if response['success']:
                sg.popup(f"""Categoria *{response['message']['atributos']['categoria']}* registrada com sucesso.""",
                          title='Sucesso')
            else:
                sg.popup_error(f"Erro: {response['error']['erro']}", title='Erro de preenchimento')
            
            # atualizar tabela
            sleep(1)
            atualizar_table(window)

        # fecha a janela de categoria e volta para movimentação
        elif window == jan_adicionar_categoria and event in ('-RETORNAR-', sg.WIN_CLOSED):
            jan_adicionar_categoria.hide()
            jan_adicionar_movimentacao.un_hide()
        
        # salva a linha do registro a ser excluido
        elif '+CLICKED+' in event:
            linha = event[2][0]

        # exclui o registro   
        elif window == jan_adicionar_categoria and event == '-EXCLUIR_BTN-':
            if linha == None:
                sg.popup("Nenhum registro selecionado", title='')
            else:
                if sg.popup_ok_cancel('Esta ação não pode ser desfeita, continuar?', title='Alerta') == 'OK':
                    # aplicar o controlador
                    categorias = pegar_categorias()
                    delCat = categorias['tuplas'][linha][1]
                    apagar_categoria(delCat)
                    linha = None

                    # atualizar tabela
                    sleep(1)
                    atualizar_table(window)

        # edita o registro
        elif window == jan_adicionar_categoria and event == '-SALVAR_BTN-':
            categorias = pegar_categorias()
            catAtual = categorias['tuplas'][linha][0]

            novoTipo = None
            if values['-TIPO_SAI-'] == True: novoTipo = 1
            elif values['-TIPO_ENT-'] == True: novoTipo = 2
            novaCat = values['-CAT_INPUT-']
            
            categoria_updt_info = {
                'categoriaAtual': catAtual,
                'tipoAtual': tipoAtual,
                'updtCategoria': novaCat,
                'updtTipo': novoTipo
            }

            #aplicar controller
            response = editar_categoria(categoria_updt_info)
            if response['success']:
                message = f"""Categoria {catAtual} aterada para > *{response['message']['atributos']['updtCategoria']}* com sucesso.
                """
                sg.popup(message, title='Sucesso')
            else:
                sg.popup_error(f"Erro: {response['error']['erro']}", title='Erro de preenchimento')
            linha = None
            window['-SALVAR_BTN-'].update(disabled=True)

            # atualizar tabela
            sleep(1)
            atualizar_table(window)

        # altera o registro
        elif window == jan_adicionar_categoria and event == '-EDITAR_BTN-':
            if linha == None:
                sg.popup("Nenhum registro selecionado", title='')
            else:
                categorias = pegar_categorias()
                id, catAtual, tipoAtual = categorias['tuplas'][linha]

                window['-CAT_INPUT-'].update(catAtual)
                window['-SALVAR_BTN-'].update(disabled=False)

    window.close()

if __name__ == '__main__':
    start()
    # cats = pegar_categorias()
    # # cats = list(map(lambda c: (c[1], c[2]), cats['tuplas']))
    # cat = 'SALÁRIO'
    # cat = [c[0] for c in cats['tuplas'] if c[1] == cat]
    # pprint(cats['tuplas'])
    # print(f'id: {cat[0]}')
    # novaCat = {
    #     'categoria': '',
    #     'tipo': 1
    # }
    # adicionar_categoria(novaCat)

    # movs = pegar_movimentacoes()
    # print(movs)