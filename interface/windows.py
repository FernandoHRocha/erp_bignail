from tkinter import Scrollbar, Text
import PySimpleGUI as sg
from interface import patterns as pt
from interface import event_handler as evh
import adapter

titulo_janelas = {
    'janela_menu':'BigNail ERP',
    #menus principais
    'janela_consulta':'Consultas',
    'janela_cadastro':'Cadastros',
    'janela_comprasnet':'Compras Net',
    #consultas
    'janela_consulta_pregao':'Consulta de Processo Participado',
    'janela_consulta_pregoes':'Visão Geral dos processos',
    'janela_consulta_empenhos':'Notas de Empenhos',
    'janela_consulta_reequilibrio':'Pedidos de Reequilíbrio Econômico',
    'janela_consulta_carona':'Pedidos de Carona',
    'janela_consulta_atas':'Atas de Processos',
    'janela_consulta_itens_pregao':'Itens do pregão',
    #alterações
    'janela_alteracao_itens_participados':'Alteração dos Itens Cadastrados.',
    'janela_alteracao_data_abertura':'Alterar a Data de Abertura do Pregão.',
    #cadastros
    'janela_cadastro_homologacao':'Homologar Pregão',
    'janela_cadastro_itens_empenhar':'Empenhar itens',
    'janela_cadastro_itens_carona':'Cadastrar Carona de Itens',
    'janela_cadastro_entrega_empenho':'Registrar Entrega',
    'janela_cadastro_itens_reequilibrio':'Registrar Pedido de Reequilibrio Economico',
    #auxiliares
    'janela_consulta_pregao_alterar_fase':'Alteração de Fase',
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
        ]
    return sg.Window(title=titulo_janelas['janela_consulta'], layout=layout, finalize=True)

def janela_consulta_pregao():
    """Retorna um sg.Window contendo a busca geral de pregão."""
    orgaos = evh.consultar_uasg_orgao()
    layout=[
        [
            sg.Column(key='cl_info_pregao',layout=[
                [
                    sg.Frame('',layout=[
                            pt.frame_pesquisa_por_pregao(orgaos),
                            pt.frame_com_informacao_pregao(),
                    ]),
                ],
                [pt.bt_voltar()]
            ])
        ]
    ]
    return sg.Window(title=titulo_janelas['janela_consulta_pregao'], layout=layout, finalize=True)

def janela_consulta_pregoes():
    """Retorna um sg.Window com tabela e abas para apresentação dos pregões."""
    tamanho_padrao=(25,1)
    cabecalho_generico = [
        ['id','Pregão','UASG','Abertura','ÓRGÃO'],
        [0,10,8,20,30]
    ]
    abas = evh.listar_pregoes_gerais()
    coluna1=[#APLICADO PARA PREGÕES EM FASE DE PROPOSTA, JULGAMENTO E FRUSTRADO
        [sg.Button('Alterar Fase',enable_events=True,key='bt_alterar_fase',size=tamanho_padrao)],
        [sg.Button('Homologar Pregão',enable_events=True,key='bt_homologar',size=tamanho_padrao),]
    ]
    coluna2=[#APLICADO PARA PREGÕES HOMOLOGADOS
        [sg.Button('Registrar Empenho',enable_events=True,key='bt_registrar_empenho',size=tamanho_padrao)],
        [sg.Button('Registrar Carona',enable_events=True,key='bt_registrar_carona',size=tamanho_padrao)],
        [sg.Button('Registrar Reequilibrio',enable_events=True,key='bt_registrar_reequilibrio',size=tamanho_padrao),]
    ]
    layout=[
        [
            sg.TabGroup(
                [[pt.aba_com_tabela_itens(cabecalho_generico,aba[0],aba[1]) for aba in abas]
                ],enable_events=True,key='tg_pregoes')
        ],
        [
            sg.Frame(title=' Opções ',border_width=0,layout=
            [
                [sg.Button('Abrir Pasta',enable_events=True,key='bt_pasta',size=tamanho_padrao)],
                [sg.Button('Consultar Itens',enable_events=True,key='bt_consultar_itens',size=tamanho_padrao)],
                [sg.Button('Alterar Data Abertura',enable_events=True,key='bt_alterar_data',size=tamanho_padrao)],
                [
                    sg.Column(coluna1,key='cl_julgamento'),
                    sg.Column(coluna2,key='cl_ganho',visible=False),
                ]
            ])
        ],
        [pt.bt_voltar()]
        ]
    return sg.Window(title=titulo_janelas['janela_consulta_pregoes'],layout=layout,finalize=True)

