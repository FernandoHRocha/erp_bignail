from database import connection as cnn
from interface import windows as wds
from subprocess import check_call
import adapter
import credentials
import PySimpleGUI as sg
import time
import os

def voltar_pagina(historico:list,menu)->list:
    """Retorna a aplicação para a página vista anteriormente."""
    try:
        if len(historico)>0:
            voltar = historico.pop()
            voltar()
            return historico
    except:
        menu()
        return [menu]

def copiar_para_area_transferencia(texto:str):
    """Passa o argumento para a area de transferência."""
    cmd='echo '+texto.strip()+'|clip'
    return check_call(cmd,shell=True)

def alterar_apresentacao_item(window:sg.Window,values:dict,event:str):
    """Atualiza a apresentação de itens com checkbox marcados ou desmarcados."""
    frame_input = str(event).replace('check_','fr_it_')
    window[frame_input].update(visible=True)
    window[frame_input].unhide_row() if values[event] else window[frame_input].hide_row()
    window.refresh()
    window['cl_itens'].contents_changed()

def conferir_campos_de_data(values:dict):
    """Retorna uma string com a data se os campos forem válidados com sucesso, caso contrátio retorna False."""
    dia = str(adapter.conferir_se_inteiro_e_menor(values['it_dia'],31))
    mes =  str(adapter.conferir_se_inteiro_e_menor(values['it_mes'],12))
    ano = str(adapter.conferir_se_inteiro_e_menor(values['it_ano'],2040))
    data = dia+'-'+mes+'-'+ano
    return False if str(False) in data else data

def conferir_campo_de_hora(values:dict):
    """Retorna uma string com o horário selecionado, caso nenhum seja selecionado, retorna False"""
    horario = str(values['cb_horario'])
    return False if horario == '' else horario

def consultar_dados_selecionados_tabela(window:sg.Window, values:dict,tab_group:str, msg_erro:str='Favor selecionar um pregão.'):
    """Retorna os dados da linha selecionada.\n
    Encontra qual a guia aberta, e recupera os dados selecionados para aquela guia somente.\n
    tab_group é o nome da guia e será utilizada para encontrar a tabela com os valores.\n
    Caso nenhum pregão esteja selecionado retorna False e um sg.popup(msg_erro) é mostrado.\n
    msg_erro - Str com a mensagem que deve aparecer caso nenhum pregão seja selecionado,
    não passando esse parametro será considerada uma frase padrão."""
    tab = str(values[tab_group]).replace('tab','tb')
    if (len(values[tab])>0):
        return [window[tab].get()[linha] for linha in values[tab]]
    else:
        sg.popup(msg_erro)
        return False

def consultar_dados_pregao(id_pregao:str):
    return cnn.consultar_dados_pregao(id_pregao)

def consultar_uasg_orgao():
    """Retorna do banco de dados uma lista com o nome dos órgãos registrados."""
    return [cnn.consultar_todos_uasgs(),cnn.consultar_todos_orgaos()]

def listar_pregoes_gerais():
    """Retorna uma lista com a categoria dos pregões e os respectivos dados."""
    retorno =[]
    fases=cnn.consultar_fases_pregoes()
    for fase in fases:
        aux = [fase,cnn.consultar_pregoes_fase(fase)]
        retorno.append(aux)
    return retorno

def listar_empenhos_gerais():
    """Retorna uma lista com a categoria dos empenhos e os respectivos empenhos."""
    retorno=[]
    fases = cnn.consultar_fases_empenhos()
    for fase in fases:
        aux = [fase,cnn.consultar_empenhos_pela_fase(fase)]
        retorno.append(aux)
    return retorno

def listar_caronas_gerais():
    """Retorna uma lista com a categoria das caronas e os respectivos pedidos."""
    retorno=[]
    fases = cnn.consultar_fases_carona()
    for fase in fases:
        aux = [fase,cnn.consultar_caronas_pela_fase(fase)]
        retorno.append(aux)
    return retorno

def listar_reequilibrios_gerais():
    """Retorna uma lista com a categoria dos reequilibrios e os pedidos."""
    retorno = []
    fases = cnn.consultar_fases_reequilibrio()
    for fase in fases:
        aux = [fase,cnn.consultar_reequilibrios_pela_fase(fase)]
        retorno.append(aux)
    return retorno

def abrir_janela_alterar_fase_pregao(uasg:str,pregao:str):
    """Abre a janela para alteração de fase de pregão."""
    wds.janela_consulta_pregao_alterar_fase(uasg,pregao,cnn.consultar_fases_pregoes())

