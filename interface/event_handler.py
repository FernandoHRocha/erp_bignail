from database import connection as cnn
from interface import windows as wds
import PySimpleGUI as sg
import time

def atualizar_lista_orgao():
    """Retorna do banco de dados uma lista com o nome dos órgãos registrados."""
    _orgao =[]
    for org in cnn.consulta_orgaos():
        _orgao.append(org[0])
    return _orgao


def escolher_orgao(window:sg.Window, orgao:str):
    """Preenche um combo box com os pregões participados pelo órgão indicado."""
    window['fr_pregao'].update(visible=True)
    for org in cnn.consulta_orgaos():
        if org[0] == orgao:
            window['txt_uasg'].update(value=org[1])
            window['cb_pregao'].update(values=cnn.consulta_pregoes(org[1]),visible=True)
            break

def apresentar_itens_pregao(window:sg.Window, orgao:str, pregao:str):
    """Preenche um combo box com os pregões participados pelo órgão indicado."""
    window['fr_itens_participados'].update(visible=True)
    for org in cnn.consulta_orgaos():
        if org[0] == orgao:
            orgao = org[1]
            break
    itens = cnn.consultar_itens_geral(orgao,pregao)
    window['tb_geral'].update(values=itens)
