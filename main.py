from database import connection as cnn
from interface import windows as wds
from interface import event_handler as evh
from automation import automate as aut
from functools import partial
import PySimpleGUI as sg

janela_anterior = []
titulo_janelas = wds.titulo_janelas

wds.janela_menu()

while True:
    window, event, values = sg.read_all_windows()

    #print(window,event,values)

    if(window.Title==titulo_janelas['janela_menu']):
        if(event == 'bt_consultar'):
            janela_anterior.append(wds.janela_menu)
            wds.janela_consulta()
        
        if(event == 'bt_cadastrar'):
            janela_anterior.append(wds.janela_menu)
            wds.janela_cadastro()
        
        if(event == 'bt_comprasnet'):
            janela_anterior.append(wds.janela_menu)
            wds.janela_comprasnet()

###JANELAS DESTINADAS A PROCEDIMENTOS DE CONSULTAS

    if(window.Title==titulo_janelas['janela_consulta']):
        if(event == 'bt_consulta_geral'):
            window.Close()
            janela_anterior.append(wds.janela_consulta)
            wds.janela_consulta_pregoes()
        
        if(event == 'bt_consulta_pregao'):
            window.Close()
            janela_anterior.append(wds.janela_consulta)
            wds.janela_consulta_pregao()
        
        if(event == 'bt_consulta_empenhos'):
            window.Close()
            janela_anterior.append(wds.janela_consulta)
            wds.janela_consulta_empenhos()
        
        if(event == 'bt_consulta_reequilibrios'):
            window.Close()
            janela_anterior.append(wds.janela_consulta)
            wds.janela_consulta_reequilibrio()
        
        if(event == 'bt_consulta_carona'):
            window.Close()
            janela_anterior.append(wds.janela_consulta)
            wds.janela_consulta_carona()

    if(window.Title==titulo_janelas['janela_consulta_pregao']):
        if (event == 'it_uasg'):
            valor = evh.entrada_numerica(values['it_uasg'])
            window['it_uasg'].update(value=valor)
            evh.procurar_pelo_uasg(valor,window)

        if (event == 'it_orgao'):
            evh.procurar_pelo_orgao(values['it_orgao'],window)
        
        if(event == 'cb_uasg'):
            evh.mostrar_frame_informacoes_opcoes(window,False)
            evh.atualizar_orgao_pelo_uasg(values['cb_uasg'],window)

        if(event == 'cb_orgao'):
            evh.mostrar_frame_informacoes_opcoes(window,False)
            evh.atualizar_uasg_pelo_orgao(values['cb_orgao'],window)

        if (event == 'it_pregao'):
            valor = evh.entrada_numerica(values['it_pregao'])
            window['it_pregao'].update(value=valor)
            evh.procurar_pelo_pregao(valor,values['cb_uasg'],window)

        if(event == 'cb_pregao'):
            evh.mostrar_frame_informacoes_opcoes(window)
            evh.atualizar_informacoes_pregao(values['cb_uasg'],values['cb_pregao'],window)
        
        if(event == 'bt_pasta'):
            evh.abrir_pasta_pregao(window['txt_id_pregao'].get())

        if(event == 'bt_consultar_itens'):
            window.Close()
            janela_anterior.append(wds.janela_consulta_pregao)
            wds.janela_consulta_itens_pregao(window['txt_id_pregao'].get())

    if(window.Title==titulo_janelas['janela_consulta_pregoes']):
        if(event == 'bt_alterar_fase'):
            pregoes = evh.consultar_dados_selecionados_tabela(window,values,'tg_pregoes')
            if pregoes:
                window.Close()
                janela_anterior.append(wds.janela_consulta_pregoes)
                [evh.abrir_janela_alterar_fase_pregao(pregao[2],pregao[1]) for pregao in pregoes]

        if(event == 'bt_pasta'):
            pregoes = evh.consultar_dados_selecionados_tabela(window,values,'tg_pregoes')
            if pregoes:
                [evh.abrir_pasta_pregao(pregao[0]) for pregao in pregoes]
        
        if(event == 'bt_consultar_itens'):
            pregoes = evh.consultar_dados_selecionados_tabela(window,values,'tg_pregoes')
            if pregoes:
                window.Close()
                janela_anterior.append(wds.janela_consulta_pregoes)
                wds.janela_consulta_itens_pregao(pregoes[0][0])
        
        if(event == 'bt_alterar_data'):
            pregao = evh.consultar_dados_selecionados_tabela(window,values,'tg_pregoes')
            if pregao:
                window.Close()
                janela_anterior.append(wds.janela_consulta_pregoes)
                wds.janela_alteracao_data_abertura(cnn.consultar_dados_pregao(pregao[0][0]))

        if(event == 'bt_homologar'):
            pregoes = evh.consultar_dados_selecionados_tabela(window,values,'tg_pregoes')
            if pregoes:
                window.Close()
                janela_anterior.append(wds.janela_consulta_pregoes)
                [evh.abrir_janela_homologacao_itens(pregao[0]) for pregao in pregoes]

        if(event == 'bt_registrar_empenho'):
            pregoes = evh.consultar_dados_selecionados_tabela(window,values,'tg_pregoes')
            if pregoes:
                window.Close()
                janela_anterior.append(wds.janela_consulta_pregoes)
                [evh.abrir_janela_itens_empenhar(pregao[0]) for pregao in pregoes]
        
        if(event == 'bt_registrar_carona'):
            pregoes = evh.consultar_dados_selecionados_tabela(window,values,'tg_pregoes')
            if pregoes:
                window.Close()
                janela_anterior.append(wds.janela_consulta_pregoes)
                [evh.abrir_janela_itens_carona(pregao[0]) for pregao in pregoes]

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
        if(event=='bt_pasta'):
            empenho = evh.consultar_dados_selecionados_tabela(window,values,'tg_empenhos','Primeiro selecione um empenho.')
            if empenho:
                evh.abrir_pasta_pregao(cnn.consultar_id_pregao_do_empenho(empenho[0][0]))

        if(event == 'bt_consultar_pregao'):
            empenho = evh.consultar_dados_selecionados_tabela(window,values,'tg_empenhos','Primeiro selecione um empenho.')
            if empenho:
                window.Close()
                janela_anterior.append(wds.janela_consulta_empenhos)
                wds.janela_consulta_itens_pregao(cnn.consultar_id_pregao_do_empenho(empenho[0][0]))
        
        if(event == 'bt_consultar_itens'):
            pass

        if(event == 'bt_registrar_entrega'):
            empenho = evh.consultar_dados_selecionados_tabela(window,values,'tg_empenhos','Primeiro selecione um empenho.')
            if empenho:
                window.Close()
                janela_anterior.append(wds.janela_consulta_empenhos)
                wds.janela_cadastro_entrega_empenho(empenho[0][0])
        
        if(event == 'tg_empenhos'):
            if(values['tg_empenhos'] == 'tab_finalizado'):
                window['bt_registrar_entrega'].update(visible=False)
            else:
                window['bt_registrar_entrega'].update(visible=True)

    if(window.Title==titulo_janelas['janela_consulta_reequilibrio']):
        if(event == 'bt_registrar_envio'):
            sg.popup('Registra o envio do pedido no banco de dados e abre a pasta do pregão.')
        
        if(event == 'bt_registrar_aceite'):
            sg.popup('Registra a aceitação no banco de dados e abre a pasta do pregão.')
        
        if(event == 'bt_registrar_recusa'):
            sg.popup('Registra a recusa no banco de dados e abre a pasta do pregão.')

    if(window.Title==titulo_janelas['janela_consulta_carona']):
        if(event=='bt_pasta'):
            carona = evh.consultar_dados_selecionados_tabela(window,values,'tg_carona','Primeiro selecione uma carona.')
            if carona:
                evh.abrir_pasta_pregao(cnn.consultar_id_pregao_da_carona(carona[0][0]))
        
        if(event=='bt_consultar_pregao'):
            carona = evh.consultar_dados_selecionados_tabela(window,values,'tg_carona','Primeiro selecione uma carona.')
            if carona:
                window.Close()
                janela_anterior.append(wds.janela_consulta_carona)
                wds.janela_consulta_itens_pregao(cnn.consultar_id_pregao_da_carona(carona[0][0]))

        if(event == 'bt_consultar_itens'):
            sg.popup('Abre a consulta aos itens da carona.')
        
        if(event == 'bt_empenhar'):
            sg.popup('Mostra opções para alterar a fase da carona.')

    if(window.Title==titulo_janelas['janela_consulta_itens_pregao']):
        if(event == 'bt_pasta'):
            evh.abrir_pasta_pregao(window['txt_id_pregao'].get())

        if (event == 'bt_item_alterar'):
            pregoes = evh.consultar_dados_selecionados_tabela(window,values,'tg_itens')
            pass
        
        if (event == 'bt_item_empenho'):
            window.Close()
            janela_anterior.append(partial(wds.janela_consulta_itens_pregao,str(window['txt_id_pregao'].get())))
            evh.abrir_janela_itens_empenhar(window['txt_id_pregao'].get())

        if (event == 'bt_item_carona'):
            pass
        
        if (event == 'bt_reequilibrio'):
            pass
        
        if (event == 'bt_fornecedor'):
            item = evh.consultar_dados_selecionados_tabela(window,values,'tg_itens')
            if item:
                evh.copiar_para_area_transferencia(item[0][8])

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
        
        if(event=='bt_cancelar'):
            window.Close()
            evh.voltar_pagina(janela_anterior,wds.janela_menu)

    if(window.Title==titulo_janelas['janela_cadastro_itens_empenhar']):
        if event:
            if('check_' in event):
                evh.alterar_apresentacao_item(window,values,event)
        
        if (event=='bt_concluir'):
            evh.empenhar_itens(window, values)
        
        if(event=='bt_cancelar'):
            window.Close()
            evh.voltar_pagina(janela_anterior,wds.janela_menu)

    if(window.Title==titulo_janelas['janela_cadastro_itens_carona']):
        if event:
            if('check_' in event):
                evh.alterar_apresentacao_item(window,values,event)

        if (event=='bt_concluir'):
            evh.caronar_itens(window, values)

        if(event=='bt_cancelar'):
            window.Close()

    if(window.Title==titulo_janelas['janela_cadastro_entrega_empenho']):
        if(event=='bt_cancelar'):
            window.Close()
            wds.janela_consulta_empenhos()
        
        if(event=='bt_concluir'):
            data = evh.conferir_campos_de_data(values)
            if data:
                if cnn.inserir_entrega_de_empenho(window['txt_id_empenho'].get(),data):
                    sg.popup('Entrega resgistrada.')
                else:
                    sg.popup('Não foi possível realizar o registro.')
                window.Close()
                evh.voltar_pagina(janela_anterior,wds.janela_menu)
            else:
                sg.popup('Reveja a data de entrega.')