def janela_consulta_empenhos():
    """Retorna um sg.Window com tabela e abas para apresentação dos empenhos da empresa."""
    cabecalho_generico = [
        ['id','Pregão','UASG','Nota','Data Empenho','Data Entrega','Valor Total'],
        [0,10,8,20,12,12,11]
    ]
    abas = evh.listar_empenhos_gerais()
    layout=[
        [
            sg.TabGroup(
                [[pt.aba_com_tabela_itens(cabecalho_generico,aba[0],aba[1]) for aba in abas]
                ],enable_events=True,key='tg_empenhos')
        ],
        [
            sg.Button('Abrir Pasta Pregão', enable_events=True,key='bt_pasta'),
            sg.Button('Consultar o Pregão', enable_events=True,key='bt_consultar_pregao'),
            sg.Button('Consultar os Itens',enable_events=True,key='bt_consultar_itens'),
            sg.Button('Registrar Entrega',enable_events=True,key='bt_registrar_entrega'),
        ],
        [pt.bt_voltar()]
        ]
    return sg.Window(title=titulo_janelas['janela_consulta_empenhos'], layout=layout, finalize=True)

def janela_consulta_reequilibrio():
    """Retorna um sg.Window com tabela e abas para apresentação dos pedidos de reequilíbrio econômico da empresa."""
    cabecalho_generico = [
        ['id','Pregão','UASG','Data do Pedido'],
        [0,10,8,20]
    ]
    abas = evh.listar_reequilibrios_gerais()
    layout=[
        [
            sg.TabGroup(
                [[pt.aba_com_tabela_itens(cabecalho_generico,aba[0],aba[1]) for aba in abas]
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
        ['id','Pregão','UASG','Data do Pedido','Órgão Requerente'],
        [0,10,8,20,30]
    ]
    abas = evh.listar_caronas_gerais()
    layout=[
        [
            sg.TabGroup(
                [[pt.aba_com_tabela_itens(cabecalho_generico,aba[0],aba[1]) for aba in abas]
                ],enable_events=True,key='tg_carona')
        ],
        [
            sg.Button('Abrir Pasta Pregão', enable_events=True,key='bt_pasta'),
            sg.Button('Consultar o Pregão', enable_events=True,key='bt_consultar_pregao'),
            sg.Button('Itens do Empenho',enable_events=True,key='bt_consultar_itens'),
            sg.Button('Registrar Empenho',enable_events=True,key='bt_empenho'),
        ],
        [pt.bt_voltar()]
        ]
    return sg.Window(title=titulo_janelas['janela_consulta_carona'], layout=layout, finalize=True)

def janela_consulta_itens_pregao(id_pregao:str):
    dados = evh.consultar_dados_pregao(id_pregao)
    pregao = adapter.adaptar_codigo_pregao(dados[1])
    uasg = dados[2]
    orgao = dados[3]
    data = dados[4]
    ata = dados[5] if dados[5] != None else 'Pendente'
    fase = dados[6]
    valor_custo = dados[7]
    valor_homologado = dados[8]
    valor_empenhado = dados[9]
    abas = evh.listar_itens_em_categorias(id_pregao)

    homologado = True if fase == 'Homologado' else False

    coluna1=sg.Column(size=(500,110),layout=[
        [
            sg.Text(id_pregao,key='txt_id_pregao',visible=False),
            sg.Text('Órgão:'),
            sg.Text(orgao,key='txt_orgao'),
        ],
        [
            sg.Text('Uasg:'),
            sg.Text(uasg,key='txt_uasg'),
        ],
        [
            sg.Text('Data Abertura: '),
            sg.Text(data,key='txt_data'),
        ],
        [
            sg.Text('Valor Homologado:',visible=homologado),
            sg.Text(valor_homologado,key='txt_homologado',visible=homologado),
        ]
    ])
    coluna2=sg.Column(size=(300,110),layout=[
        [
            sg.Text('Fase:'),
            sg.Text(fase,key='txt_fase'),
        ],
        [
            sg.Text('Data de Assinatura da Ata:'),
            sg.Text(ata,key='txt_ata'),
        ],
        [
            sg.Text('Valor Custo:'),
            sg.Text(valor_custo,key='txt_custo'),
        ],
        [
            sg.Text('Valor Empenhado:',visible=homologado),
            sg.Text(valor_empenhado,key='txt_empenhado',visible=homologado),
        ]
    ])
    layout=[
        [
            sg.Frame(title=' Consulta aos itens do pregão ' + pregao,key='fr_titulo_pregao',layout=[
                [
                    coluna1,
                    coluna2
                ]
            ]),
            sg.Column(layout=[
                [sg.Button('Abrir Pasta',enable_events=True,size=(20,1),key='bt_pasta')],
                [sg.Button('Registrar Empenho',enable_events=True,visible=homologado,size=(20,1),key='bt_item_empenho')],
                [sg.Button('Registrar Carona',enable_events=True,visible=homologado,size=(20,1),key='bt_item_carona')],
            ])
        ],
        [
            sg.Frame(title='',visible=True,key='fr_itens',layout=[
                [
                    sg.TabGroup([
                        [pt.aba_com_tabela_itens(aba[0],aba[1],aba[2]) for aba in abas]
                    ],enable_events=True,key='tg_itens')
                ]
            ])
        ],
        [
            sg.Button('Alterar item',enable_events=True,key='bt_item_alterar'),
            sg.Button('Solicitar Reequilibrio',visible=homologado,enable_events=True,key='bt_reequilibrio'),
            sg.Button('Consultar Fornecedor',enable_events=True,key='bt_fornecedor'),
        ],
        [pt.bt_voltar()]
    ]
    return sg.Window(title=titulo_janelas['janela_consulta_itens_pregao'],layout=layout,finalize=True)

###JANELAS DESTINADAS A ALTERAÇÕES

def janela_alteracao_itens_participados(id_pregao:str):#INCOMPLETO
    
    layout = [
        [

        ]
    ]
    return sg.Window(title=titulo_janelas['janela_alteracao_itens_participados'],layout=layout, finalize=True)

def janela_alteracao_data_abertura(dados:str):
    """Retorna um sg.Window com campos de data para alterar a data de abertura de um pregão."""
    id_pregao = dados[0]
    dia = dados[4][:2]
    mes = dados[4][3:5]
    ano = dados[4][6:10]
    horario = dados[4][11:]
    layout = [
        [
            sg.Text(id_pregao,key='txt_id_pregao',visible=False),
            pt.data('Qual a nova data do pregão?',dia_padrao=dia,mes_padrao=mes,ano_padrao=ano)
        ],
        [sg.Text('Abertura da disputa de lances:')],
        [pt.horario(valor_inicial=horario)],
        [pt.botoes_concluir_cancelar_operacao()]
    ]
    return sg.Window(title=titulo_janelas['janela_alteracao_data_abertura'],layout=layout,finalize=True)

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

def janela_cadastro_itens_reequilibrio(id_pregao:str):#INCOMPLETO
    """Retorna um sg.Window para registro dos itens que necessitam de pedido de reequilibrio econômico."""
    
    return

def janela_cadastro_homologacao(id_pregao:str,uasg:str,pregao:str,itens:list):
    """Retorna um sg.Window para homologação do pregão."""
    data_ata =[
        [
            sg.Text('Data de assinatura da ARP (Ata de Registro de Preços)\nDeixe em branco caso não tenha sido assinada.')
        ],
        [
            sg.Text('Dia'),sg.InputText('',size=(2,1),key='it_dia'),
            sg.Text('mês'),sg.InputText('',size=(2,1),key='it_mes'),
            sg.Text('ano'),sg.InputText('',size=(4,1),key='it_ano'),
        ]
    ]
    layout=[
        [
            sg.Text(id_pregao,key='txt_id_pregao',visible=False),
            sg.Text('Homologando o Pregão'),
            sg.Text(pregao,key='txt_pregao'),
            sg.Text('do Uasg'),
            sg.Text(uasg,key='txt_uasg')
        ],
        [
            sg.Text('Escolha os itens que foram homologados e coloque o valor disputado')
        ],
        [
            sg.Column(  layout=[[pt.frame_item_homologar(item[0],item[1],item[2], item[3], item[4])] for item in itens],
                        size=(600,400),vertical_scroll_only=True,scrollable=True,key='cl_itens')
        ],
        data_ata,
        pt.botoes_concluir_cancelar_operacao(),
    ]
    return sg.Window(title=titulo_janelas['janela_cadastro_homologacao'],layout=layout,finalize=True)

def janela_cadastro_itens_empenhar(uasg:str,pregao:str,itens:list):
    """Retorna um sg.Window para escolher os itens a serem empenhados."""
    numero_empenho =[
        [
            sg.Text(' Número do empenho '),sg.InputText('',size=(20,1),key='it_codigo_empenho'),
        ]
    ]
    dados_empenho=[
        [sg.Frame(title=' Data de Recebimento do Empenho ',layout=[[pt.data()]])],
        [sg.Frame(title=' Código da Nota de Empenho ',layout=numero_empenho)],
    ]
    layout=[
        [
            sg.Text('Registrar nota de empenho para o pregão '),
            sg.Text(pregao,key='txt_pregao'),
            sg.Text('do Uasg'),
            sg.Text(uasg,key='txt_uasg')
        ],
        [
            sg.Text('Escolha os itens que compõem a nota e indique a quantidade empenhada.')
        ],
        [
            sg.Column(  layout=[[pt.frame_item_empenhar(item)] for item in itens],
                        size=(600,400),vertical_scroll_only=True,scrollable=True,key='cl_itens')
        ],
        [
            dados_empenho
        ],
        pt.botoes_concluir_cancelar_operacao(),
    ]
    return sg.Window(title=titulo_janelas['janela_cadastro_itens_empenhar'],layout=layout,finalize=True)

def janela_cadastro_itens_carona(uasg:str,pregao:str,itens:list):
    """Retorna um sg.Window para escolher os itens a serem registrados em carona."""
    dados_carona =[
        [sg.Frame(title=' Data de Adesão a Carona ',layout=[[pt.data()]])]
    ]
    layout=[
        [
            sg.Text('Registrar Pedido de Carona para o pregão'),
            sg.Text(pregao,key='txt_pregao'),
            sg.Text('do Uasg'),
            sg.Text(uasg,key='txt_uasg')
        ],
        [
            sg.Text('Selecione o órgão que solicitou entrar de carona no pregão.')
        ],
        [
            sg.Combo(values=evh.consultar_uasg_orgao()[1],size=(100,1),enable_events=True,key='cb_orgao',readonly=True)
        ],
        [
            sg.Text('Selecione os itens aceitos na carona para servir ao órgão selecionado e indique a quantidade.')
        ],
        [
            sg.Column(  layout=[[pt.frame_item_empenhar(item)] for item in itens],
                        size=(600,400),vertical_scroll_only=True,scrollable=True,key='cl_itens')
        ],
        [
            sg.Text('Caso um mesmo órgão realize mais pedidos de carona para o mesmo pregão, considere datas diferentes para cada um.')
        ],
        dados_carona,
        pt.botoes_concluir_cancelar_operacao(),
    ]
    return sg.Window(title=titulo_janelas['janela_cadastro_itens_carona'],layout=layout,finalize=True)

def janela_cadastro_itens_reequilibrio(id_pregao:str,pregao:str,uasg:str,itens:list):
    layout = [
        [
            sg.Text(id_pregao,key='txt_id_pregao',visible=False),
            sg.Text('Registrar Pedido de Reequilibrio economico para o pregão '),
            sg.Text(pregao,key='txt_pregao'),
            sg.Text('do Uasg'),
            sg.Text(uasg,key='txt_uasg')
        ],
        [
            sg.Column(  layout=[[pt.frame_item_reequilibrio(item)] for item in itens],
                        size=(600,400),vertical_scroll_only=True,scrollable=True,key='cl_itens')
        ],
        [
            sg.Frame(title='Data de Solicitação do Pedido.',layout=[[pt.data()]])
        ],
        [pt.botoes_concluir_cancelar_operacao()]
    ]
    return sg.Window(title=titulo_janelas['janela_cadastro_itens_reequilibrio'], layout=layout,finalize=True)

def janela_cadastro_entrega_empenho(id_empenho:str):
    """Retorna um sg.Window com campos de data para registrar a entrega."""
    layout = [
        [
            sg.Text(id_empenho,key='txt_id_empenho',visible=False),
            pt.data('Em que data a entrega foi realizada?','entrega_empenho',True)
        ],
        [
            pt.botoes_concluir_cancelar_operacao(concluir='Registrar')
        ]
    ]
    return sg.Window(title=titulo_janelas['janela_cadastro_entrega_empenho'],layout=layout,finalize=True)
    
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
