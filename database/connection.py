import pyodbc
import credentials as dbi
conn = pyodbc.connect('Driver='+dbi.driver+';''Server='+dbi.server+';''Database='+dbi.database+';''Trusted_Connection='+dbi.trusted+';UID='+dbi.uid+';PWD='+dbi.pwd+';')

cursor = conn.cursor()

def validar(campo):#NÃO PERMITE SQL INJECTION
    campo = str(campo).replace("'","").replace("--","")
    return campo

###CONSULTAS A IDENTIFICADORES------------------------------------

def consultar_id_orgao(uasg):
    """Retorna o código identificador do pregão caso ele exista, senão retorna -1."""
    cursor.execute("select id_orgao from orgao where uasg = '"+validar(uasg)+"'  ORDER BY id_orgao OFFSET 0 ROW FETCH NEXT 1 ROW ONLY;")
    resultado = cursor.fetchone()
    return str(resultado[0]) if resultado!=None else '-1'

def consultar_id_orgao_nome(nome):
    """Retorna o código identificador do pregão caso ele exista, senão retorna -1."""
    cursor.execute("select id_orgao from orgao where nome_orgao =  '"+validar(nome)+"';")
    resultado = cursor.fetchone()
    return str(resultado[0]) if resultado!=None else '-1'

def consultar_id_pregao(uasg:str,pregao:str):
    """Retorna o id do pregão, caso não exista retorna -1."""
    id_orgao = consultar_id_orgao(uasg)
    cursor.execute("select id_pregao from pregao where id_orgao = '"+validar(id_orgao)+"';")
    resultado = cursor.fetchone()
    return str(resultado[0]) if resultado!=None else '-1'

def consultar_id_item(item:str,uasg:str,pregao:str):
    """Retorna o id de um item. Caso não exista retorna o valor -1."""
    id_pregao = consultar_id_pregao(uasg,pregao)
    query=( "select id_item from item where item = '"+validar(item)+"' and id_pregao = '"+validar(id_pregao)+"';")
    cursor.execute(query)
    resultado = cursor.fetchone()
    return str(resultado[0]) if resultado!=None else '-1'

def consultar_id_empenho(uasg:str,pregao:str,nota_empenho:str):
    """Retorna o id do empenho. Caso não exista retorna o valor -1."""
    id_pregao = consultar_id_pregao(uasg,pregao)
    query=( "select id_empenho from empenho "
            "where id_pregao = '"+validar(id_pregao)+"' "
            "and nota_empenho = '"+validar(nota_empenho)+"';")
    cursor.execute(query)
    resultado = cursor.fetchone()
    return str(resultado[0]) if resultado!=None else '-1'

def consultar_id_fase_carona(fase:str):
    """Retorna o id da fase da carona. Caso não exista retorna o valor -1."""
    query=("select id_fase from carona where nome_fase = '"+validar(fase)+"';")
    cursor.execute(query)
    resultado = cursor.fetchone()
    return str(resultado[0]) if resultado!=None else '-1'

def consultar_id_carona(uasg:str,pregao:str,orgao:str,data:str):
    """Retorna o id da carona. Caso não exista retorna o valor -1."""
    id_orgao = consultar_id_orgao_nome(orgao)
    id_pregao = consultar_id_pregao(uasg,pregao)
    query=( "select id_carona from carona where id_orgao = '"+validar(id_orgao)+"' and "
            "id_pregao = '"+validar(id_pregao)+"' and data_carona = '"+validar(data)+"';")
    cursor.execute(query)
    resultado = cursor.fetchone()
    return str(resultado[0]) if resultado!=None else '-1'

###CONSULTAS-------------------------------------------------------

def consulta_orgaos():
    """Retorna uma lista de todos os órgãos cadastrados e sua respectiva uasg."""
    consulta = []
    cursor.execute('exec sel_orgaos;')
    for row in cursor:
        aux = [row[0],row[1]]
        consulta.append(aux)
    return consulta

def consulta_pregoes(uasg):
    """Consulta os pregões participados por órgão."""
    cursor.execute("exec sel_pregoes @uasg = '"+validar(uasg)+"'")
    consulta = []
    for row in cursor:
        consulta.append(row[0])
    return consulta

def consultar_pregoes_fase(fase:str):
    """Retorna a lista de pregões ordenados pela data filtrado por fase.
    Passado parametro nulo, retorna todos."""
    query = ("select numero_pregao, uasg, data_abertura, nome_orgao from pregao "
            "join orgao on pregao.id_orgao = orgao.id_orgao "
            "where id_fase = (select id_fase from fase_pregao where nome_fase = '"+validar(fase)+"') "
            "order by data_abertura;") if fase != '' else ("select data_abertura, "
            "numero_pregao, uasg, nome_orgao from pregao "
            "join orgao on pregao.id_orgao = orgao.id_orgao "
            "order by data_abertura;")
    cursor.execute(query)
    consulta = []
    for row in cursor:
        if len(row)<1:
            return []
        else:
            consulta.append([str(valor) for valor in row])
    return consulta

