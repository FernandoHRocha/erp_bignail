from datetime import datetime

def padronizar_tamanho_texto(texto:str,tamanho:int,char:str):
    """Padroniza a quantia de caracteres que um texto possui."""
    texto = str(texto)
    char = str(char)
    while(len(texto)<tamanho):
        texto=char+texto
    return texto

def padronizar_uasg(codigo:str):
    """Retorna o uma string padrozinada do código uasg."""
    return padronizar_tamanho_texto(codigo,6,'0')

def padronizar_pregao(codigo:str):
    """Retorna uma string padronizada do código número do pregão."""
    return padronizar_tamanho_texto(codigo,10,'0')

def padronizar_data_hora(data:str,hora:str):
    """Retorna uma string padronizada da data e horário no formato numérico DD-MM-YYYY H:M."""
    codigo = datetime.strptime(data + ' ' + hora,r'%Y-%m-%d %H:%M')
    codigo = datetime.strftime(codigo,r'%Y-%m-%d %H:%M')
    return codigo

def padronizar_nome_pasta(data:str,pregao:str,uasg:str):
    """Retorna o padrao de nomenclatura das pastas."""
    data = datetime.strftime(datetime.strptime(data,r'%Y-%m-%d %H:%M'),r'%Y-%m-%d')
    codigo = data+'_'+pregao+'_'+uasg
    return codigo