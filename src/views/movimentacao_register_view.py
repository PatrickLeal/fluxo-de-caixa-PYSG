from PySimpleGUI import PySimpleGUI as sg
from datetime import datetime as dt
from src.controllers.categoria_register_controller import pegar_categorias
from src.controllers.movimentacao_register_controller import pegar_movimentacoes, pegar_caixa_inicial, pegar_resumo_geral

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

def atualizar_resumo_geral(window):
    resumo_geral = pegar_resumo_geral()
    if resumo_geral['soma_saida'][0] == None:
        soma_saida = "R$"
    else:
        soma_saida = f"R$ {resumo_geral['soma_saida'][0]:.2f}"

    if resumo_geral['soma_entrada'][0] == None:
        soma_entrada = 'R$'
    else:
        soma_entrada = f"R$ {resumo_geral['soma_entrada'][0]:.2f}"

    saldo_atual = resumo_geral['saldo_atual'][0]

    window['-TXT_SUM_SAIDA-'].update(soma_saida)
    window['-TXT_SUM_ENTRADA-'].update(soma_entrada)
    window['-TXT_SALDO_ATUAL-'].update(saldo_atual)

def atualizar_cx_inicial(window):
    caixa_inicial = pegar_caixa_inicial()
    valor_formatado = f"R$ {caixa_inicial[0]:_.2f}".replace('.', ',')
    window['-TXT_CX_INICIAL-'].update(value=valor_formatado.replace('_', '.'))