def listar_itens_em_categorias(id_pregao:str):#incompleto
    """Retorna os dados necessários para apresentar os itens do pregão em suas categorias."""
    cabecalho_participados =    [
        ['id','Item','Marca','Modelo','Quant','Preço','Custo','Frete','Preço Min','Fornecedor'],
        [0,5,15,20,5,12,12,8,12,20]]
    cabecalho_homologados =  [
        ['id','Item','Marca','Modelo','Preço','Quant','Empenho','Carona'],
        [0,5,15,20,12,5,7,5]]
    cabecalho_empenhos =    [
        ['id','Item','Marca','Modelo','Quant','Preço','Custo','Data Empenho','Data Entrega','Nota','Fase'],
        [0,5,15,20,5,12,12,12,12,10,12]]
    cabecalho_caronas =     [
        ['id','Item','Marca','Modelo','Quant','Empenhado','Preço','Data','Órgão','Fase'],
        [0,5,15,20,9,9,12,10,30]]
    cabecalho_reequilibrios =   [
        ['Item','Marca','Modelo','Quant','Preço','Novo Preço','Data','Fase','id'],
        [5,15,20,5,12,12,10,12,0]]
    return [
        [cabecalho_participados,'participados',cnn.consultar_itens_participados(id_pregao)],
        [cabecalho_homologados,'homologados',cnn.consultar_itens_homologados_id(id_pregao)],
        [cabecalho_empenhos,'empenhados',cnn.consultar_itens_empenhados_id(id_pregao)],
        [cabecalho_caronas,'caronas',cnn.consultar_itens_carona(id_pregao)],
        #[cabecalho_reequilibrio,'reequilibros',],##cnn.(id_pregao)],
    ]

def abrir_pasta_pregao(id_pregao:str):
    """Abre a pasta do pregão dentro do sistema."""
    path = credentials.pasta+cnn.consultar_pasta_pregao(id_pregao)
    try:
        os.startfile(os.path.realpath(path))
    except:
        sg.popup('Não foi possível encontrar a pasta.')

##JANELA DE PROCURA POR PREGÃO

def limpar_entradas_procura_pregao(window,entradas:list):
    """Esvazia as entradas de dados que não estão sendo utilizadas"""
    [window[entrada].update(value='') for entrada in entradas]

def procurar_pelo_uasg(uasg:str,window):
    """Procura e atualiza o combobox com os uasgs que condizem com o parametro entrada."""
    if uasg:
        limpar_entradas_procura_pregao(window,['it_orgao','it_pregao'])
        window['cb_uasg'].update(values=cnn.procurar_uasg(uasg))

def procurar_pelo_orgao(orgao:str,window):
    if orgao:
        limpar_entradas_procura_pregao(window,['it_uasg','it_pregao'])
        valor = cnn.procurar_orgao(orgao)
        window['cb_orgao'].update(values=valor)

def procurar_pelo_pregao(pregao:str,uasg:str,window):
    if pregao and uasg:
        limpar_entradas_procura_pregao(window,['it_uasg','it_orgao'])
        valor = cnn.procurar_pregoes(pregao,uasg)
        window['cb_pregao'].update(values=valor)
    else:
        window['it_pregao'].update(value='')

def atualizar_orgao_pelo_uasg(uasg:str,window):
    """Procura e atualiza o órgão pelo seu código uasg."""
    if uasg:
        window['cb_orgao'].update(value=cnn.procurar_orgao_com_uasg(uasg))
        atualizar_lista_pregoes(cnn.consultar_id_orgao(uasg),window)

def atualizar_uasg_pelo_orgao(orgao:str,window):
    """Procura e atualiza o uasg pelo nome do órgão."""
    if orgao:
        uasg = cnn.procurar_uasg_com_nome_orgao(orgao)
        window['cb_uasg'].update(value=uasg)
        atualizar_lista_pregoes(cnn.consultar_id_orgao(uasg),window)

def atualizar_lista_pregoes(id_orgao:str,window):
    """Procura e atualiza o combobox dos pregões registrados para determinado órgão."""
    window['cb_pregao'].update(values=cnn.consultar_pregoes_do_orgao(id_orgao))

def mostrar_frame_informacoes_opcoes(window, mostrar:bool=True):
    """Esconde ou mostra (dependendo do parametro de entrada) as frames de informções de um pregão."""
    window['fr_info_pregao'].update(visible=True)
    window['fr_info_pregao'].unhide_row() if mostrar else window['fr_info_pregao'].hide_row()

