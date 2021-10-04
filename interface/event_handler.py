from database import connection as cnn
from interface import windows as wds
import adapter
import credentials
import PySimpleGUI as sg
import time
import os

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
    window['tb_registrado'].update(values=cnn.consultar_itens_geral(orgao,pregao))

def lista_pregoes_gerais():
    """Retorna uma lista com a categoria dos pregões e a consulta ao banco de dados."""
    retorno =[]
    fases=cnn.consultar_fases_pregoes()
    for fase in fases:
        aux = [fase,cnn.consultar_pregoes_fase(fase)]
        retorno.append(aux)
    return retorno

def abrir_janela_alterar_fase_pregao(uasg:str,pregao:str):
    """Abre a janela para alteração de fase de pregão."""
    wds.janela_consulta_pregao_alterar_fase(uasg,pregao,cnn.consultar_fases_pregoes())

def atualizar_pregoes_gerais(window:sg.Window):
    """Refaz a consulta ao banco de dados para atualizar as tabelas de pregões."""
    window['tb_submeter'].update(values=cnn.consultar_pregoes_fase(1))
    window['tb_proposta'].update(values=cnn.consultar_pregoes_fase(1))
    window['tb_julgamento'].update(values=cnn.consultar_pregoes_fase(2))
    window['tb_ganhos'].update(values=cnn.consultar_pregoes_fase(4))
    window['tb_finalizados'].update(values=cnn.consultar_pregoes_fase(6))

def abrir_pasta_pregao(pregao:str,uasg:str,data:str):
    """Abre a pasta do pregão dentro do sistema."""
    while(True):##funções temporarias após consolidação do banco de dados não será necessário
        if(len(pregao)>=8):
            break
        else:
            pregao = '0'+pregao
    while(True):
        if(len(uasg)>=6):
            break
        else:
            pregao = '0' + uasg
    path = credentials.pasta
    data = data.replace('/','-')
    data = data[0:10]+'_'+pregao+'_'+uasg
    path += data
    try:
        os.startfile(os.path.realpath(path))
    except:
        sg.popup('Não foi possível encontrar a pasta.')

def abrir_janela_homologacao_itens(uasg:str, pregao:str):
    """Faz a chamada dos itens do pregão ao banco de dados e abre a janela de itens a homologar."""
    itens = cnn.consultar_itens_homologar(uasg, pregao)
    wds.janela_cadastro_homologacao(uasg,pregao,itens)

def confirmar_dados_homologacao_itens(uasg:str,pregao:str,values:dict):
    """Verifica e converte os valores dos itens para homologacao."""
    itens_homologar=[]
    for item in values.keys():
        if 'check' in item:
            if values[item]:
                codigo_item = item.replace('check_','')
                valor = values[str(item).replace('check','it')]
                if valor.replace(',','',1).isdigit():
                    aux = []
                    aux.append(codigo_item)
                    valor = str(round(float(valor.replace(',','.',1)),2))
                    if (len(valor.split('.')[1])<2):
                        valor = valor + '0'
                    aux.append(valor)
                    itens_homologar.append(aux)
                else:
                    return sg.popup('Favor corrigir o valor do item '+codigo_item)
    
    cnn.alterar_fase_pregao(uasg,pregao,'Homologado')
    for item in itens_homologar:
        cnn.inserir_item_ganho(uasg,pregao,item[0],item[1])
    return sg.popup('O pregão foi homologado.')

def abrir_janela_itens_empenhar(uasg:str,pregao:str):
    """Coleta as informações dos itens do pregão e chama a janela para empenho."""
    return wds.janela_cadastro_itens_empenhar(uasg,pregao,cnn.consultar_itens_empenhar(uasg,pregao))