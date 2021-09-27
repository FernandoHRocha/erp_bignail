import credentials as aui
from database import connection as cnn
from tkinter import filedialog
import PySimpleGUI as sg
from datetime import datetime
import openpyxl
import os
import adapter

def abrir_arquivo(initialdir = 'C:/Users/Licitacao/Desktop',filetypes=(('Arquivo','*.*'),)):
    return filedialog.askopenfilename(initialdir=initialdir,filetypes=filetypes)

def abrir_pasta(initialdir='C:/Users/Licitacao/Desktop'):
    return filedialog.askdirectory(initialdir=initialdir)

class Planilha:
    
    def __init__(self, caminho):
        self.planilha = openpyxl.load_workbook(caminho,data_only=True)

    def obter_pregao(self):
        wb = self.planilha['Controle']
        pregao = []
        pregao.append(adapter.padronizar_pregao(str(wb.cell(2,1).value)))
        pregao.append(adapter.padronizar_uasg(str(wb.cell(2,2).value)))
        pregao.append(adapter.padronizar_data_hora(str(wb.cell(2,3).value)[:10],str(wb.cell(2,4).value)[:5]))
        pregao.append(str(wb.cell(2,5).value).upper())
        return pregao
    
    def obter_itens_cotados(self):
        wb = self.planilha['Planilha1']
        colunas_registro = [1,3,4,5,9,11,12,13,14]
        item = []
        for linha in range(2,wb.max_row):
            item.append([str(wb.cell(linha,coluna).value) for coluna in colunas_registro])
        return item

class Operacoes:
    
    def cadastrar_planilha(self):
        try:
            pasta = abrir_pasta()
            for arquivo in os.listdir(pasta):
                if arquivo.endswith('.xlsx'):
                    arquivo_planilha = arquivo
                if arquivo.endswith('.docx'):
                    arquivo_word = arquivo
        except:
            sg.popup('Não foi possível abrir o arquivo.')
            return
        planilha = Planilha(pasta+'/'+arquivo_planilha)
        pregao = planilha.obter_pregao()
        itens = planilha.obter_itens_cotados()
        print(pregao)
        #if(pregao[3] != ''):
        #    cnn.inserir_orgao(uasg=pregao[1],orgao=pregao[3])
        #cnn.inserir_pregao(uasg = pregao[1], numero=pregao[0], data=pregao[2],fase='Proposta')
        for item in itens:
            print (item)
            # cnn.inserir_items_planilha(
            #     uasg = pregao[1],
            #     pregao = pregao[0],
            #     item=item[0],
            #     marca=item[1],
            #     valor=item[2],
            #     quantidade=item[3],
            #     frete=item[4],
            #     categoria=item[5],
            #     modelo=item[6],
            #     fornecedor=item[7],
            #     preco_custo=item[8],
            #     )
        nomenclatura = adapter.padronizar_nome_pasta(pregao[2],pregao[0],pregao[1])
        renomear_arquivo(pasta, arquivo_planilha, nomenclatura)
        renomear_arquivo(pasta, arquivo_word, nomenclatura)
        sg.popup('Foram inseridos '+str(len(itens))+' itens no pregão de número '+pregao[0])
        return

def renomear_arquivo(pasta:str, arquivo:str, nomenclatura:str):
    """Renomea arquivo de acordo com a nomenclatura inserida."""
    os.rename(pasta +'/'+ arquivo, pasta +'/'+ nomenclatura +'_'+ arquivo)