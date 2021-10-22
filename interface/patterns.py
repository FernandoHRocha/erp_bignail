import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Checkbox, Text

def data(
        title:str='',
        key:str='fr_data',
        visible:bool=True,
        border_width:int=0,
        dia_padrao:str='',
        mes_padrao:str='',
        ano_padrao:str='2021'):
    """Retorna um sg.Frame com compos para inserção de datas.\n
    Os campos de dia, mês e ano possuem as chaves it_dia, it_mes e it_ano respectivamente.\n
    E os argumentos são referentes às propriedades do Frame."""
    anos = []
    for n in range(2020,2026): anos.append(str(n))
    return sg.Frame( layout=[
        [
            sg.Text('Dia'),
            sg.Input(default_text=dia_padrao,size=(4,1),enable_events=True,key='it_dia'),
            sg.Text('mês'),
            sg.Input(default_text=mes_padrao,size=(4,1),enable_events=True,key='it_mes'),
            sg.Text('ano'),
            sg.Input(default_text=ano_padrao,size=(5,1),enable_events=True,key='it_ano'),
        ],
    ],title=title,key=key,visible=visible,border_width=border_width)

def horario(title:str='',key:str='fr_horario',visible:bool=True,texto:str='Horário ',valor_inicial:str='',border_width:int=0):
    """Retorna um sg.Frame com compos para inserção de datas.\n
    Os campos de dia, mês e ano possuem as chaves it_dia, it_mes e it_ano respectivamente.\n
    E os argumentos são referentes às propriedades do Frame."""
    horarios = []
    for m in range(8,18):
        for n in [':00',':30']:
            hr = '0' + str(m) if len(str(m)) == 1 else str(m)
            horarios.append(str(hr+n))
    return sg.Frame( layout=[
        [
            sg.Text(texto),
            sg.Combo(default_value=valor_inicial,values=horarios,size=(5,1),enable_events=True,key='cb_horario',readonly=True),
        ],
    ],title=title,key=key,visible=visible,border_width=border_width)

def bt_voltar():
    """Retorna um sg.Button padronizado para navegação entre janelas."""
    return sg.Button(button_text='Voltar',enable_events=True, key='bt_voltar',size=(10,1))

def tabela_itens(cabecalho,key,larguras,visible=True):
    return [[sg.Table(headings=cabecalho,values=cabecalho,enable_events=True,key=key,auto_size_columns=False,col_widths=larguras,visible=visible)]]

def tabela_itens_preenchida(cabecalho,valores,key,larguras,visible=True):
    return [[sg.Table(headings=cabecalho,values=valores,enable_events=True,key=key,auto_size_columns=False,col_widths=larguras,visible=visible)]]

def combo_estado_pregao(key):
    return sg.Combo(values=['Proposta','Julgamento','Frustrado','Homologado','Adjudicado','Finalizado','Suspenso'],enable_events=True, key=key,size=(12,1))

def frame_pesquisa_por_pregao(orgaos:list):
    """Retorna uma sg.frame com a busca de pregão, informações e opções.\n
    O parametro deve ser uma lista com a primeira lista sendo dos códigos UASG, e a segunda o nome dos Órgãos."""
    return [
        sg.Frame(title=' Pesquisar por Órgão e Pregão ',layout=[
            [
                sg.Column(layout=[
                    [
                        sg.Text('UASG')
                    ],
                    [
                        sg.InputText(size=(10,1),key='it_uasg',enable_events=True)
                    ],
                    [
                        sg.Combo(values=orgaos[0],size=(8,1),enable_events=True,key='cb_uasg',readonly=True)
                    ]
                ]),
                sg.Column(layout=[
                    [
                        sg.Text('Órgão')
                    ],
                    [
                        sg.InputText(size=(82,1),key='it_orgao',enable_events=True)
                    ],
                    [
                        sg.Combo(values=orgaos[1],size=(80,1),key='cb_orgao',readonly=True,enable_events=True)
                    ],
                ]),
                sg.Column(layout=[
                    [
                        sg.Text('Pregão')
                    ],
                    [
                        sg.InputText(size=(14,1),key='it_pregao',enable_events=True)
                    ],
                    [
                        sg.Combo(values=[],size=(12,1),key='cb_pregao',readonly=True,enable_events=True)
                    ]
                ])
            ],
        ])
    ]