def atualizar_informacoes_pregao(uasg:str,pregao:str,window):
    """Atualiza as informações gerais a cerca de um pregão para apresenta-lo na busca."""
    id = cnn.consultar_id_pregao(uasg,pregao)
    infos = cnn.consultar_dados_gerais_pregao(id)
    window['txt_id_pregao'].update(value=id)
    window['txt_data_abertura'].update(value=infos[0])
    window['txt_julgamento'].update(value=infos[1])
    window['txt_itens_homologados'].update(value=infos[2])
    window['txt_empenhos'].update(value=infos[4])
    window['txt_valor_homologado'].update(value=infos[3])
    window['txt_valor_empenhado'].update(value=infos[5])

##JANELA HOMOLOGAÇÃO DE ITENS

def abrir_janela_homologacao_itens(id_pregao:str):
    """Faz a chamada dos itens do pregão ao banco de dados e abre a janela de itens a homologar."""
    dados = consultar_dados_pregao(id_pregao)
    uasg = dados[2]
    pregao = dados[1]
    wds.janela_cadastro_homologacao(id_pregao,uasg,pregao,cnn.consultar_itens_homologar(id_pregao))

def homologar_pregao_e_itens(window:sg.Window,values:dict):
    """Verifica e converte os valores dos itens para homologacao."""
    window.BringToFront()
    id_pregao = window['txt_id_pregao'].get()
    uasg = window['txt_uasg'].get()
    pregao = window['txt_pregao'].get()
    data_ata = conferir_campos_de_data(values)
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
    else:
        if(len(itens_homologar)<1):
            return sg.popup('Para homologar um pregão é necessário que pelo menos um item seja empenhado.')
        if not cnn.alterar_fase_pregao(uasg,pregao,'Homologado'):
            return sg.popup('Não foi possível alterar a fase do pregão.')
        if data_ata != False:
            if not cnn.alterar_data_arp(id_pregao,data_ata):
                sg.popup('Será necessário inserir a data de assinatura posteriormente.')
        if not cnn.inserir_itens_ganho(uasg,pregao,itens_homologar):
            return sg.popup('Não foi possível inserir os itens como homologados.')
        sg.popup('O pregão foi homologado.')

##JANELA EMPENHO DE ITENS

def abrir_janela_itens_empenhar(id_pregao:str):
    """Coleta as informações dos itens do pregão e chama a janela para empenho."""
    dados = consultar_dados_pregao(id_pregao)
    uasg = dados[2]
    pregao = dados[1]
    return wds.janela_cadastro_itens_empenhar(uasg,pregao,cnn.consultar_itens_homologados(id_pregao))

def empenhar_itens(window:sg.Window,values:list):
    """Valida dados dos itens, data, e insere ao banco de dados."""
    window.BringToFront()
    nota_empenho = values['it_codigo_empenho']
    uasg = window['txt_uasg'].get()
    pregao = window['txt_pregao'].get()
    data_empenho = conferir_campos_de_data(values)
    if not data_empenho:
        return sg.popup('Favor corrigir a data do empenho.')
    itens_homologar=[]
    for item in values.keys():
        if 'check' in item:
            if values[item]:
                codigo_item = item.replace('check_','')
                quantidade = values[str(item).replace('check','it_quantidade')]
                quantidade_max = window[str(item).replace('check','txt_quantidade')].get()
                valor = values[str(item).replace('check','it_valor')]
                aux = []
                aux.append(codigo_item)
                if (not quantidade.isdigit()) or (int(quantidade_max) < int(quantidade) or int(quantidade) < 1):
                    return sg.popup('Verifique a quantidade para o item '+codigo_item)
                else:
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
            return sg.popup('Para registrar um empenho é necessário que pelo menos um item seja empenhado.')
        else:
            if (not cnn.inserir_empenho(uasg,pregao,data_empenho,nota_empenho)):
                return sg.popup('Não foi possível registrar o empenho.')
            else:
                if(not cnn.inserir_itens_em_empenho(uasg,pregao,nota_empenho,itens_homologar)):
                    return sg.popup('Houve um problema para registrar os itens do empenho.')
                else:
                    sg.popup('Empenho registrado com sucesso!')

##JANELA CARONA DE ITENS

def abrir_janela_itens_carona(id_pregao:str):
    """Coleta as informações dos itens do pregão e chama a janela para carona."""
    dados = consultar_dados_pregao(id_pregao)
    uasg = dados[2]
    pregao = dados[1]
    return wds.janela_cadastro_itens_carona(uasg,pregao,cnn.consultar_itens_homologados(id_pregao))

