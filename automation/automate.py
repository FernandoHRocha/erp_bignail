import credentials as aui
from automation import archive_handler as arh
from database import connection as cnn
from tkinter import filedialog
import PySimpleGUI as sg
import datetime
import openpyxl
import os

def cadastrar_planilha(renomear:bool):
    """Lê os dados da planilha, cadastra o pregão e os itens no banco de dados, renomeia pasta e arquivos."""
    arh.cadastrar_planilha(renomear)

def cadastrar_pregao():
    """Cadastra os itens do pregão para participação no site ComprasNet."""
    sg.popup('Favor encontrar a planilha de cotação.')
    planilha = arh.abrir_arquivo()
    if(planilha == ''):
        return
    sg.popup('Favor encontrar a proposta a ser enviada.')
    proposta = arh.abrir_arquivo()
    if(proposta == ''):
        return
    sg.popup('Favor encontrar a documentação.')
    documentacao = arh.abrir_arquivo()
    if(documentacao == ''):
        return