def frame_com_informacao_pregao():
    col1=(30,1)
    return[
        sg.Frame('',visible=False,border_width=0,key='fr_info_pregao',layout=[
            [
                sg.Text('',visible=False,key='txt_id_pregao')
            ],
            [
                sg.Column(layout=[
                    [sg.Text('Data da disputa de preços',size=col1,justification='center')],
                    [sg.Text('00/00/0000', key='txt_data_abertura',size=col1,justification='center')],
                    [sg.Text('Estado atual',size=col1,justification='center')],
                    [sg.Text('Julgamento', key='txt_julgamento',size=col1,justification='center')],
                ]),
                sg.Column(layout=[
                    [sg.Text('Itens homologados',size=col1,justification='center')],
                    [sg.Text('0', key='txt_itens_homologados',size=col1,justification='center')],
                    [sg.Text('Empenhos',size=col1,justification='center')],
                    [sg.Text('0', key='txt_empenhos',size=col1,justification='center')],
                ]),
                sg.Column(layout=[
                    [sg.Text('Valor total homologado',size=col1,justification='center')],
                    [sg.Text('0', key='txt_valor_homologado',size=col1,justification='center')],
                    [sg.Text('Valor total empenhado',size=col1,justification='center')],
                    [sg.Text('0', key='txt_valor_empenhado',size=col1,justification='center')],
                ]),
            ],
            [
                sg.Button(button_text='Abrir Pasta',key='bt_pasta'),
                sg.Button(button_text='Consultar Itens',key='bt_consultar_itens'),
            ]
        ])
    ]

def aba_com_tabela_itens(cabecalho:list, identificador:str, valores:list):
    """Retorna a sg.Tab contendo uma tabela.\n
    cabecalho - Contem uma lista com o nome das colunas e outra lista com a largura de cada coluna [[str],[int]].\n
    identificador - Str para identificar a guia (tab) e a tabela (tb).\n
    valores - conteudo para preencher a tabela, caso não seja passado nenhum valor, a tabela será preenchida com os valores do cabeçalho."""
    if(len(valores)<1):
        valores = []
    titulo = identificador[0].upper()+identificador[1:len(identificador)]
    return sg.Tab(titulo, tabela_itens_preenchida(cabecalho[0],valores,'tb_'+identificador,larguras=cabecalho[1]),key='tab_'+identificador,visible=True)

def frame_item_alterar(item:dict,marcas:list,categorias:list)->sg.Frame:
    size = (70,1)
    return sg.Frame(' Item '+item['item'],layout=[
        [
            sg.Checkbox('Atualizar item',enable_events=True,key='check_'+item['id_item']),
            sg.Text(item['id_item'],visible=False,key='txt_id_item_'+item['id_item'])
        ],
        [
            sg.Frame('',border_width=0,key='fr_it_'+item['id_item'],visible=False, layout=[
                [sg.Text('Item')],
                [sg.InputText(default_text=item['item'],size=size, enable_events=True, key='it_item_'+item['id_item'])],
                [sg.Text('Valor Ofertado')],
                [sg.InputText(default_text=item['valor_ofertado'],size=size, enable_events=True, key='it_valor_'+item['id_item'])],
                [sg.Text('Modelo')],
                [sg.InputText(default_text=item['modelo'],size=size, enable_events=True, key='it_modelo_'+item['id_item'])],
                [sg.Text('Marca')],
                [sg.Combo(readonly=True,default_value=item['nome_marca'],values=marcas,size=size, enable_events=True, key='cb_marca_'+item['id_item'])],
                [sg.Text('Categoria')],
                [sg.Combo(readonly=True,default_value=item['nome_categoria'],values=categorias,size=size, enable_events=True,key='cb_categoria_'+item['id_item'])],
                [sg.Text('Quantidade')],
                [sg.InputText(default_text=item['quantidade'],size=size, enable_events=True, key='it_quantidade_'+item['id_item'])],
                [sg.Text('Preço de Custo')],
                [sg.InputText(default_text=item['preco_custo'],size=size, enable_events=True, key='it_custo_'+item['id_item'])],
                [sg.Text('Fornecedor')],
                [sg.InputText(default_text=item['fornecedor'],size=size, enable_events=True, key='it_fornecedor_'+item['id_item'])],
            ]),
        ]
    ])