def tela_adicionar_movimentacao():
    hoje = dt.strftime(dt.today(), "%d-%m-%Y")
    
    
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
        [sg.Text('Data:', size=(8 ,1), justification='r'), inpHoje, btnData],
        [sg.Text('Valor:', size=(8 ,1), justification='r'), inpValor],
        [sg.Text('OBS:', size=(8 ,1), justification='r'), inpOBS]
    ]

    # COLUNA LAYOUT
    bntADCMovimentacao = sg.Button(button_text='Adicionar Movimentação', key='-ADC_MOVIMENTACAO_BTN-', button_color='green')
    bntApagarMovimentacao = sg.Button(button_text='Apagar Movimentação', key='-DEL_MOVIMENTACAO_BTN-', button_color='red', size=(18, ))
    column_layout = [
        [bntADCMovimentacao],
        [bntApagarMovimentacao]
    ]

    # TELA LAYOUT
    movimentacoes = pegar_movimentacoes()
    headings = ['ID', 'DATA', 'TIPO', 'CATEGORIA', 'OBS', 'VALOR', 'SALDO ATUAL'] 
    tabMovimentacoes = sg.Table(values=movimentacoes, headings=headings, justification='c',
                                def_col_width=20, expand_x=True, key='-TAB_MOV-',
                                col_widths=[5, 10, 8, 12, 15, 6, 8], auto_size_columns=False,
                                num_rows=15, alternating_row_color='#99dbf9',
                                enable_click_events=True)
    
    cx_inicial = pegar_caixa_inicial()
    inp_cx_inicial = None
    txt_cx_incial = None
    btnSalvarCXInicial = sg.Button("Salvar", key='-BTN_CAIXA_INICIAL-')
    
    # CAIXA INICIAL
    if cx_inicial == None:
        inp_cx_inicial = sg.Input(size=(8, ), focus=False,
                                  do_not_clear=False,
                                  tooltip=" Insira um valor... ",
                                  key='-INP_CAIXA_INICIAL-')
        txt_cx_incial = sg.Text(key='-TXT_CX_INICIAL-', visible=False,
                                size=(12, ),
                                font=('Arial bold', 16),
                                justification='center',
                                background_color='#84fe8f',
                                text_color='#0e2f44',)
    else:
        inp_cx_inicial = sg.Input(size=(8, ), focus=False,                           
                                  do_not_clear=False,
                                  tooltip=" Insira um valor... ",
                                  key='-INP_CAIXA_INICIAL-')
        
        valor_formatado = f"R$ {cx_inicial[0]:_.2f}".replace('.', ',')
        txt_cx_incial = sg.Text(valor_formatado.replace('_', '.'),
                                size=(12, ),
                                font=('Arial bold', 16),
                                justification='center',
                                background_color='#84fe8f',
                                text_color='#0e2f44',
                                key='-TXT_CX_INICIAL-', 
                                visible=True)

    
    resumo_geral = pegar_resumo_geral()

    # RESUMO GERAL
    if (resumo_geral['soma_saida'][0] == None) or (resumo_geral['soma_entrada'][0] == None):
        font = ('Microsoft PhagsPa bold', 12)  
        col1 = [[sg.Text('ENTRADAS', background_color='#0f1518', text_color='#ccedfc', font=font, size=(9, ), justification='c')],
                [sg.Text('R$', key='-TXT_SUM_ENTRADA-', size=(11, ), background_color='#0f1518', font=font, text_color='#ccedfc', justification='c')]]
        col2 = [[sg.Text('SAÍDAS', background_color='#0f1518', font=font, text_color='#ccedfc', size=(9, ), justification='c')],
                [ sg.Text('R$', key='-TXT_SUM_SAIDA-', size=(11, ), background_color='#0f1518', text_color='#ccedfc', font=font, justification='c')]]
        col3 = [[sg.Text('SALDO ATUAL', background_color='#0f1518', font=font, text_color='#ccedfc',)],
                [sg.Text('R$', key='-TXT_SALDO_ATUAL-', background_color='#0f1518', size=(11, ), text_color='#ccedfc', font=font, justification='c')]]
        frame_layout_resumo = [[sg.Column(col1, element_justification='c', background_color='#4c6d7c'),
                                sg.Column(col2, element_justification='c', background_color='#4c6d7c'),
                                sg.Column(col3, element_justification='c', background_color='#4c6d7c')]]
    else:
        soma_saida = f"R$ {resumo_geral['soma_saida'][0]:.2f}"
        soma_entrada = f"R$ {resumo_geral['soma_entrada'][0]:.2f}"
        saldo_atual = resumo_geral['saldo_atual'][0]
        font = ('Microsoft PhagsPa bold', 12)  
        col1 = [[sg.Text('ENTRADAS', background_color='#0f1518', text_color='#ccedfc', font=font, size=(9, ), justification='c')],
                [sg.Text(soma_entrada, key='-TXT_SUM_ENTRADA-', size=(11, ), background_color='#0f1518', font=font, text_color='#ccedfc', justification='c')]]
        col2 = [[sg.Text('SAÍDAS', background_color='#0f1518', font=font, text_color='#ccedfc', size=(9, ), justification='c')],
                [ sg.Text(soma_saida, key='-TXT_SUM_SAIDA-', size=(11, ), background_color='#0f1518', text_color='#ccedfc', font=font, justification='c')]]
        col3 = [[sg.Text('SALDO ATUAL', background_color='#0f1518', font=font, text_color='#ccedfc',)],
                [sg.Text(saldo_atual, key='-TXT_SALDO_ATUAL-', background_color='#0f1518', size=(11, ), text_color='#ccedfc', font=font, justification='c')]]
        frame_layout_resumo = [[sg.Column(col1, element_justification='c', background_color='#4c6d7c'),
                                sg.Column(col2, element_justification='c', background_color='#4c6d7c'),
                                sg.Column(col3, element_justification='c', background_color='#4c6d7c')]]

    layout = [
        [sg.Text('Caixa Inical:'), inp_cx_inicial, btnSalvarCXInicial, txt_cx_incial, 
         sg.Frame('', frame_layout_resumo, background_color='#4c6d7c')],
        [tabMovimentacoes],
        [ sg.Frame('Adicionar Movimentações', frame_layout), sg.Column(column_layout, element_justification='l')],
    ]

    return sg.Window("Movimentações", layout=layout, finalize=True, size=(800, 550))