from tkinter import Text
import PySimpleGUI as sg
from interface import patterns as pt
from interface import event_handler as evh

titulo_janelas = {
    'janela_menu':'BigNail ERP',
    #menus principais
    'janela_consulta':'Consultas',
    'janela_cadastro':'Cadastros',
    'janela_comprasnet':'Compras Net',
    #consultas
    'janela_consulta_pregao':'Consulta de processo participado',
    'janela_consulta_pregoes':'Visão Geral dos processos',
    'janela_consulta_empenhos':'Empenhos realizados',
    'janela_consulta_reequilibrio':'Pedidos de Reequilíbrio Econômico',
    'janela_consulta_carona':'Pedidos de Carona',
    'janela_consulta_atas':'Atas de Processos',
    #cadastros
    'janela_cadastro_homologacao':'Homologar Pregão',
    #auxiliares
    'janela_consulta_pregao_alterar_fase':'Alteração de Fase'
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
            sg.Button('Listar Processos',key='bt_consulta_geral',enable_events=True, size=(20,1))],
        [   sg.Button('Buscar Pregão',key='bt_consulta_pregao',enable_events=True, size=(20,1))],
        [   sg.Button('Listar Empenhos',key='bt_consulta_empenhos',enable_events=True, size=(20,1))],
        [   sg.Button('Pedidos de Reequilíbrio',key='bt_consulta_reequilibrios',enable_events=True, size=(20,1))],
        [   sg.Button('Listar Caronas',key='bt_consulta_carona',enable_events=True, size=(20,1))],
        [   sg.Button('Atas de Processos',key='bt_consulta_atas',enable_events=True, size=(20,1))],
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
                sg.Button('Registrar Empenho',enable_events=True,key='bt_item_empenho'),
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
        ['Pregão','UASG','Abertura','ÓRGÃO'],
        [10,8,20,30]
    ]
    abas = evh.lista_pregoes_gerais()
    layout=[
        [
            sg.TabGroup(
                [[pt.aba_com_tabela_itens(cabecalho_generico,aba[0],aba[1]) for aba in abas]
                ],enable_events=True,key='tg_pregoes')
        ],
        [
            sg.Button('Alterar Fase',enable_events=True,key='bt_alterar_fase'),
            sg.Button('Abrir Pasta',enable_events=True,key='bt_pasta'),
            sg.Button('Homologar Pregão',enable_events=True,key='bt_homologar'),
        ],
        [pt.bt_voltar()]
        ]
    return sg.Window(title=titulo_janelas['janela_consulta_pregoes'],layout=layout,finalize=True)

def janela_consulta_empenhos():
    """Retorna um sg.Window com tabela e abas para apresentação dos empenhos da empresa."""
    cabecalho_generico = [
        ['Pregão','UASG','Data do Empenho','Valor Total','ÓRGÃO'],
        [10,8,20,10,30]
    ]
    abas = ['pendentes','encerrados']
    layout=[
        [
            sg.TabGroup(
                [[pt.aba_com_tabela_itens(cabecalho_generico,aba,aba) for aba in abas]
                ],enable_events=True,key='tg_empenho')
        ],
        [
            sg.Button('Registrar Empenho',enable_events=True,key='bt_registrar_empenho'),
        ],
        [pt.bt_voltar()]
        ]
    return sg.Window(title=titulo_janelas['janela_consulta_empenhos'], layout=layout, finalize=True)

def janela_consulta_reequilibrio():
    """Retorna um sg.Window com tabela e abas para apresentação dos pedidos de reequilíbrio econômico da empresa."""
    cabecalho_generico = [
        ['Pregão','UASG','Data do Pedido','Item','Valor Licitado','Novo Licitado'],
        [10,8,20,10,15,15]
    ]
    abas = ['pendentes','enviados','aceitos','recusados']
    layout=[
        [
            sg.TabGroup(
                [[pt.aba_com_tabela_itens(cabecalho_generico,aba,aba) for aba in abas]
                ],enable_events=True,key='tg_reequilibrio')
        ],
        [
            sg.Button('Registrar Envio',enable_events=True,key='bt_registrar_envio'),
            sg.Button('Registrar Aceite',enable_events=True,key='bt_registrar_aceite'),
            sg.Button('Registrar Recusa',enable_events=True,key='bt_registrar_recusa'),
        ],
        [pt.bt_voltar()]
        ]
    return sg.Window(title=titulo_janelas['janela_consulta_reequilibrio'], layout=layout, finalize=True)