def consultar_itens_geral(uasg:str,pregao:str):
    """Retorna uma lista de itens participados em um pregão."""
    cursor.execute(
        "select id_item, item, modelo, quantidade, valor_ofertado, preco_custo, frete, fornecedor, nome_marca from item "
        "join marca on item.id_marca = marca.id_marca "
        "where id_pregao = (select id_pregao from pregao where id_orgao = "
        "(select id_orgao from orgao where uasg = '"+validar(uasg)+"') and numero_pregao = '"+validar(pregao)+"');")
    consulta=[]
    for row in cursor:
        consulta.append([str(valor) for valor in row])
    return consulta

def consultar_itens_ganhos(uasg:str,pregao:str):
    """Retorna uma lista de itens classificados em primeiro lugar."""
    query=("select item.id_item, item, nome_marca, modelo, quantidade, valor_ganho, (quantidade * valor_ganho) as valor_total, preco_custo, frete, fornecedor from item "
        "join marca on item.id_marca = marca.id_marca "
        "join resultado_item on resultado_item.id_item = item.id_item "
        "where id_pregao = (select id_pregao from pregao where id_orgao = "
        "(select id_orgao from orgao where uasg = '"+validar(uasg)+"') and numero_pregao = '"+validar(pregao)+"') "
        " and resultado_item.colocacao = '1'")
    cursor.execute(query)
    consulta=[list(row) for row in cursor.fetchall()]
    return consulta

def consultar_fases_pregoes():
    query="select nome_fase from fase_pregao"
    cursor.execute(query)
    consulta=[row[0].lower() for row in cursor.fetchall()]
    return consulta

def consultar_itens_homologar(uasg:str,pregao:str):
    """Retorna número, quantidade e modelo dos itens de um pregão."""
    id_pregao = consultar_id_pregao(uasg, pregao)
    query = ("select item, modelo, quantidade from item where id_pregao = '"+validar(id_pregao)+"';")
    cursor.execute(query)
    consulta=[list(row) for row in cursor.fetchall()]
    return consulta

def consultar_itens_homologados(uasg:str,pregao:str):
    """Retorna as informações dos itens ganhos para empenhar.
    -> item, marca, modelo, quantidade, valor_ganho"""
    id_pregao = consultar_id_pregao(uasg,pregao)
    query=( "select item.item, nome_marca, modelo, quantidade, valor_ganho from resultado_item "
            "join item on item.id_item = resultado_item.id_item "
            "join marca on item.id_marca = marca.id_marca "
            "where item.id_pregao = '"+validar(id_pregao)+"';")
    cursor.execute(query)
    consulta=[list(row) for row in cursor.fetchall()]
    return consulta

def consultar_fases_empenhos():
    query=("select nome_fase from fase_empenho")
    cursor.execute(query)
    consulta=[row[0].lower() for row in cursor.fetchall()]
    return consulta

def consultar_empenhos_fase(fase:str=''):
    """Retorna dados dos empenhos, passando a fase como argumento a busca será filtrada pela fase."""
    query=( "select numero_pregao, uasg, data_empenho, nota_empenho, sum(quantidade * valor_unitario) from empenho "
            "join pregao on empenho.id_pregao = pregao.id_pregao "
            "join orgao on orgao.id_orgao = pregao.id_orgao "
            "join fase_empenho on fase_empenho.id_fase = empenho.id_fase "
            "join item_empenho on item_empenho.id_empenho = empenho.id_empenho ")
    group = ("group by data_empenho, nota_empenho, uasg, pregao.numero_pregao")
    if(fase!=''):
        query=query+("where fase_empenho.nome_fase = '"+validar(fase)+"' ")
    query=query+group
    cursor.execute(query)
    consulta=[list(row) for row in cursor.fetchall()]
    return consulta

def consultar_fases_carona():
    """Retorna uma lista com as fases para as caronas."""
    query=("select nome_fase from fase_carona")
    cursor.execute(query)
    consulta=[row[0].lower() for row in cursor.fetchall()]
    return consulta

###ALTERAÇÕES-------------------------------------

def alterar_fase_pregao(uasg:str,pregao:str,fase:str):
    """Altera a fase de determinado pregão, necessário passar todos os argumentos."""
    query = "select id_fase from fase_pregao where nome_fase = '"+validar(fase)+"';"
    cursor.execute(query)
    fase = str(cursor.fetchone()[0])
    query = ("update pregao set id_fase = '"+fase+"'"
            "where numero_pregao = '"+validar(pregao)+"' and id_orgao = (select id_orgao from orgao where orgao.uasg ='"+validar(uasg)+"');")
    cursor.execute(query)
    cursor.commit()

###INSERÇÕES---------------------------------------

