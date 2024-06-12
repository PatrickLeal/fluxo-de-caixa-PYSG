from time import sleep
from datetime import datetime as dt
import PySimpleGUI as sg
from src.views import movimentacao_register_view as MovView
from src.views import categoria_register_view as CatView
from src.controllers import movimentacao_register_controller as MovController
from src.controllers import categoria_register_controller as CatController

def start() -> None:
    sg.set_options(suppress_raise_key_errors=False, suppress_error_popups=False, suppress_key_guessing=False)

    # Cria as janelas iniciais
    jan_adicionar_movimentacao, jan_adicionar_categoria = MovView.tela_adicionar_movimentacao(), None
    linha = None # vai guardar a linha quando for deletar|editar um registro
    categoria_updt_info = {} # vai guardar as infos do registro a ser editado   

    while True:
        # comando = introduction_page()
        window, event, values = sg.read_all_windows()

        if window == jan_adicionar_movimentacao and event == sg.WIN_CLOSED:
            break        
        
        # SALVAR CAIXA INICIAL
        elif window == jan_adicionar_movimentacao and event == '-BTN_CAIXA_INICIAL-':
            valor_cx_inicial = values['-INP_CAIXA_INICIAL-']
            response = MovController.salvar_caixa_inicial(valor_cx_inicial)
            if response['success'] == False:
                sg.popup_error(response['error']['erro'], title='')
            else:
                window['-TXT_CX_INICIAL-'].update(visible=True)
                MovView.atualizar_cx_inicial(window)
                sleep(.5)
                MovView.atualizar_table_mov(window)
                MovView.atualizar_resumo_geral(window)

        
        elif window == jan_adicionar_movimentacao and event in ('-TIPO_ENT-', '-TIPO_SAI-'):
            MovView.atualizar_combo(values, window)

        # === ADICIONAR MOVIMENTAÇÃO ===
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
            response = MovController.adicionar_movimentacao(new_movimentacao_info)
            if response['success']:
                sg.popup("""Movimentação adicionada com sucesso.""", title='Sucesso')
                # atualizar tabela
                sleep(.5)
                hoje = dt.strftime(dt.today(), "%d-%m-%Y")
                MovView.atualizar_table_mov(window)
                MovView.atualizar_resumo_geral(window)
                window['-DATA_INPUT-'].update(hoje)
            else:
                sg.popup_error(f"Erro: {response['error']['erro']}", title='Erro de preenchimento')

        elif window == jan_adicionar_movimentacao and event == '-CALENDAR_BTN-':
            data = sg.popup_get_date()
            if data != None:
                mes, dia, ano = data
                window['-DATA_INPUT-'].update(f"{dia:0>2d}-{mes:0>2d}-{ano}")
                    
        # === ADICIONAR MOVIMENTAÇÃO ===   
        elif window == jan_adicionar_movimentacao and event == '-DEL_MOVIMENTACAO_BTN-':
            if linha == None:
                sg.popup("Nenhum registro selecionado", title='')
            else:
                if sg.popup_ok_cancel('Esta ação não pode ser desfeita, continuar?', title='Alerta') == 'OK':
                    # aplicar o controlador
                    all_movimentacoes = MovController.pegar_movimentacoes()
                    idMov = all_movimentacoes[linha][0]
                    MovController.apagar_movimentacao(idMov)
                    linha = None

                    # atualizar tabela
                    sleep(1)
                    MovView.atualizar_table_mov(window)
                    MovView.atualizar_resumo_geral(window)

        # ========================= JANELA CATEGORIA =========================
        # abre a janela de categoria
        elif window == jan_adicionar_movimentacao and event == '-CAT_BTN-':
            jan_adicionar_categoria = CatView.tela_adicionar_categoria()
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
            response = CatController.adicionar_categoria(new_categoria_info)
            if response['success']:
                sg.popup(f"""Categoria *{response['message']['atributos']['categoria']}* registrada com sucesso.""",
                          title='Sucesso')
            else:
                sg.popup_error(f"Erro: {response['error']['erro']}", title='Erro de preenchimento')
            
            # atualizar tabela
            sleep(1)
            CatView.atualizar_table(window)

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
                msg = """Excluir esta categoria apagará as movimentações atribuidas a ela.
                Esta ação não pode ser desfeita, continuar?
                """
                if sg.popup_ok_cancel(msg, title='Alerta') == 'OK':
                    # aplicar o controlador
                    categorias = CatController.pegar_categorias()
                    delCat = categorias['tuplas'][linha][1]
                    CatController.apagar_categoria(delCat)
                    linha = None

                    # atualizar tabela
                    sleep(1)
                    CatView.atualizar_table(window)

        # edita o registro
        elif window == jan_adicionar_categoria and event == '-SALVAR_BTN-':
            categorias = CatController.pegar_categorias()
            catAtual = categorias['tuplas'][linha][1]

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
            response = CatController.editar_categoria(categoria_updt_info)
            if response['success']:
                message = f"""Categoria {categoria_updt_info['categoriaAtual']} aterada para > *{response['message']['atributos']['updtCategoria']}* com sucesso.
                """
                sg.popup(message, title='Sucesso')
                 # atualizar tabela
                sleep(1)
                CatView.atualizar_table(window)
                MovView.atualizar_table_mov(jan_adicionar_movimentacao)
            else:
                sg.popup_error(f"Erro: {response['error']['erro']}", title='Erro de preenchimento')
            
            linha = None
            window['-SALVAR_BTN-'].update(disabled=True)

        # altera o registro
        elif window == jan_adicionar_categoria and event == '-EDITAR_BTN-':
            if linha == None:
                sg.popup("Nenhum registro selecionado", title='')
            else:
                categorias = CatController.pegar_categorias()
                id, catAtual, tipoAtual = categorias['tuplas'][linha]

                window['-CAT_INPUT-'].update(catAtual)
                window['-SALVAR_BTN-'].update(disabled=False)

    window.close()

if __name__ == '__main__':
    start()