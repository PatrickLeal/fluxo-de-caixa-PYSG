from PySimpleGUI import PySimpleGUI as sg
from datetime import datetime as dt
from src.controllers.categoria_register_controller import pegar_categorias
from src.controllers.movimentacao_register_controller import pegar_movimentacoes, pegar_caixa_inicial

# Layout
sg.theme('Reddit')

def atualizar_combo(values, window):
    categorias = pegar_categorias()
    if values['-TIPO_ENT-']:
        window['-COMBO-'].update(value='', values=sorted(categorias['dict']['ENTRADA']))
    elif values['-TIPO_SAI-']:
        window['-COMBO-'].update(value='', values=sorted(categorias['dict']['SAIDA']))

def atualizar_table_mov(window):
    movimentacoes = pegar_movimentacoes()
    window['-TAB_MOV-'].update(values=movimentacoes)

def tela_adicionar_movimentacao():
    movimentacoes = pegar_movimentacoes()
    hoje = dt.strftime(dt.today(), "%d-%m-%Y")
    headings = ['ID', 'DATA', 'TIPO', 'CATEGORIA', 'OBS', 'VALOR', 'SALDO'] 
    
    rdEntrada = sg.Radio('ENTRADA', group_id=1, key='-TIPO_ENT-', enable_events=True)
    rdSaida = sg.Radio('SAIDA', group_id=1, key='-TIPO_SAI-', enable_events=True)
    cbTipo = sg.Combo([], size=(20 ,1), key='-COMBO-', tooltip=' Escolha uma Categoria ',
                        enable_events=True, readonly=True, auto_size_text=True)
    btnNovaCat = sg.Button('Criar Nova Categoria', key='-CAT_BTN-')
    inpValor = sg.Input(key='-VALOR-', size=(10 ,1), tooltip='Digite um valor positivo.', do_not_clear=False)
    inpOBS = sg.Input(key='-OBS-', size=(20, 4), expand_x=True, do_not_clear=False)
    inpHoje = sg.Input(hoje, key='-DATA_INPUT-', size=(10 ,1))
    btnData = sg.Button(button_text='Escolha uma data', key='-CALENDAR_BTN-')

    # FRAME LAYOUT
    frame_layout = [
        [sg.Text('Tipo:', size=(8 ,1), justification='r'), rdEntrada, rdSaida],
        [sg.Text('Categoria:', size=(8 ,1), justification='r'), cbTipo, btnNovaCat],
        [sg.Text('Valor:', size=(8 ,1), justification='r'), inpValor],
        [sg.Text('OBS:', size=(8 ,1), justification='r'), inpOBS],
        [sg.Text('Data:', size=(8 ,1), justification='r'), inpHoje, btnData]
    ]

    # COLUNA LAYOUT
    bntADCMovimentacao = sg.Button(button_text='Adicionar Movimentação', key='-ADC_MOVIMENTACAO_BTN-', button_color='green')
    bntApagarMovimentacao = sg.Button(button_text='Apagar Movimentação', key='-DEL_MOVIMENTACAO_BTN-', button_color='red', size=(18, ))
    column_layout = [
        [bntADCMovimentacao],
        [bntApagarMovimentacao]
    ]

    # TELA LAYOUT
    tabMovimentacoes = sg.Table(values=movimentacoes, headings=headings, justification='c',
                                def_col_width=20, expand_x=True, key='-TAB_MOV-',
                                col_widths=[5, 10, 8, 12, 15, 6, 5], auto_size_columns=False,
                                num_rows=15, alternating_row_color='#99dbf9',
                                enable_click_events=True)
    
    cx_inicial = pegar_caixa_inicial()
    op_cx_inicial = None
    txt_cx_inicial = None
    
    # CAIXA INICIAL
    if cx_inicial == None:
        op_cx_inicial = sg.Input('', size=(10, ),
                             tooltip=" insira o valor do caixa inicial: ",
                             visible=True)
        txt_cx_inicial = sg.Text(str(cx_inicial), size=(10, 2) ,
                                 background_color='#7aafc7',
                                 visible=False)
    else:
        txt_cx_inicial = sg.Text(str(cx_inicial[0]), size=(10, 2),
                                 background_color='#7aafc7',
                                 visible=True)
        op_cx_inicial = sg.Input('', size=(10, ),
                             tooltip=" insira o valor do caixa inicial: ",
                             visible=False)
        # mostrar output com o valor

    layout = [
        [sg.Text('Caixa Inical:'), op_cx_inicial, txt_cx_inicial], 
        [tabMovimentacoes],
        [ sg.Frame('Adicionar Movimentações', frame_layout), sg.Column(column_layout, element_justification='l')],
    ]

    return sg.Window("Movimentações", layout=layout, finalize=True, size=(700, 500))

def main() -> None:
    # CRIANDO A JANELA
    janela = tela_adicionar_movimentacao()

    # Event Loop to process "events" and get the "values" of the inputs
    while True:

        eventos, valores = janela.read()

        if (eventos == sg.WINDOW_CLOSED):
            break

    janela.close()

if  __name__ == "__main__":
    main()