def caronar_itens(window:sg.Window,values:list):
    """Valida os dados dos itens, a data e insere ao banco de dados."""
    window.BringToFront()
    uasg = window['txt_uasg'].get()
    pregao = window['txt_pregao'].get()
    orgao = values['cb_orgao']
    data_carona = conferir_campos_de_data(values)
    if not data_carona:
        return sg.popup('Favor corrigir a data da carona.')
    if (not str(orgao) != ''):
        return sg.popup('Favor escolher o Órgão solicitante da carona.')
    itens_caronar=[]
    for item in values.keys():
        if 'check' in item:
            if values[item]:
                codigo_item = item.replace('check_','')
                quantidade = values[str(item).replace('check','it_quantidade')]
                quantidade_max = window[str(item).replace('check','txt_quantidade')].get()
                valor = values[str(item).replace('check','it_valor')]
                aux = []
                aux.append(codigo_item)
                if ((not quantidade.isdigit()) or (int(quantidade_max) < int(quantidade) or int(quantidade) < 1)):
                    return sg.popup('Verifique a quantidade para o item '+codigo_item)
                else:
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
            return sg.popup('Para registrar uma carona é necessário que pelo menos um item seja selecionado.')
        else:
            if (not cnn.inserir_carona(uasg,pregao,data_carona,orgao)):
                return sg.popup('Não foi possível registrar a carona.')
            else:
                if(not cnn.inserir_itens_em_carona(uasg,pregao,orgao,data_carona,itens_caronar)):
                    return sg.popup('Houve um problema para registrar os itens da carona.')
                else:
                    sg.popup('Carona registrado com sucesso!')

##JANELA REEQUILIBRIO DE ITENS

def abrir_janela_itens_reequilibrio(id_pregao:str):
    dados = consultar_dados_pregao(id_pregao)
    id_pregao = dados[0]
    uasg = dados[2]
    pregao = dados[1]
    return wds.janela_cadastro_itens_reequilibrio(id_pregao,uasg,pregao,cnn.consultar_itens_homologados(id_pregao))

def reequilibrar_itens(window:sg.Window,values:list):
    window.BringToFront()
    id_pregao = window['txt_id_pregao'].get()
    data_reequilibrio = conferir_campos_de_data(values)
    if not data_reequilibrio:
        return sg.popup('Favor corrigir a data do reequilibrio.')
    itens_reequilibrio=[]
    for item in values.keys():
        if 'check' in item:
            if values[item]:
                codigo_item = item.replace('check_','')
                quantidade_max = window[str(item).replace('check','txt_quantidade')].get()
                valor = values[str(item).replace('check','it_valor')]
                aux = []
                aux.append(codigo_item)
                aux.append(quantidade_max)
                if valor.replace(',','',1).isdigit():
                    valor = str(round(float(valor.replace(',','.',1)),2))
                    if (len(valor.split('.')[1])<2):
                        valor = valor + '0'
                    aux.append(valor)
                else:
                    return sg.popup('Favor corrigir o valor do item '+codigo_item)
                itens_reequilibrio.append(aux)
    else:
        if(len(itens_reequilibrio)<1):
            return sg.popup('Para registrar um pedido de reequilibrio é necessário que pelo menos um item seja selecionado.')
        else:
            if (not cnn.inserir_reequilibrio(id_pregao,data_reequilibrio)):
                return sg.popup('Não foi possível registrar o pedido.\nConfira se o pregão já possui um pedido na mesma data')
            else:
                if(not cnn.inserir_itens_em_reequilibrio(id_pregao,data_reequilibrio,itens_reequilibrio)):
                    return sg.popup('Houve um problema para registrar os itens do pedido.')
                else:
                    sg.popup('Carona registrado com sucesso!')
                    window.Close()

##CONTROLE DE ENTRADAS

def entrada_numerica(valor:str,comprimento:int=7)->str:
    """Confere se o último caractere inserido é um número.\n
    Retorna um caractere a menos caso não seja um número.\n
    Retorna nulo quando a entrada é nula."""
    if valor:
        if(valor[-1].isdigit() and len(valor)<comprimento):
            return valor
        else:
            return valor[:-1]

def entrada_decimal(valor:str,comprimento:int=12)->str:
    """Confere se o último caractere inserido é um número.\n
    Retorna um caractere a menos caso não seja um número ou pontuação.\n
    Retorna nulo quando a entrada é nula."""
    if valor:
        valor = valor.replace('.',',')
        if(valor[-1].isdigit() and len(valor)<comprimento):
            return valor
        elif((valor[-1] == ',') and (valor.count(',')==1 and len(valor)<comprimento)):
            return valor
        else:
            return valor[:-1]