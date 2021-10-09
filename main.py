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

    if(window.Title==titulo_janelas['janela_consulta_pregao']):
        if (event == 'it_uasg'):
            valor = evh.entrada_numerica(values['it_uasg'])
            window['it_uasg'].update(value=valor)
            evh.procurar_pelo_uasg(valor,window)

        if (event == 'it_orgao'):
            evh.procurar_pelo_orgao(values['it_orgao'],window)
        
        if(event == 'cb_uasg'):
            evh.atualizar_orgao_pelo_uasg(values['cb_uasg'],window)

        if(event == 'cb_orgao'):
            evh.atualizar_uasg_pelo_orgao(values['cb_orgao'],window)

        if (event == 'it_pregao'):
            valor = evh.entrada_numerica(values['it_pregao'])
            window['it_pregao'].update(value=valor)
            evh.procurar_pelo_uasg(valor,window)

        if(event == 'cb_pregao'):
            window['fr_info_pregao'].update(visible=True)
            window['fr_opcoes_pregao'].update(visible=True)

    if(window.Title==titulo_janelas['janela_consulta_pregoes']):
        janela_anterior=wds.janela_consulta
        if(event == 'bt_alterar_fase'):
            pregoes = evh.consultar_dados_selecionados_tabela(window,values,'tg_pregoes')
            if pregoes:
                [evh.abrir_janela_alterar_fase_pregao(pregao[1],pregao[0]) for pregao in pregoes]
                window.Close()

        if(event == 'bt_pasta'):
            pregoes = evh.consultar_dados_selecionados_tabela(window,values,'tg_pregoes')
            if pregoes:
                [evh.abrir_pasta_pregao(pregao[0],pregao[1],pregao[2]) for pregao in pregoes]
        
        if(event == 'bt_consultar_itens'):
            pregoes = evh.consultar_dados_selecionados_tabela(window,values,'tg_pregoes')
            if pregoes:
                janela_anterior=wds.janela_consulta_pregoes
                wds.janela_consulta_itens_pregao(pregoes[0][len(pregoes[0])-1])
                window.Close()
        
        if(event == 'bt_homologar'):
            pregoes = evh.consultar_dados_selecionados_tabela(window,values,'tg_pregoes')
            if pregoes:
                [evh.abrir_janela_homologacao_itens(pregao[1],pregao[0]) for pregao in pregoes]
                window.Close()

        if(event == 'bt_registrar_empenho'):
            pregoes = evh.consultar_dados_selecionados_tabela(window,values,'tg_pregoes')
            if pregoes:
                [evh.abrir_janela_itens_empenhar(pregao[1],pregao[0]) for pregao in pregoes]
                window.Close()
        
        if(event == 'bt_registrar_carona'):
            pregoes = evh.consultar_dados_selecionados_tabela(window,values,'tg_pregoes')
            if pregoes:
                [evh.abrir_janela_itens_carona(pregao[1],pregao[0]) for pregao in pregoes]
                window.Close()

        if(event == 'tg_pregoes'):
            if(values['tg_pregoes'] in ['tab_homologado','tab_finalizado']):
                window['cl_julgamento'].update(visible=False)
                window['cl_ganho'].update(visible=True)
            elif(values['tg_pregoes'] in ['tab_proposta','tab_julgamento','tab_frustrado']):
                window['cl_julgamento'].update(visible=True)
                window['cl_ganho'].update(visible=False)
            else:
                window['cl_julgamento'].update(visible=False)
                window['cl_ganho'].update(visible=False)

    if(window.Title==titulo_janelas['janela_consulta_empenhos']):
        if(event == 'bt_consultar'):
            sg.popup('Abre a consulta aos itens do empenho.')
        if(event == 'bt_registrar_entrega'):
            empenho = evh.consultar_dados_selecionados_tabela(window,values,'tg_empenhos')
            if empenho:
                window.Close()
                wds.janela_cadastro_entrega_empenho(empenho[0][0])

    if(window.Title==titulo_janelas['janela_consulta_reequilibrio']):
        if(event == 'bt_registrar_envio'):
            sg.popup('Registra o envio do pedido no banco de dados e abre a pasta do pregão.')
        if(event == 'bt_registrar_aceite'):
            sg.popup('Registra a aceitação no banco de dados e abre a pasta do pregão.')
        if(event == 'bt_registrar_recusa'):
            sg.popup('Registra a recusa no banco de dados e abre a pasta do pregão.')

    if(window.Title==titulo_janelas['janela_consulta_carona']):
        if(event == 'bt_consultar'):
            sg.popup('Abre a consulta aos itens da carona.')
        if(event == 'bt_empenhar'):
            sg.popup('Mostra opções para alterar a fase da carona.')

    if(window.Title==titulo_janelas['janela_consulta_itens_pregao']):
        if (event == 'bt_item_alterar'):
            pregoes = evh.consultar_dados_selecionados_tabela(window,values,'tg_itens')
            pass
        if (event == 'bt_item_empenho'):
            pass
        if (event == 'bt_item_carona'):
            pass
        if (event == 'bt_reequilibrio'):
            pass
        if (event == 'bt_fornecedor'):
            pass

