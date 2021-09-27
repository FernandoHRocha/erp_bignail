import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Text

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

def voltar():
    return sg.Button(button_text='Voltar',enable_events=True, key='bt_voltar',size=(10,1))

def tabelaItens(cabecalho,key,larguras,visible=True):
    return [[sg.Table(headings=cabecalho,values=cabecalho,enable_events=True,key=key,auto_size_columns=False,col_widths=larguras,visible=visible)]]

def comboEstadoPregao(key):
    return sg.Combo(values=['Proposta','Julgamento','Frustrado','Homologado','Adjudicado','Finalizado','Suspenso'],enable_events=True, key=key,size=(12,1))