###JANELAS DESTINADAS A PROCEDIMENTOS DE ALTERAÇÃO

    if(window.Title==titulo_janelas['janela_alteracao_data_abertura']):
        if(event == 'bt_concluir'):
            try:
                nova_data = evh.conferir_campos_de_data(values) + ' ' + evh.conferir_campo_de_hora(values)
                if cnn.alterar_data_abertura(window['txt_id_pregao'].get(),nova_data):
                    sg.popup('Data alterada com sucesso.')
                    window.Close()
                    evh.voltar_pagina(janela_anterior,wds.janela_menu)
            except:
                sg.popup('Confira se a data está correta.')
                
        if(event == 'bt_cancelar'):
            window.Close()
            evh.voltar_pagina(janela_anterior,wds.janela_menu)

###JANELAS DESTINADAS AOS PROCESSOS DE AUTOMAÇÃO

    if(window.Title==titulo_janelas['janela_comprasnet']):
        if(event == 'bt_cadastrar'):
            janela_anterior.append(wds.janela_comprasnet)
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
                window.Close()
                evh.voltar_pagina(janela_anterior,wds.janela_menu)
                cnn.alterar_fase_pregao(window['txt_uasg'].get(),window['txt_pregao'].get(),values['cb_alterar_fase'])

    if event == 'bt_voltar':
        window.Close()
        janela_anterior = evh.voltar_pagina(janela_anterior,wds.janela_menu)

    if(event == sg.WIN_CLOSED):
        if(window.Title == titulo_janelas['janela_menu']):
            break
        else:
            window.Close()

window.close()