from database import connection as cnn
from interface import windows as wds
import adapter
import credentials
import PySimpleGUI as sg
import time
import os

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

def consultar_dados_selecionados_tabela_pregao(window:sg.Window, values:dict, msg_erro:str='Favor selecionar um pregão.'):
    """Retorna os dados do(s) pregão(ões) selecionado(s) na guia atual.\n
    Caso nenhum pregão esteja selecionado retorna False e um sg.popup(msg_erro) é mostrado.\n
    msg_erro - Str com a mensagem que deve aparecer caso nenhum pregão seja selecionado,
    não passando esse parametro será considerada uma frase padrão."""
    tab = str(values['tg_pregoes']).replace('tab','tb')
    if (len(values[tab])>0):
        return [window[tab].get()[linha] for linha in values[tab]]
    else:
        sg.popup(msg_erro)
        return False

def consultar_dados_pregao(id_pregao:str):
    return cnn.consultar_dados_pregao(id_pregao)

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
    window['tb_ganho'].update(values=cnn.consultar_itens_homologados(orgao,pregao))

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

def abrir_janela_alterar_fase_pregao(uasg:str,pregao:str):
    """Abre a janela para alteração de fase de pregão."""
    wds.janela_consulta_pregao_alterar_fase(uasg,pregao,cnn.consultar_fases_pregoes())

def listar_itens_em_categorias(id_pregao:str):
    """Retorna os dados necessários para apresentar os itens do pregão em suas categorias."""
    cabecalho_participados =    [
        ['Item','Marca','Modelo','Quant','Preço','Custo','Frete','Fornecedor','id'],
        [5,15,20,5,12,12,8,20,0]]
    cabecalho_homologados =  [
        ['Item','Marca','Modelo','Preço','Quant','Empenho','Carona','id'],
        [5,15,20,12,5,7,5,0]]
    cabecalho_empenhos =    [
        ['Item','Marca','Modelo','Quant','Preço','Custo','Data Empenho','Data Entrega','Nota','Fase','id'],
        [5,15,20,5,12,12,12,12,10,12,0]]
    cabecalho_caronas =     [
        ['Item','Marca','Modelo','Quant','Preço','Data','Órgão','Fase','id'],
        [5,15,20,5,12,10,30,12,0]]
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

##JANELA HOMOLOGAÇÃO DE ITENS

def abrir_janela_homologacao_itens(uasg:str, pregao:str):
    """Faz a chamada dos itens do pregão ao banco de dados e abre a janela de itens a homologar."""
    wds.janela_cadastro_homologacao(uasg,pregao,cnn.consultar_itens_homologar(uasg, pregao))

def homologar_pregao_e_itens(window:sg.Window,values:dict):
    """Verifica e converte os valores dos itens para homologacao."""
    window.BringToFront()
    uasg = window['txt_uasg'].get()
    pregao = window['txt_pregao'].get()
    data_ata = conferir_campos_de_data(values)
    if not data_ata:
        return sg.popup('Favor conferir a data de assinatura da ata.')
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
        if not cnn.inserir_itens_ganho(uasg,pregao,itens_homologar):
            return sg.popup('Não foi possível inserir os itens como homologados.')
        sg.popup('O pregão foi homologado.')
        window.Close()

##JANELA EMPENHO DE ITENS

def abrir_janela_itens_empenhar(uasg:str,pregao:str):
    """Coleta as informações dos itens do pregão e chama a janela para empenho."""
    return wds.janela_cadastro_itens_empenhar(uasg,pregao,cnn.consultar_itens_homologados(uasg,pregao))

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
                quantidade = values[str(item).replace('check','it')]
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
                    window.Close()

##JANELA CARONA DE ITENS

def abrir_janela_itens_carona(uasg:str,pregao:str):
    """Coleta as informações dos itens do pregão e chama a janela para carona."""
    return wds.janela_cadastro_itens_carona(uasg,pregao,cnn.consultar_itens_homologados(uasg,pregao))

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
                quantidade = values[str(item).replace('check','it')]
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
                    window.Close()

