import credentials
from database import connection as cnn
from tkinter import filedialog
import PySimpleGUI as sg
import openpyxl
import os
import adapter

def abrir_arquivo(initialdir = 'C:/Users/Licitacao/Desktop',filetypes=(('Arquivo','*.*'),)):
    return filedialog.askopenfilename(initialdir=initialdir,filetypes=filetypes)

def abrir_pasta(initialdir='C:/Users/Licitacao/Desktop'):
    return filedialog.askdirectory(initialdir=initialdir)

class Planilha:
    
    def __init__(self, caminho):
        while(True):
            try:
                self.planilha = openpyxl.load_workbook(caminho,data_only=True)
                break
            except:
                sg.popup('Confira se a planilha está aberta, caso esteja favor fechar.')
                self.planilha = openpyxl.load_workbook(caminho,data_only=True)
                break

    def obter_pregao(self):
        wb = self.planilha['Controle']
        pregao = {
            'numero' : adapter.padronizar_pregao(str(wb.cell(2,1).value)),
            'uasg' : adapter.padronizar_uasg(str(wb.cell(2,2).value)),
            'data' : adapter.padronizar_data_hora(str(wb.cell(2,3).value)[:10],str(wb.cell(2,4).value)[:5]),
            'orgao' : str(wb.cell(2,5).value).upper()
        }
        return pregao
    
    def obter_itens_cotados(self):
        wb = self.planilha['Planilha1']
        colunas_registro = [1,3,4,5,9,11,12,13,14]
        item = []
        for linha in range(2,wb.max_row):
            item.append([str(wb.cell(linha,coluna).value) for coluna in colunas_registro])
        return item

def renomear_arquivo(pasta:str, arquivo:str, nomenclatura:str):
    """Renomea arquivo de acordo com a nomenclatura inserida."""
    os.rename(pasta +'/'+ arquivo, pasta +'/'+ nomenclatura +'_'+ arquivo)

def mover_e_renomear_pasta(pasta:str,nomenclatura:str):
    local = '/'.join(pasta.split('/')[:-1])+'/'
    os.rename(pasta,local+nomenclatura)

def cadastrar_planilha():
    """Realiza a leitura da planilha de cotação, insere os dados em banco de dados e move a pasta para a pasta de pregões"""
    try:
        pasta = abrir_pasta()
        pasta_proposta = pasta+'\proposta'
        for arquivo in os.listdir(pasta_proposta):
            if arquivo.endswith('.xlsx'):
                arquivo_planilha = arquivo
            if arquivo.endswith('.docx'):
                arquivo_word = arquivo
    except:
        sg.popup('Não foi possível abrir o arquivo.')
        return
    
    planilha = Planilha(pasta_proposta+'/'+arquivo_planilha)
    pregao = planilha.obter_pregao()
    itens = planilha.obter_itens_cotados()
    if(cnn.consultar_id_orgao(pregao['uasg'])!='-1'):
        if not cnn.inserir_pregao(pregao['uasg'],pregao['numero'],pregao['data'],"Proposta"):
            sg.popup('O pregão já foi inserido anteriormente.')
            return
    else:
        cnn.inserir_orgao(pregao['uasg'],pregao['orgao'])
        cnn.inserir_pregao(pregao['uasg'],pregao['numero'],pregao['data'],"Proposta")

    for item in itens:
        cnn.inserir_itens_planilha(
            uasg = pregao['uasg'],
            pregao = pregao['numero'],
            item=item[0],
            marca=item[1],
            valor=item[2],
            quantidade=item[3],
            frete=item[4],
            categoria=item[5],
            modelo=item[6],
            fornecedor=item[7],
            preco_custo=item[8],
            )
    nomenclatura = adapter.padronizar_nome_pasta(pregao['data'],pregao['numero'],pregao['uasg'])
    renomear_arquivo(pasta_proposta, arquivo_planilha, nomenclatura)
    renomear_arquivo(pasta_proposta, arquivo_word, nomenclatura)
    mover_e_renomear_pasta(pasta,nomenclatura)
    sg.popup('Foram inseridos '+str(len(itens))+' itens no pregão de número '+pregao['numero'])
    return