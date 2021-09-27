from database import connection as cnn
from interface import windows as wds
from automation import automate as aut
import PySimpleGUI as sg

janela1, janela2 = wds.janela_menu(), None
janela_anterior = wds.janela_menu

while True:
    window, event, values = sg.read_all_windows()

    if event == 'bt_voltar':
        janela1.UnHide()
        janela2.Hide()

    if(window.Title==wds.titulo_janelas['janela_menu']):
        janela_anterior=wds.janela_menu
        if(event == 'bt_consultar'):
            janela2 = wds.janela_consulta()
            janela1.Hide()
            pass
        if(event == 'bt_cadastrar'):
            janela2 = wds.janela_cadastro()
            janela1.Hide()
            pass
        if(event == 'bt_comprasnet'):
            janela2 = wds.janela_comprasnet()
            janela1.Hide()
            pass

    if(window.Title==wds.titulo_janelas['janela_consulta']):
        janela_anterior=wds.janela_consulta
        if(event == 'bt_submeter'):
            pass
        if(event == 'bt_disputar'):
            pass
        if(event == 'bt_julgamento'):
            pass
    
    if(window.Title==wds.titulo_janelas['janela_cadastro']):
        janela_anterior=wds.janela_cadastro
        if(event == 'bt_planilha'):
            aut.cadastrar_planilha()
            pass
        if(event == 'bt_carona'):
            pass
        if(event == 'bt_pedido'):
            pass

    if(window.Title==wds.titulo_janelas['janela_comprasnet']):
        janela_anterior=wds.janela_comprasnet
        if(event == 'bt_cadastrar'):
            aut.cadastrar_pregao()
            pass
        if(event == 'bt_consultar'):
            pass
        if(event == 'bt_disputar'):
            pass
        
    if(event == sg.WIN_CLOSED):
        break

window.close()