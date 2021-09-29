from database import connection as cnn
from interface import windows as wds
from interface import event_handler as evh
from automation import automate as aut
import PySimpleGUI as sg

janela_anterior = wds.janela_menu
titulo_janelas = wds.titulo_janelas

wds.janela_menu()

while True:
    window, event, values = sg.read_all_windows()

    print(window.Title, event, values)

    if event == 'bt_voltar':
        if janela_anterior == 'janela_menu':
            window.Close()
        else:
            window.Close()
            janela_anterior()

    if(window.Title==titulo_janelas['janela_menu']):
        if(event == 'bt_consultar'):
            janela_anterior=wds.janela_menu
            wds.janela_consulta()
        if(event == 'bt_cadastrar'):
            janela_anterior=wds.janela_menu
            wds.janela_cadastro()
        if(event == 'bt_comprasnet'):
            janela_anterior=wds.janela_menu
            wds.janela_comprasnet()

###JANELAS DESTINADAS A PROCEDIMENTOS DE CONSULTAS

    if(window.Title==titulo_janelas['janela_consulta']):
        if(event == 'bt_consulta_geral'):
            janela_anterior=wds.janela_consulta
            window.Close()
            wds.janela_consulta_pregoes()
        if(event == 'bt_consulta_pregao'):
            janela_anterior=wds.janela_consulta
            window.Close()
            wds.janela_consulta_pregao()
        if(event == 'bt_consulta_empenhos'):
            janela_anterior=wds.janela_consulta
            window.Close()
            wds.janela_consulta_empenhos()
        if(event == 'bt_consulta_reequilibrios'):
            janela_anterior=wds.janela_consulta
            window.Close()
            wds.janela_consulta_reequilibrio()
        if(event == 'bt_consulta_carona'):
            janela_anterior=wds.janela_consulta
            window.Close()
            wds.janela_consulta_carona()
        if(event == 'bt_consulta_atas'):
            janela_anterior=wds.janela_consulta
            window.Close()
            wds.janela_consulta_atas()

    if(window.Title==titulo_janelas['janela_consulta_pregao']):
        #wds.janela_consulta_pregao
        if(event == 'cb_orgao'):
            evh.escolher_orgao(window,values['cb_orgao'])
        if(event == 'cb_pregao'):
            evh.apresentar_itens_pregao(window,values['cb_orgao'],values['cb_pregao'])
        if(event == 'tg_item'):#eventos de mudança de aba tab_registrado tab_ganho
            pass
        if(event == 'tb_registrado'):
            pass
        if(event == 'tb_ganho'):
            pass
        if(event == 'bt_item_alterar'):
            sg.popup('Abre a tela de alteração das informações do item.')
        if(event == 'bt_item_empenho'):
            sg.popup('Registra o empenho dos itens selecionados e abre a pasta do pregão.')
        if(event == 'bt_item_carona'):
            sg.popup('Registra o aceite de carona dos itens selecionados e abre a pasta do pregão.')

    if(window.Title==titulo_janelas['janela_consulta_pregoes']):
        #wds.janela_consulta_pregoes
        if(event == 'bt_alterar_fase'):
            tab = str(values['tg_pregoes']).replace('tab','tb')
            if(len(values[tab])>0):
                lista = values[tab]
                for linha in lista:
                    pregao = window[tab].get()[linha]
                    evh.abrir_janela_alterar_fase_pregao(pregao[1],pregao[0])
                    window.Close()
            else:
                sg.popup('Para alterar a fase de algum pregão é preciso selecionar um primeiro.')

        if(event == 'bt_pasta'):
            tab = str(values['tg_pregaos'].replace('tab','tb'))
            if (len(values[tab])>0):
                lista = values[tab]
                for linha in lista:
                    pregao = window[tab].get()[linha]
                    evh.
            sg.popup('Abre a pasta do pregão.')

    if(window.Title==titulo_janelas['janela_consulta_empenhos']):
        if(event == 'bt_registrar_empenho'):
            sg.popup('Registra o empenho no banco de dados e abre a pasta do pregão.')

    if(window.Title==titulo_janelas['janela_consulta_reequilibrio']):
        if(event == 'bt_registrar_envio'):
            sg.popup('Registra o envio do pedido no banco de dados e abre a pasta do pregão.')
        if(event == 'bt_registrar_aceite'):
            sg.popup('Registra a aceitação no banco de dados e abre a pasta do pregão.')
        if(event == 'bt_registrar_recusa'):
            sg.popup('Registra a recusa no banco de dados e abre a pasta do pregão.')

    if(window.Title==titulo_janelas['janela_consulta_carona']):
        if(event == 'bt_registrar_carona'):
            sg.popup('Registra adesão à carona no banco de dados e abre a pasta do pregão.')

    if(window.Title==titulo_janelas['janela_consulta_atas']):
        if(event == 'bt_registrar_ata'):
            sg.popup('Registra a assinatura no banco de dados e abre a pasta do pregão.')

###JANELAS DESTINADAS A PROCEDIMENTOS DE CADASTROS

    if(window.Title==titulo_janelas['janela_cadastro']):
        if(event == 'bt_cadastro_planilha'):
            janela_anterior=wds.janela_cadastro
            aut.cadastrar_planilha()
        if(event == 'bt_cadastro_empenho'):
            pass
        if(event == 'bt_cadastro_carona'):
            pass
        if(event == 'bt_cadastro_reequilibrio'):
            pass

###JANELAS DESTINADAS AOS PROCESSOS DE AUTOMAÇÃO

    if(window.Title==titulo_janelas['janela_comprasnet']):
        if(event == 'bt_cadastrar'):
            janela_anterior=wds.janela_comprasnet
            aut.cadastrar_pregao()
        if(event == 'bt_consultar'):
            pass
        if(event == 'bt_disputar'):
            pass

###JANELAS DESTINADAS AOS PROCESSOS AUXILIARES

    if(window.Title==titulo_janelas['janela_consulta_pregao_alterar_fase']):
        if(event=='bt_confirmar_fase'):
            if(values['cb_alterar_fase']==''):
                sg.popup('Favor escolher um novo estado para o pregão.')
            else:
                cnn.alterar_fase_pregao(window['txt_uasg'].get(),window['txt_pregao'].get(),values['cb_alterar_fase'])
                window.Close()
                wds.janela_consulta_pregoes()

    if(event == sg.WIN_CLOSED):
        if(window.Title == titulo_janelas['janela_menu']):
            break
        else:
            window.Close()

window.close()