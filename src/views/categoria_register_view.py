from PySimpleGUI import PySimpleGUI as sg
from src.controllers.categoria_register_controller import pegar_categorias

# Layout
sg.theme('Reddit')

def atualizar_table(window):
    categorias = pegar_categorias()
    categorias = list(map(lambda c: (c[1], c[2]), categorias['tuplas']))
    window['-TAB-'].update(values=categorias)

def tela_adicionar_categoria():

    # FRAME
    rdEntrada = sg.Radio('ENTRADA', group_id=1, key='-TIPO_ENT-')
    rdSaida = sg.Radio('SAIDA', group_id=1, key='-TIPO_SAI-')
    frame_layout1 = [
        [sg.Text('Tipo:', size=(8 ,1), justification='r'), rdEntrada, rdSaida],
        [sg.Push(), sg.Text('Categoria:', size=(8 ,1)),
         sg.Input(key='-CAT_INPUT-', tooltip='Digite a nova categoria...', do_not_clear=False)]
        ]

    headings = ['CATEGORIAS', 'TIPOS']
    categorias = pegar_categorias()
    categorias = list(map(lambda c: (c[1], c[2]), categorias['tuplas']))
    tabCategorias = sg.Table(values=categorias, headings=headings,
                             justification='c', def_col_width=20,
                             expand_x=True, key='-TAB-',
                             num_rows=15, alternating_row_color='#99dbf9',
                             enable_click_events=True)
    
    layout = [
        [sg.Frame('Categoria', frame_layout1)],
        [sg.Button('Adicionar Categoria', key='-ADC_CAT_BTN-', enable_events=True,
                   button_color="green")],
        [sg.Button("Retornar", key='-RETORNAR-')],
        [tabCategorias],
        [sg.Button("Excluir Categoria", key='-EXCLUIR_BTN-', button_color='red'), sg.Button("Editar Categoria", key='-EDITAR_BTN-', size=(12, ))],
        [sg.Button("Salvar alterações", key='-SALVAR_BTN-', disabled=True, size=(12, ))]
    ]

    return sg.Window("Adicionar Categoria", layout=layout, element_justification='r', finalize=True)