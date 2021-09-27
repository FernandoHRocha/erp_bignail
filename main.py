from database import connection as cnn
from interface import windows as wds
from interface import event_handler as evh
from automation import automate as aut
import PySimpleGUI as sg

janela_anterior = wds.janela_menu

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

    if(window.Title==wds.titulo_janelas['janela_menu']):
        if(event == 'bt_consultar'):
            janela_anterior=wds.janela_menu
            wds.janela_consulta()
        if(event == 'bt_cadastrar'):
            janela_anterior=wds.janela_menu
            wds.janela_cadastro()
        if(event == 'bt_comprasnet'):
            janela_anterior=wds.janela_menu
            wds.janela_comprasnet()

    if(window.Title==wds.titulo_janelas['janela_consulta']):
        if(event == 'bt_submeter'):
            pass
        if(event == 'bt_disputar'):
            pass
        if(event == 'bt_julgamento'):
            pass
        if(event == 'bt_consulta_pregao'):
            janela_anterior=wds.janela_consulta
            window.Close()
            evh.abrir_janela_consulta_pregao(window)
    
    if(window.Title==wds.titulo_janelas['janela_cadastro']):
        if(event == 'bt_planilha'):
            janela_anterior=wds.janela_cadastro
            aut.cadastrar_planilha()
        if(event == 'bt_carona'):
            pass
        if(event == 'bt_pedido'):
            pass

    if(window.Title==wds.titulo_janelas['janela_comprasnet']):
        if(event == 'bt_cadastrar'):
            janela_anterior=wds.janela_comprasnet
            aut.cadastrar_pregao()
        if(event == 'bt_consultar'):
            pass
        if(event == 'bt_disputar'):
            pass

    if(window.Title==wds.titulo_janelas['janela_consulta_pregao']):
        #janela_anterior=wds.janela_consulta_pregao
        if(event == 'cb_orgao'):
            print('oi')
            pass
        if(event == 'cb_pregao'):
            pass
        if(event == 'tg_item'):#eventos tb_geral tb_ganho
            pass
        
    if(event == sg.WIN_CLOSED):
        break

window.close()