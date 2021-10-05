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
    window['tb_ganho'].update(values=cnn.consultar_itens_ganhos(orgao,pregao))

def lista_pregoes_gerais():
    """Retorna uma lista com a categoria dos pregões e os respectivos dados."""
    retorno =[]
    fases=cnn.consultar_fases_pregoes()
    for fase in fases:
        aux = [fase,cnn.consultar_pregoes_fase(fase)]
        retorno.append(aux)
    return retorno

def lista_empenhos_gerais():
    """Retorna uma lista com a categoria dos empenhos e os respectivos empenhos."""
    retorno=[]
    fases = cnn.consultar_fases_empenhos()
    for fase in fases:
        aux = [fase,cnn.consultar_empenhos_fase(fase)]
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
    return wds.janela_cadastro_itens_empenhar(uasg,pregao,cnn.consultar_itens_homologados(uasg,pregao))

def empenhar_itens(window:sg.Window,values:list):
    """Valida dados dos itens, data, e insere ao banco de dados."""
    dia = str(adapter.conferir_se_inteiro_e_menor(values['it_dia'],31))
    mes =  str(adapter.conferir_se_inteiro_e_menor(values['it_mes'],12))
    ano = str(adapter.conferir_se_inteiro_e_menor(values['it_ano'],2040))
    nota_empenho = values['it_codigo_empenho']
    uasg = window['txt_uasg'].get()
    pregao = window['txt_pregao'].get()
    data_empenho = dia+'-'+mes+'-'+ano
    if str(False) in data_empenho:
        return sg.popup('Favor corrigir a data do empenho.')
    itens_homologar=[]
    for item in values.keys():
        if 'check' in item:
            if values[item]:
                codigo_item = item.replace('check_','')
                quantidade = values[str(item).replace('check','it')]
                quantidade_max = window[str(item).replace('check','txt_quantidade')].get()
                valor = values[str(item).replace('check','it_valor')]
                aux = []
                aux.append(codigo_item)
                if quantidade.isdigit():
                    if (int(quantidade_max) < int(quantidade) or int(quantidade) < 1):
                        return sg.popup('Verifique a quantidade para o item '+codigo_item)
                    aux.append(quantidade)
                if valor.replace(',','',1).isdigit():
                    valor = str(round(float(valor.replace(',','.',1)),2))
                    if (len(valor.split('.')[1])<2):
                        valor = valor + '0'
                    aux.append(valor)
                else:
                    return sg.popup('Favor corrigir o valor do item '+codigo_item)
                itens_homologar.append(aux)
    else:
        if(len(itens_homologar)<1):
            sg.popup('Para registrar um empenho é necessário que pelo menos um item seja empenhado.')
        else:
            if (not cnn.inserir_empenho_solicitado(uasg,pregao,data_empenho,nota_empenho)):
                sg.popup('Não foi possível registrar o empenho.')
            else:
                if(not cnn.inserir_itens_em_empenho(uasg,pregao,nota_empenho,itens_homologar)):
                    sg.popup('Houve um problema para registrar os itens do empenho.')
                else:
                    sg.popup('Empenho registrado com sucesso!')
                    window.Close()

def abrir_janela_itens_carona(uasg:str,pregao:str):
    """Coleta as informações dos itens do pregão e chama a janela para carona."""
    return wds.janela_cadastro_itens_carona(uasg,pregao,cnn.consultar_itens_homologados(uasg,pregao))

def caronar_itens(window:sg.Window,values:list):
    """Valida dados dos itens, data, e insere ao banco de dados."""
    dia = str(adapter.conferir_se_inteiro_e_menor(values['it_dia'],31))
    mes =  str(adapter.conferir_se_inteiro_e_menor(values['it_mes'],12))
    ano = str(adapter.conferir_se_inteiro_e_menor(values['it_ano'],2040))
    uasg = window['txt_uasg'].get()
    pregao = window['txt_pregao'].get()
    orgao = values['cb_orgao']
    data_carona = dia+'-'+mes+'-'+ano
    if str(False) in data_carona:
        return sg.popup('Favor corrigir a data do empenho.')
    itens_caronar=[]
    for item in values.keys():
        if 'check' in item:
            if values[item]:
                codigo_item = item.replace('check_','')
                quantidade = values[str(item).replace('check','it')]
                quantidade_max = window[str(item).replace('check','txt_quantidade')].get()
                valor = values[str(item).replace('check','it_valor')]
                aux = []
                aux.append(codigo_item)
                if quantidade.isdigit():
                    if (int(quantidade_max) < int(quantidade) or int(quantidade) < 1):
                        return sg.popup('Verifique a quantidade para o item '+codigo_item)
                    aux.append(quantidade)
                if valor.replace(',','',1).isdigit():
                    valor = str(round(float(valor.replace(',','.',1)),2))
                    if (len(valor.split('.')[1])<2):
                        valor = valor + '0'
                    aux.append(valor)
                else:
                    return sg.popup('Favor corrigir o valor do item '+codigo_item)
                itens_caronar.append(aux)
    else:
        if(len(itens_caronar)<1):
            sg.popup('Para registrar um empenho é necessário que pelo menos um item seja empenhado.')
        else:
            if (not cnn.inserir_carona(uasg,pregao,data_carona,orgao)):
                sg.popup('Não foi possível registrar o empenho.')
            else:
                if(not cnn.inserir_itens_em_empenho(uasg,pregao,itens_caronar)):
                    sg.popup('Houve um problema para registrar os itens do empenho.')
                else:
                    sg.popup('Empenho registrado com sucesso!')
                    window.Close()