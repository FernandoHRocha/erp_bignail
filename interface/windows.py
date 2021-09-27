import PySimpleGUI as sg
from interface import patterns as pt
from interface import event_handler as evh

titulo_janelas = {
    'janela_menu':'BigNail ERP',
    'janela_consulta':'Consultas',
    'janela_cadastro':'Cadastros',
    'janela_comprasnet':'Compras Net',
    'janela_consulta_pregao':'Consulta de processo participado'
}

theme = 'DarkGrey5'

def janela_menu():
    sg.theme(theme)
    layout = [[
            sg.Button('Cadastros',key='bt_cadastrar',enable_events=True, size=(20,1))],
        [   sg.Button('Consultas',key='bt_consultar',enable_events=True, size=(20,1))],
        [   sg.Button('Compras Net',key='bt_comprasnet',enable_events=True, size=(20,1))],
        ]
    return sg.Window(title=titulo_janelas['janela_menu'], layout=layout, finalize=True)

def janela_consulta():
    sg.theme(theme)
    layout = [[
            sg.Button('Processos a Submeter',key='bt_submeter',enable_events=True, size=(20,1))],
        [   sg.Button('Processos a Disputar',key='bt_disputar',enable_events=True, size=(20,1))],
        [   sg.Button('Processos em Julgamento',key='bt_julgamento',enable_events=True, size=(20,1))],
        [   sg.Button('Processos Participado',key='bt_consulta_pregao',enable_events=True, size=(20,1))],
        [pt.voltar()]
        ]
    return sg.Window(title=titulo_janelas['janela_consulta'], layout=layout, finalize=True)

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
    return sg.Window(title=titulo_janelas['janela_comprasnet'], layout=layout, finalize=True)

def janela_consulta_pregao():

    orgaos = evh.atualizar_lista_orgao()

    sg.theme(theme)
    cabecalho_geral = [
        ['ID','Item','Colocação','Produto','Nosso Preço','Melhor Preço','Estado'],
        [5,4,4,20,10,10,15]
    ]
    cabecalho_ganhos = [
        ['ID','Item','Categoria','Produto','Marca/Modelo','Restam','Valor','Valor Total','Custo','Custo Total','Margem','Fornecedor'],
        [5,4,15,20,30,6,10,10,10,10,8,15]
    ]

    layout=[[
        sg.Text('Órgão: ',(10,1), click_submits=False,enable_events=False),
        sg.Combo(values=orgaos,size=(40,1),enable_events=True,key='cb_orgao',readonly=True),
        sg.Text(' UASG ',(10,1),enable_events=False,visible=False),
        sg.Combo(values=[],size=(10,1),enable_events=True,key='cb_pregao',visible=False,readonly=True)
    ],
    [
        sg.Frame(
        layout=[
            [
                sg.TabGroup(
                    [[
                    sg.Tab('Geral', pt.tabelaItens(cabecalho_geral[0],'tb_geral',larguras=cabecalho_geral[1]),key='tab_geral',visible=True),
                    sg.Tab('Ganhos', pt.tabelaItens(cabecalho_ganhos[0],'tb_ganho',larguras=cabecalho_ganhos[1]),key='tab_ganho',visible=True)
                    ]],enable_events=True,key='tg_item')
            ],
        ],title='Itens',visible=False,key='fr_itens_participados'),
    ],
    [pt.voltar()]
    ]
    return sg.Window(title=titulo_janelas['janela_consulta_pregao'], layout=layout, finalize=True)