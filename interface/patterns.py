import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Checkbox, Text

def data(title,key,visible):
    horas = ['08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30']
    anos = []
    for n in range(2021,2026): anos.append(str(n))
    return sg.Frame( layout=[
        [
            sg.Text('Dia '),
            sg.Input(size=(4,1),enable_events=True,key='it_dia'),
            sg.Text(' do mês de '),
            sg.Input(size=(4,1),enable_events=True,key='it_mes'),
            sg.Text(' no ano de '),
            sg.Input(size=(5,1),enable_events=True,key='it_ano'),
            sg.Text(' às '),
            sg.Combo(values=horas,size=(6,1),enable_events=True,key='cb_hora',readonly=True),
        ],
        ],
        title=title,key=key,visible=visible,border_width=0)

def bt_voltar():
    """Retorna um sg.Button padronizado para navegação entre janelas."""
    return sg.Button(button_text='Voltar',enable_events=True, key='bt_voltar',size=(10,1))

def tabela_itens(cabecalho,key,larguras,visible=True):
    return [[sg.Table(headings=cabecalho,values=cabecalho,enable_events=True,key=key,auto_size_columns=False,col_widths=larguras,visible=visible)]]

def tabela_itens_preenchida(cabecalho,valores,key,larguras,visible=True):
    if valores:
        return [[sg.Table(headings=cabecalho,values=valores,enable_events=True,key=key,auto_size_columns=False,col_widths=larguras,visible=visible)]]

def combo_estado_pregao(key):
    return sg.Combo(values=['Proposta','Julgamento','Frustrado','Homologado','Adjudicado','Finalizado','Suspenso'],enable_events=True, key=key,size=(12,1))

def frame_orgaos_pregao(orgaos):
    """Retorna uma sg.frame com dois rótulos e duas caixas combo,
    referente aos órgãos registrados (lista que deve ser passada
    como parametro) e outra aos pregões."""
    return [sg.Frame(title='',layout=[
            [sg.Text('Órgão: ',(10,1),key='txt_uasg'),
            sg.Combo(values=orgaos,size=(60,1),enable_events=True,key='cb_orgao',readonly=True)]
            ]),
        sg.Frame(title='',key='fr_pregao',visible=False,layout=[
            [sg.Text(' Pregão: ',(10,1)),
            sg.Combo(values=[],size=(10,1),enable_events=True,key='cb_pregao',readonly=True)]
            ])]

def aba_com_tabela_itens(cabecalho:list, texto:str, valores:list):
    """Retorna a sg.Tab contendo uma tabela."""
    if(len(valores)<1): valores = cabecalho
    titulo = texto[0].upper()+texto[1:len(texto)]
    return sg.Tab(titulo, tabela_itens_preenchida(cabecalho[0],valores,'tb_'+texto,larguras=cabecalho[1]),key='tab_'+texto,visible=True)

def frame_item_homologar(item:str,modelo:str,unidades:str):
    """Retorna um sg.Frame para incluir itens em homologação."""
    item = str(item)
    modelo = str(modelo)
    unidades = str(unidades)
    return sg.Frame(title=' Item '+str(item)+' ',layout=
        [
            [
                sg.Checkbox(unidades+' un. do modelo: '+modelo,key='check_'+item,default=False,enable_events=True)
            ],
            [
                sg.Frame('',border_width=0,key='fr_it_'+item,visible=False,layout=[
                    [
                        sg.Text('Valor Ganhor R$'),
                        sg.InputText(size=(15,1), enable_events=True, key='it_'+item)
                    ]
                ]),
            ]
        ])

def frame_item_empenhar(itens:list):
    """Retorna um sg.Frame para incluir itens em nota de empenho."""
    item = str(itens[0])
    marca = str(itens[1])
    modelo = str(itens[2])
    unidades = str(itens[3])
    valor = str(itens[4]).replace('.',',')
    return sg.Frame(title=' Item '+str(item)+' ',layout=
        [
            [
                sg.Checkbox(marca+' - '+modelo,key='check_'+item,default=False,enable_events=True)
            ],
            [
                sg.Frame('',border_width=0,key='fr_it_'+item,visible=False,layout=[
                    [
                        sg.Text('Valor Ganhor R$'),
                        sg.Text(valor),
                    ],
                    [
                        sg.InputText(size=(6,1), enable_events=True, key='it_'+item),
                        sg.Text(' de '),
                        sg.Text(unidades,key='txt_quantidade_'+item),
                        sg.Text(' unidades.'),
                    ],
                ]),
            ]
        ])

def botos_concluir_cancelar_operacao():
    """Retorna um array com dois sg.Button para finalizar operações com Cancelar e Concluir."""
    return [
        sg.Button('Cancelar',enable_events=True,key='bt_cancelar',size=(20,1)),
        sg.Button('Concluir',enable_events=True,key='bt_concluir',size=(20,1)),
    ]