###JANELAS DESTINADAS A PROCEDIMENTOS DE CADASTROS

    if(window.Title==titulo_janelas['janela_cadastro']):
        if(event == 'bt_cadastro_planilha'):
            aut.cadastrar_planilha()
        if(event == 'bt_cadastro_empenho'):
            pass
        if(event == 'bt_cadastro_carona'):
            pass
        if(event == 'bt_cadastro_reequilibrio'):
            pass

    if(window.Title==titulo_janelas['janela_cadastro_homologacao']):
        if event:
            if('check_' in event):
                evh.alterar_apresentacao_item(window,values,event)

        if (event=='bt_concluir'):
            evh.homologar_pregao_e_itens(window, values)
            janela_anterior=wds.janela_consulta
        
        if(event=='bt_cancelar'):
            janela_anterior=wds.janela_consulta
            window.Close()
            wds.janela_consulta_pregoes()

    if(window.Title==titulo_janelas['janela_cadastro_itens_empenhar']):
        if event:
            if('check_' in event):
                evh.alterar_apresentacao_item(window,values,event)
        
        if (event=='bt_concluir'):
            evh.empenhar_itens(window, values)
            janela_anterior=wds.janela_consulta
        
        if(event=='bt_cancelar'):
            janela_anterior=wds.janela_consulta
            window.Close()
            wds.janela_consulta_pregoes()

    if(window.Title==titulo_janelas['janela_cadastro_itens_carona']):
        if event:
            if('check_' in event):
                evh.alterar_apresentacao_item(window,values,event)

        if (event=='bt_concluir'):
            evh.caronar_itens(window, values)
            janela_anterior=wds.janela_consulta

        if(event=='bt_cancelar'):
            janela_anterior=wds.janela_consulta
            window.Close()
            wds.janela_consulta_pregoes()

    if(window.Title==titulo_janelas['janela_cadastro_entrega_empenho']):
        if(event=='bt_cancelar'):
            window.Close()
        if(event=='bt_concluir'):
            data = evh.conferir_campos_de_data(values)
            if data:
                if cnn.inserir_entrega_de_empenho(window['txt_empenho'].get(),data):
                    sg.popup('Entrega resgistrada.')
                else:
                    sg.popup('Não foi possível realizar o registro.')
                window.Close()
                wds.janela_consulta_empenhos()
            else:
                sg.popup('Reveja a data de entrega.')

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

    if event == 'bt_voltar':
        window.Close()
        if janela_anterior != 'janela_menu':
            janela_anterior()

    if(event == sg.WIN_CLOSED):
        if(window.Title == titulo_janelas['janela_menu']):
            break
        else:
            window.Close()

window.close()