def janela_consulta_carona():
    """Retorna um sg.Window com tabela e abas para apresentação dos pedidos de carona recebidos pela empresa."""
    cabecalho_generico = [
        ['Pregão','UASG','Data do Pedido','Item','Quantidade','Órgão Requerente'],
        [10,8,20,10,8,30]
    ]
    abas = ['aceitos','empenhados']
    layout=[
        [
            sg.TabGroup(
                [[pt.aba_com_tabela_itens(cabecalho_generico,aba,aba) for aba in abas]
                ],enable_events=True,key='tg_carona')
        ],
        [
            sg.Button('Registrar Carona',enable_events=True,key='bt_registrar_carona'),
        ],
        [pt.bt_voltar()]
        ]
    return sg.Window(title=titulo_janelas['janela_consulta_carona'], layout=layout, finalize=True)

def janela_consulta_atas():
    """Retorna um sg.Window com tabela e abas para apresentação dos pregões ganhos e atas assinadas."""
    cabecalho_generico = [
        ['Pregão','UASG','Data de Assinatura'],
        [10,8,20]
    ]
    abas = ['pendentes','assinadas']
    layout=[
        [
            sg.TabGroup(
                [[pt.aba_com_tabela_itens(cabecalho_generico,aba,aba) for aba in abas]
                ],enable_events=True,key='tg_atas')
        ],
        [
            sg.Button('Registrar assinatura de Ata',enable_events=True,key='bt_registrar_ata'),
        ],
        [pt.bt_voltar()]
        ]
    return sg.Window(title=titulo_janelas['janela_consulta_atas'], layout=layout, finalize=True)

###JANELAS DESTINADAS A CADASTROS

def janela_cadastro():
    """Retorna um sg.Window destinado a mostrar as opções de diferentes cadastros disponíveis."""
    layout = [[
            sg.Button('Planilha de Cotação',key='bt_cadastro_planilha',enable_events=True, size=(20,1))],
        [   sg.Button('Registrar Empenho',key='bt_cadastro_empenho',enable_events=True, size=(20,1))],
        [   sg.Button('Registrar Carona',key='bt_cadastro_carona',enable_events=True, size=(20,1))],
        [   sg.Button('Registrar Reequilíbrio',key='bt_cadastro_reequilibrio',enable_events=True, size=(20,1))],
        ]
    return sg.Window(titulo_janelas['janela_cadastro'], layout, finalize=True)

def janela_cadastro_homologacao(uasg:str,pregao:str,itens:list):
    """Retorna um sg.Window para homologação do pregão."""
    layout=[
        [
            sg.Text('Homologando o Pregão '),
            sg.Text(pregao,key='txt_pregao'),
            sg.Text(' do Uasg '),
            sg.Text(uasg,key='txt_uasg')
        ],
        [
            sg.Column(  layout=[[pt.frame_item_homologar(item[0],item[1],item[2])] for item in itens],
                        size=(400,600),scrollable=True, vertical_scroll_only=True)
        ],
        [
            sg.Button('Concluir',enable_events=True,key='bt_concluir'),
        ]
    ]
    return sg.Window(title=titulo_janelas['janela_cadastro_homologacao'],layout=layout,finalize=True)

def janela_cadastro_empenho():
    return

###JANELAS DESTINADAS AOS PROCESSOS DE AUTOMAÇÃO

def janela_comprasnet():
    """Retorna um sg.Window com botões para executar as principais automações."""
    layout = [[
            sg.Button('Cadastrar Pregão',key='bt_cadastrar',enable_events=True, size=(20,1))],
        [   sg.Button('Consultar Novidades',key='bt_consultar',enable_events=True, size=(20,1))],
        [   sg.Button('Participar de Disputa',key='bt_disputar',enable_events=True, size=(20,1))],
        ]
    return sg.Window(title=titulo_janelas['janela_comprasnet'], layout=layout, finalize=True)

###JANELAS AUXILIARES

def janela_consulta_pregao_alterar_fase(uasg:str,pregao:str,fases:list):
    """Retorna um sg.Window com um menu suspenso de opções para alterar a fase do pregão."""
    layout=[
        [
            sg.Text('Para o UASG '),
            sg.Text(uasg,key='txt_uasg'),
            sg.Text(' no pregão '),
            sg.Text(pregao,key='txt_pregao'),
        ],
        [
            sg.Text('Qual a nova fase do pregão?')
        ],
        [
            sg.Combo(values=fases,size=(20,1),key='cb_alterar_fase',enable_events=True)
        ],
        [
            sg.Button('Confirmar Alteração',key='bt_confirmar_fase')
        ]
    ]
    return sg.Window(title=titulo_janelas['janela_consulta_pregao_alterar_fase'],layout=layout,finalize=True)