def frame_item_homologar(item:str,marca:str,modelo:str,unidades:str,valor_ofertado:str):
    """Retorna um sg.Frame para incluir itens em homologação."""
    item = str(item)
    modelo = str(modelo)
    unidades = str(unidades)
    valor_ofertado = str(valor_ofertado)
    return sg.Frame(title=' Item '+str(item)+' ',layout=
        [
            [
                sg.Checkbox(unidades+' un. '+marca+' do modelo: '+modelo,key='check_'+item,default=False,enable_events=True)
            ],
            [
                sg.Frame('',border_width=0,key='fr_it_'+item,visible=False, layout=[
                    [
                        sg.Text('Valor Ganhor R$'),
                        sg.InputText(default_text=valor_ofertado,size=(15,1), pad=(0,0),enable_events=True, key='it_'+item),
                        sg.Text('Valor Ofertado R$'),
                        sg.Text(valor_ofertado)
                    ]
                ]),
            ]
        ])

def frame_item_empenhar(itens:list):
    """Retorna um sg.Frame para incluir itens em nota de empenho."""
    item = str(itens[1])
    marca = str(itens[2])
    modelo = str(itens[3])
    unidades = str(itens[4])
    valor = str(itens[5]).replace('.',',')
    if(int(unidades)<1):
        return sg.Text()
    return sg.Frame(title=' Item '+str(item)+' ',layout=
        [
            [
                sg.Checkbox(marca+' - '+modelo,key='check_'+item,default=False,enable_events=True)
            ],
            [
                sg.Frame('',border_width=0,key='fr_it_'+item,visible=False,layout=[
                    [
                        sg.Text('Valor Ganhor R$'),
                        sg.InputText(default_text=valor,size=(12,1),enable_events=True,key='it_valor_'+item),
                        sg.Text('quantidade'),
                        sg.InputText(size=(6,1), enable_events=True, key='it_quantidade_'+item),
                        sg.Text('de'),
                        sg.Text(unidades,key='txt_quantidade_'+item),
                    ],
                ]),
            ]
        ])

def frame_item_reequilibrio(itens:list):
    """Retorna um sg.Frame para incluir itens em um pedido de reequilibrio economico."""
    item = str(itens[1])
    marca = str(itens[2])
    modelo = str(itens[3])
    unidades = str(itens[4])
    valor = str(itens[5]).replace('.',',')
    if(int(unidades)<1):
        return sg.Text()
    return sg.Frame(title=' Item '+str(item)+' ',layout=
        [
            [
                sg.Checkbox(unidades+' un. '+marca+' - '+modelo,key='check_'+item,default=False,enable_events=True)
            ],
            [
                sg.Frame('',border_width=0,key='fr_it_'+item,visible=False,layout=[
                    [
                        sg.Text('Disputado R$'),
                        sg.Text(valor),
                        sg.Text('Reequilibrio R$'),
                        sg.InputText(size=(12,1), enable_events=True, key='it_valor_'+item),
                        sg.Text(unidades,key='txt_quantidade_'+item),
                        sg.Text('unidades.'),
                    ],
                ]),
            ]
        ])

def botoes_concluir_cancelar_operacao(cancelar:str='Cancelar',concluir:str='Concluir'):
    """Retorna um array com dois sg.Button para finalizar operações com Cancelar e Concluir.\n
    Passando os parametros é possível alterar o nome exposto no botão, mas não suas chaves.\n
    As chaves são respectivamente: bt_cancelar e bt_concluir."""
    return [
        sg.Button(cancelar,enable_events=True,key='bt_cancelar',size=(20,1)),
        sg.Button(concluir,enable_events=True,key='bt_concluir',size=(20,1)),
    ]