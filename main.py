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

        if(event == 'bt_alterar_fase'):
            pregoes = evh.consultar_dados_selecionados_tabela_pregao(window,values)
            if pregoes:
                [evh.abrir_janela_alterar_fase_pregao(pregao[1],pregao[0]) for pregao in pregoes]
                window.Close()

        if(event == 'bt_pasta'):
            pregoes = evh.consultar_dados_selecionados_tabela_pregao(window,values)
            if pregoes:
                [evh.abrir_pasta_pregao(pregao[0],pregao[1],pregao[2]) for pregao in pregoes]
        
        if(event == 'bt_consultar_itens'):
            sg.popup('Abrir janela consulta itens.')
        
        if(event == 'bt_homologar'):
            pregoes = evh.consultar_dados_selecionados_tabela_pregao(window,values)
            if pregoes:
                [evh.abrir_janela_homologacao_itens(pregao[1],pregao[0]) for pregao in pregoes]
                window.Close()

        if(event == 'bt_registrar_empenho'):
            pregoes = evh.consultar_dados_selecionados_tabela_pregao(window,values)
            if pregoes:
                [evh.abrir_janela_itens_empenhar(pregao[1],pregao[0]) for pregao in pregoes]
        
        if(event == 'bt_registrar_carona'):
            pregoes = evh.consultar_dados_selecionados_tabela_pregao(window,values)
            if pregoes:
                [evh.abrir_janela_itens_carona(pregao[1],pregao[0]) for pregao in pregoes]

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
            sg.popup('Em qual data a entrega foi realizada?')

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
        pass

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

    if(window.Title==titulo_janelas['janela_cadastro_homologacao']):
        if event:
            if('check_' in event):
                frame_input = str(event).replace('check_','fr_it_')
                window[frame_input].update(visible=True) if values[event] else window[frame_input].update(visible=False)
        
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
                frame_input = str(event).replace('check_','fr_it_')
                window[frame_input].update(visible=True) if values[event] else window[frame_input].update(visible=False)
        
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
                frame_input = str(event).replace('check_','fr_it_')
                window[frame_input].update(visible=True) if values[event] else window[frame_input].update(visible=False)
        
        if (event=='bt_concluir'):
            evh.caronar_itens(window, values)
            janela_anterior=wds.janela_consulta

        if(event=='bt_cancelar'):
            janela_anterior=wds.janela_consulta
            window.Close()
            wds.janela_consulta_pregoes()

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