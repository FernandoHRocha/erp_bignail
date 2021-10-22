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

def conferir_se_inteiro_e_menor(numero:str,teto:int):
    """Confere se o parametro numero é um inteiro e menor ou igual ao valor teto."""
    if(numero.isdigit()):
        if(0 < int(numero) <= teto):
            return int(numero)
        else:
            return False
    else:
        return False

def adaptar_codigo_pregao(pregao:str)->str:
    """Converte o texto de identificação do número do pregão para apresentar ao usuário."""
    return pregao[:-4]+'/'+pregao[-4:]

def calcular_preco_minimo(custo:str,frete:str)->str:
    return str((float(custo) + float(frete))/0.75)

def converter_item_dicionario(item:list)->dict:
    """Retorna um dicionario com os dados do item.\n
    O item deve conter os dados na seguinte ordem:
    id - item - modelo - quantidade - valor_ofertado - custo - frete - fornecedor - marca - categoria"""
    return dict(
        id_item = str(item[0]),
        item = str(item[1]),
        modelo = str(item[2]),
        quantidade = str(item[3]),
        valor_ofertado = str(item[4]),
        preco_custo = str(item[5]),
        frete = str(item[6]),
        fornecedor = str(item[7]),
        nome_marca = str(item[8]),
        nome_categoria = str(item[9])
    )