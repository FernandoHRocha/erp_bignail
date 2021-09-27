import PySimpleGUI as sg
from interface import patterns as pt

titulo_janelas = {
    'janela_menu':'BigNail ERP',
    'janela_consulta':'Consultas',
    'janela_cadastro':'Cadastros',
    'janela_comprasnet':'Compras Net'
}

theme = 'DarkGrey5'

def janela_menu():
    sg.theme(theme)
    layout = [[
            sg.Button('Cadastros',key='bt_cadastrar',enable_events=True, size=(20,1))],
        [   sg.Button('Consultas',key='bt_consultar',enable_events=True, size=(20,1))],
        [   sg.Button('Compras Net',key='bt_comprasnet',enable_events=True, size=(20,1))],
        ]
    return sg.Window(titulo_janelas['janela_menu'], layout, finalize=True)

def janela_consulta():
    sg.theme(theme)
    layout = [[
            sg.Button('Processos a Submeter',key='bt_submeter',enable_events=True, size=(20,1))],
        [   sg.Button('Processos a Disputar',key='bt_disputar',enable_events=True, size=(20,1))],
        [   sg.Button('Processos em Julgamento',key='bt_julgamento',enable_events=True, size=(20,1))],
        [pt.voltar()]
        ]
    return sg.Window(titulo_janelas['janela_consulta'], layout, finalize=True)

def janela_cadastro():
    sg.theme(theme)
    layout = [[
            sg.Button('Cadastrar Planilha',key='bt_planilha',enable_events=True, size=(20,1))],
        [   sg.Button('Registrar Pedido',key='bt_pedido',enable_events=True, size=(20,1))],
        [   sg.Button('Registrar Carona',key='bt_carona',enable_events=True, size=(20,1))],
        [pt.voltar()]
        ]
    return sg.Window(titulo_janelas['janela_cadastro'], layout, finalize=True)

def janela_comprasnet():
    sg.theme(theme)
    layout = [[
            sg.Button('Cadastrar Pregão',key='bt_cadastrar',enable_events=True, size=(20,1))],
        [   sg.Button('Consultar Novidades',key='bt_consultar',enable_events=True, size=(20,1))],
        [   sg.Button('Participar de Disputa',key='bt_disputar',enable_events=True, size=(20,1))],
        [pt.voltar()]
        ]
    return sg.Window(titulo_janelas['janela_comprasnet'], layout, finalize=True)