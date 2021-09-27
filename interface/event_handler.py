from database import connection as cnn
from interface import windows as wds
import PySimpleGUI as sg
import time

def atualizar_lista_orgao():
    """Retorna do banco de dados uma lista com o nome dos órgãos registrados."""
    _orgao =[]
    for org in cnn.consulta_orgaos():
        _orgao.append(org[1])
    return _orgao

def abrir_janela_consulta_pregao(window):
    """Instancia a janela de consulta a pregões"""
    wds.janela_consulta_pregao()