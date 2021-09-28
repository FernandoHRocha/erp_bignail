import PySimpleGUI as sg
from interface import patterns as pt
from interface import event_handler as evh

titulo_janelas = {
    'janela_menu':'BigNail ERP',
    'janela_consulta':'Consultas',
    'janela_cadastro':'Cadastros',
    'janela_comprasnet':'Compras Net',
    'janela_consulta_pregao':'Consulta de processo participado',
    'janela_consulta_pregoes':'Visão Geral dos processos'
}

sg.theme('DarkGrey5')

def janela_menu():
    """Retorna um menu com as principais opções para gerenciamentos dos processos licitatórios da empresa."""
    layout = [[
            sg.Button('Cadastros',key='bt_cadastrar',enable_events=True, size=(20,1))],
        [   sg.Button('Consultas',key='bt_consultar',enable_events=True, size=(20,1))],
        [   sg.Button('Compras Net',key='bt_comprasnet',enable_events=True, size=(20,1))],
        ]
    return sg.Window(title=titulo_janelas['janela_menu'], layout=layout, finalize=True)

###JANELAS DESTINADAS A PROCEDIMENTOS DE CONSULTAS

def janela_consulta():
    """Retorna um sg.Window destinado a mostrar as opções de diferentes consultas disponíveis."""
    layout = [[
            sg.Button('Processos Geral',key='bt_consulta_geral',enable_events=True, size=(20,1))],
        [   sg.Button('Buscar Participado',key='bt_consulta_pregao',enable_events=True, size=(20,1))],
        ]
    return sg.Window(title=titulo_janelas['janela_consulta'], layout=layout, finalize=True)

def janela_consulta_pregao():
    """Retorna um sg.Window contendo uma frame com a busca de pregão, e uma frame com tabela e botões."""
    orgaos = evh.atualizar_lista_orgao()

    cabecalho_registrado = [
        ['ID','Item','Modelo','Quantidade','Nosso Preço','Custo','Frete','Fornecedor','Marca'],
        [5,4,20,10,12,12,10,20,15]
    ]
    cabecalho_ganhos = [
        ['ID','Item','Categoria','Produto','Marca/Modelo','Restam','Valor','Valor Total','Custo','Custo Total','Margem','Fornecedor'],
        [5,4,15,20,30,6,10,10,10,10,8,15]
    ]

    layout=[
        pt.frame_orgaos_pregao(orgaos),
        [sg.Frame(title='',visible=False,key='fr_itens_participados',layout=[
            [
            sg.TabGroup([
                [
                    sg.Tab('Registrados', pt.tabela_itens(cabecalho_registrado[0],'tb_registrado',larguras=cabecalho_registrado[1]),key='tab_registrado',visible=True),
                    sg.Tab('Ganhos', pt.tabela_itens(cabecalho_ganhos[0],'tb_ganho',larguras=cabecalho_ganhos[1]),key='tab_ganho',visible=True)
                ]
                ],enable_events=True,key='tg_item')
            ],
            [
                sg.Button('Alterar item',enable_events=True,key='bt_item_alterar'),
                sg.Button('Registrar Pedido',enable_events=True,key='bt_item_pedido'),
                sg.Button('Registrar Carona',enable_events=True,key='bt_item_carona'),
            ]
            ]),
        ],
        [pt.bt_voltar()]
    ]
    return sg.Window(title=titulo_janelas['janela_consulta_pregao'], layout=layout, finalize=True)

def janela_consulta_pregoes():
    """Retorna um sg.Window com tabela e abas para apresentação dos pregões."""
    cabecalho_generico = [
        ['Abertura','Nº Pregão','UASG','ÓRGÃO'],
        [20,10,8,30]
    ]
    abas = evh.lista_pregoes_gerais()
    layout=[
        [
            sg.TabGroup(
                [[pt.aba_com_tabela_itens(cabecalho_generico,aba[0],aba[1]) for aba in abas]
                ],enable_events=True,key='tg_item')
        ],
        [pt.bt_voltar()]
        ]
    return sg.Window(title=titulo_janelas['janela_consulta_pregoes'],layout=layout,finalize=True)

###JANELAS DESTINADAS A CADASTROS

def janela_cadastro():
    """Retorna um sg.Window destinado a mostrar as opções de diferentes cadastros disponíveis."""
    layout = [[
            sg.Button('Planilha de Cotação',key='bt_planilha',enable_events=True, size=(20,1))],
        [   sg.Button('Registrar Pedido',key='bt_pedido',enable_events=True, size=(20,1))],
        [   sg.Button('Registrar Carona',key='bt_carona',enable_events=True, size=(20,1))],
        ]
    return sg.Window(titulo_janelas['janela_cadastro'], layout, finalize=True)

###JANELAS DESTINADAS AOS PROCESSOS DE AUTOMAÇÃO

def janela_comprasnet():
    """Retorna um sg.Window com botões para executar as principais automações."""
    layout = [[
            sg.Button('Cadastrar Pregão',key='bt_cadastrar',enable_events=True, size=(20,1))],
        [   sg.Button('Consultar Novidades',key='bt_consultar',enable_events=True, size=(20,1))],
        [   sg.Button('Participar de Disputa',key='bt_disputar',enable_events=True, size=(20,1))],
        ]
    return sg.Window(title=titulo_janelas['janela_comprasnet'], layout=layout, finalize=True)