def inserir_items_planilha(uasg, pregao, item, modelo, valor, quantidade, fornecedor, marca, categoria,preco_custo, frete):
    """Insere os itens do pregão."""
    id_pregao = consultar_id_pregao(uasg, pregao)
    query = "exec dbo.sp_inserir_item @frete="+validar(frete)+", @preco_custo="+validar(preco_custo)+", @item="+validar(item)+', @modelo="'+validar(modelo)+'", @valor='+validar(valor)+", @quantidade="+validar(quantidade)+", @id_pregao="+str(id_pregao)+', @fornecedor="'+validar(fornecedor)+'", @marca="'+validar(marca)+'", @categoria="'+validar(categoria)+'";'
    cursor.execute(query)
    conn.commit()

def inserir_pregao(uasg:str,pregao:str,data:str,fase:str):
    """Insere o pregão com base no id do órgão e no nome da fase."""
    id_orgao = consultar_id_orgao(uasg)
    if consultar_id_pregao(uasg,pregao)=='-1':
        query = ("insert into pregao (id_orgao, numero_pregao, data_abertura, id_fase) "
                "values ('"+validar(id_orgao)+"','"+validar(pregao)+"',convert(datetime,'"+validar(data)+":00',120),(select id_fase from fase_pregao where nome_fase = '"+validar(fase)+"'));")
        cursor.execute(query)
        conn.commit()
        return True
    else:
        return False

def inserir_orgao(uasg:str,orgao:str):
    """Insere um novo órgão no banco de dados."""
    if consultar_id_orgao(uasg)!='-1':
        query=("insert into orgao (nome_orgao, uasg) VALUES ('"+validar(uasg)+"','"+validar(orgao)+"');")
        cursor.execute(query)
        conn.commit()
        return True
    else:
        return False

def inserir_item_ganho(uasg:str,pregao:str,item:str,valor:str):
    """Insere o item como ganho no banco de dados."""
    id_item = consultar_id_item(item,uasg,pregao)
    query=( "insert into resultado_item (colocacao, valor_ganho, id_item) values ("
            "'1','"+validar(valor)+"','"+validar(id_item)+"')")
    cursor.execute(query)
    conn.commit()

def inserir_carona(uasg:str,pregao:str,data:str,orgao:str,fase:str=''):
    """Insere uma nova carona no banco de dados."""
    id_pregao = consultar_id_pregao(uasg,pregao)
    id_orgao = consultar_id_orgao_nome(orgao)
    if fase == '':
        id_fase = '1'
    else:
        id_fase = consultar_id_fase_carona(fase)
    query=( "insert into carona (data_carona, id_pregao, id_orgao, id_fase) "
            "values ('"+validar(data)+"', '"+id_pregao+"', '"+id_orgao+"','"+id_fase+"')")
    try:
        cursor.execute(query)
        conn.commit()
        return True
    except:
        return False

def inserir_itens_em_carona(uasg:str,pregao:str,orgao:str,data:str,itens:list):
    """Insere os itens na carona do referido pregão
    Cada item da lista deve conter código, quantidade e valor.
    Necessariamente nessa ordem."""
    id_carona = consultar_id_carona(uasg,pregao,orgao,data)
    try:
        for item in itens:
            id_item = consultar_id_item(item[0],uasg,pregao)
            query=( "insert into item_carona (id_item, id_carona, quantidade, valor_ganho) "
                    "values ('"+validar(id_item)+"','"+validar(id_carona)+"','"+validar(item[1])+"','"+validar(item[2])+"')")
            cursor.execute(query)
        else:
            conn.commit()
            return True
    except:
        return False

def inserir_empenho_solicitado(uasg:str,pregao:str,data:str,nota:str):
    """Insere um empenho no banco de dados na fase Solicitado."""
    id_orgao = consultar_id_orgao(uasg)
    id_pregao = consultar_id_pregao(uasg,pregao)
    query = (   "insert into empenho (data_empenho,nota_empenho, id_pregao, id_fase, id_orgao) values"
                "('"+validar(data)+"','"+validar(nota)+"','"+validar(id_pregao)+"','1','"+validar(id_orgao)+"')")
    try:
        cursor.execute(query)
        conn.commit()
        return True
    except:
        return False

def inserir_itens_em_empenho(uasg:str,pregao:str,nota_empenho:str,itens:list):
    """Insere itens em uma nota de empenho.
    Cada item da lista deve conter código, quantidade, valor.
    Necessariamente nessa ordem."""
    id_empenho = consultar_id_empenho(uasg,pregao,nota_empenho)
    try:
        for item in itens:
            id_item = consultar_id_item(item[0],uasg,pregao)
            query = (   "insert into item_empenho (quantidade, valor_unitario, id_empenho, id_item) "
                        "values ('"+validar(item[1])+"','"+validar(item[2])+"','"+validar(id_empenho)+"','"+validar(id_item)+"');")
            cursor.execute(query)
            conn.commit()
        else:
            return True
    except:
        return False