import pyodbc
import credentials as dbi
conn = pyodbc.connect('Driver='+dbi.driver+';''Server='+dbi.server+';''Database='+dbi.database+';''Trusted_Connection='+dbi.trusted+';UID='+dbi.uid+';PWD='+dbi.pwd+';')

cursor = conn.cursor()

def validar(campo):#NÃO PERMITE SQL INJECTION
    campo = str(campo).replace("'","").replace("--","")
    return campo

###CONSULTAS A IDENTIFICADORES

def consultar_id_orgao(uasg):
    """Retorna o código identificador do pregão caso ele exista, senão retorna -1."""
    cursor.execute("select id_orgao from orgao where uasg = '"+validar(uasg)+"';")
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

def consultar_id_fase_pregao(fase:str):
    """Retorna o id da fase do pregão. Caso não exista, retorna -1"""
    query=("select id_fase from fase_pregao where nome_fase = '"+validar(fase)+"';")
    cursor.execute(query)
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
    query=("select id_fase from fase_carona where nome_fase = '"+validar(fase)+"';")
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

def consultar_id_fase_empenho(fase:str):
    """Retorna o id da fase do empenho. Caso não exista retorna o valor -1."""
    query=("select id_fase from fase_empenho where nome_fase = '"+validar(fase)+"'")
    cursor.execute(query)
    resultado = cursor.fetchone()
    return str(resultado[0]) if resultado != None else '-1'

###CONSULTAS

def consultar_todos_orgaos():
    """Retorna uma lista de todos os órgãos cadastrados."""
    query=("select nome_orgao from orgao order by nome_orgao asc;")
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]

def consultar_todos_uasgs():
    """Retorna uma lista ordenada dos uasgs contidos no banco de dados."""
    query=("select uasg from orgao order by uasg asc;")
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]

def consultar_pregoes_fase(fase:str=''):
    """Retorna a lista de pregões ordenados pela data filtrado por fase.
    Passado parametro nulo, retorna todos."""
    query = (
    """select
        id_pregao,
        numero_pregao,
        uasg,
        data_abertura,
        nome_orgao
    from pregao
    join orgao on pregao.id_orgao = orgao.id_orgao """)
    if(fase != ''):
        id_fase = consultar_id_fase_pregao(fase)
        query = query + ("where id_fase = '"+validar(id_fase)+"' ")
    query = query+("order by data_abertura;")
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
        "select item, nome_marca, modelo, quantidade, valor_ofertado, preco_custo, frete, fornecedor, id_item from item "
        "join marca on item.id_marca = marca.id_marca "
        "where id_pregao = (select id_pregao from pregao where id_orgao = "
        "(select id_orgao from orgao where uasg = '"+validar(uasg)+"') and numero_pregao = '"+validar(pregao)+"');")
    consulta=[]
    for row in cursor:
        consulta.append([str(valor) for valor in row])
    return consulta

def consultar_fases_pregoes():
    query="select nome_fase from fase_pregao"
    cursor.execute(query)
    consulta=[row[0].lower() for row in cursor.fetchall()]
    return consulta

def consultar_itens_homologados(id_pregao:str):
    """Retorna as informações dos itens ganhos e a quantidade disponível para empenhar.
    id, item, marca, modelo, quantidade, valor_ofertado"""
    query=(
    """select
        i.id_item,
        i.item,
        nome_marca,
        i.modelo,
        total.quantidade,
        i.valor_ofertado
    from item as i
        join (select id_item, sum(quantidade) as quantidade
            from (select id_item, quantidade*(-1) as quantidade
            from item_empenho
            union all
            select
                id_item,
                quantidade*(-1) as quantidade
            from item_carona
            union all
            select
                id_item,
                quantidade
            from item) t group by id_item) as total on total.id_item = i.id_item 
    join marca on i.id_marca = marca.id_marca
	where i.colocacao = 1 and i.id_pregao = '"""+validar(id_pregao)+"';")
    cursor.execute(query)
    consulta=[list(row) for row in cursor.fetchall()]
    return consulta

def consultar_fases_empenhos():
    query=("select nome_fase from fase_empenho")
    cursor.execute(query)
    consulta=[row[0].lower() for row in cursor.fetchall()]
    return consulta

def consultar_empenhos_pela_fase(fase:str=''):
    """Retorna dados dos empenhos, passando a fase como argumento a busca será filtrada pela fase."""
    query=(
    """select
        empenho.id_empenho,
        numero_pregao,
        uasg,
        nota_empenho,
        format (data_empenho,'dd/MM/yyyy') as data_empenho,
        format (data_entrega,'dd/MM/yyyy') as data_entrega,
        sum(quantidade * valor_ofertado)
    from empenho 
    join pregao on empenho.id_pregao = pregao.id_pregao 
    join orgao on orgao.id_orgao = pregao.id_orgao 
    join fase_empenho on fase_empenho.id_fase = empenho.id_fase 
    join item_empenho on item_empenho.id_empenho = empenho.id_empenho """)
    group = ("group by empenho.id_empenho, data_empenho, nota_empenho, data_entrega, uasg, pregao.numero_pregao")
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

def consultar_caronas_pela_fase(fase:str=''):
    """Retorna dados das caronas, passando a fase como argumento a busca será filtrada pela fase."""
    query=( "select c.id_carona, numero_pregao, o.uasg, data_carona, og.nome_orgao from carona as c "
            "join pregao as p on p.id_pregao = c.id_pregao "
            "join orgao as o on o.id_orgao = p.id_orgao "
            "join orgao as og on og.id_orgao = c.id_orgao "
            "join item_carona as ic on ic.id_carona = c.id_carona "
            "join fase_carona as fc on fc.id_fase = c.id_fase ")
    group = ("group by c.id_carona, numero_pregao, o.uasg, data_carona, og.nome_orgao")
    if(fase!=''):
        query=query+("where fc.nome_fase = '"+validar(fase)+"' ")
    query=query+group
    cursor.execute(query)
    consulta=[list(row) for row in cursor.fetchall()]
    return consulta

###CONSULTAS PELO ID DO PREGÃO

def consultar_pasta_pregao(id_pregao:str):
    """Retorna o padrão das data_pregao_uasg para o pregão."""
    query=(
    """select
        format(data_abertura,'yyyy-MM-dd'),
        numero_pregao,
        uasg
    from pregao
    inner join orgao on orgao.id_orgao = pregao.id_orgao where id_pregao = '"""+validar(id_pregao)+"';")
    cursor.execute(query)
    resultado = [list(row) for row in cursor.fetchall()]
    return '_'.join(resultado[0])

def consultar_pregoes_do_orgao(id_orgao:str):
    """Retorna uma lista com os pregões registrados para o órgão."""
    query=("select numero_pregao from pregao where id_orgao = '"+validar(id_orgao)+"' order by numero_pregao asc;")
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]

def consultar_dados_pregao(id_pregao:str):
    """Retorna os dados gerais de um pregão.\n
    numero, uasg, órgão, data de abertura, data da ata, fase."""
    query=(
        """select
            p.id_pregao,
            p.numero_pregao,
            o.uasg,
            o.nome_orgao,
            format (p.data_abertura,'dd/MM/yyyy HH:mm') as data_abertura,
            format (p.data_ata, 'dd/MM/yyyy HH:mm') as data_ata,
            fp.nome_fase from pregao as p
        join orgao as o on o.id_orgao = p.id_orgao
        join fase_pregao as fp on fp.id_fase = p.id_fase
        where p.id_pregao = '"""+validar(id_pregao)+"';")
    cursor.execute(query)
    consulta=[list(row) for row in cursor.fetchall()]
    return consulta[0]

def consultar_dados_gerais_pregao(id_pregao:str):
    """Retorna os dados gerais do pregão."""
    query=("""
    select
        format (p.data_abertura,'dd/MM/yyyy HH:mm'),
        nome_fase,
        count(i.id_item) as itens_homologados,
        sum(i.quantidade * i.valor_ofertado) as total_homologado,
        e.empenhos,
        emp.total as total_empenhado
        from pregao as p
    left join fase_pregao as fp on fp.id_fase = p.id_fase
    left join item as i on i.id_pregao = p.id_pregao
    left join (select id_pregao, count(id_empenho) as empenhos from empenho group by id_pregao) as e on e.id_pregao = p.id_pregao
    left join (
        select p.id_pregao, e.empenhos, sum(ie.valor_ofertado * ie.quantidade) as total from pregao as p
        join (select id_empenho, id_pregao, count(id_empenho) as empenhos from empenho group by id_empenho, id_pregao) as e on e.id_pregao = p.id_pregao
        join item_empenho as ie on ie.id_empenho = e.id_empenho
        group by p.id_pregao, e.id_pregao, e.empenhos) as emp on emp.id_pregao = p.id_pregao
    where p.id_pregao = '"""+validar(id_pregao)+"""'
    group by data_abertura, nome_fase, e.empenhos, emp.total""")
    cursor.execute(query)
    consulta=[list(row) for row in cursor.fetchall()]
    print(consulta)
    return consulta[0]

def consultar_itens_participados(id_pregao:str):
    """Retorna uma lista de itens participados em um pregão."""
    query=(
        """select i.id_item, i.item, nome_marca, modelo, i.quantidade, i.valor_ofertado, 
        i.preco_custo, i.frete, i.fornecedor from item as i
        join marca as m on m.id_marca = i.id_marca
        where i.id_pregao = '"""+validar(id_pregao)+"';")
    cursor.execute(query)
    consulta=[list(row) for row in cursor.fetchall()]
    return consulta

def consultar_itens_homologar(id_pregao:str):
    """Retorna número, quantidade e modelo dos itens de um pregão."""
    query = (
    """select
        item,
        nome_marca,
        modelo,
        quantidade,
        valor_ofertado
    from item
    inner join marca on marca.id_marca = item.id_marca
    where id_pregao = '"""+validar(id_pregao)+"';")
    cursor.execute(query)
    return [list(row) for row in cursor.fetchall()]

def consultar_itens_homologados_id(id_pregao:str):
    """Retorna uma lista de itens ganhos para determinado pregão."""
    query=(
    """select
        i.id_item,
        i.item,
        nome_marca,
        i.modelo,
        i.valor_ofertado,
        i.quantidade,
        (case when qnts.empenho is null then 0 else qnts.empenho end) as empenho,
        (case when qnts.carona is null then 0 else qnts.carona end) as carona
        from item as i
    left join
        (select
            id_item,
            sum(carona) as carona,
            sum(empenho) as empenho from
                (select
                    id_item,
                    carona,
                    sum(empenho) as empenho from
                        (select
                            item_empenho.id_item,
                            cast(0 as int) as carona,
                            quantidade as empenho from item_empenho) as emp group by id_item, carona
                        union all
                        select
                            id_item,
                            sum(carona),
                            empenho from
                            (select
                                item_carona.id_item,
                                quantidade as carona,
                                cast(0 as int) as empenho
                            from item_carona) as car group by id_item, empenho) as total group by id_item)
                            as qnts on qnts.id_item = i.id_item
    join marca on marca.id_marca = i.id_marca where id_pregao = '"""+validar(id_pregao)+"' and i.colocacao = 1;")
    cursor.execute(query)
    consulta=[list(row) for row in cursor.fetchall()]
    return consulta

def consultar_itens_empenhados_id(id_pregao:str):
    """Retorna as informações dos itens do pregão que já foram empenhados."""
    query=(
    """select
        e.id_empenho,
        i.item,
        nome_marca,
        (case when ie.modelo is null then i.modelo else ie.modelo end),
        ie.quantidade,
        ie.valor_ofertado,
        (case when ie.custo_unitario is null then 0 else ie.custo_unitario end) as custo,
        format(e.data_empenho,'dd/MM/yyyy'),
        format(e.data_entrega,'dd/MM/yyyy'),
        e.nota_empenho,
        nome_fase
    from item_empenho as ie
    join empenho as e on e.id_empenho = ie.id_empenho
    join item as i on i.id_item = ie.id_item
    join marca as m on (case when ie.id_marca is null then (i.id_marca) else (ie.id_marca) end) = m.id_marca
    join fase_empenho as fs on fs.id_fase = e.id_fase
    join pregao as p on p.id_pregao = i.id_pregao
    where p.id_pregao = '"""+validar(id_pregao)+"' order by e.data_empenho desc;")
    cursor.execute(query)
    consulta=[list(row) for row in cursor.fetchall()]
    return consulta

def consultar_itens_carona(id_pregao:str):
    """Retorna uma lista de itens aceitos em carona para determinado pregão."""
    query=(
    """select
        c.id_carona,
        i.item,
        nome_marca,
        i.modelo,
        ic.quantidade,
		ie.quantidade as empenho,
        ic.valor_ofertado,
        format (c.data_carona,'dd/MM/yyyy'),
        nome_orgao,
        nome_fase
        from carona as c
    join item_carona as ic on ic.id_carona = c.id_carona
    left join empenho as e on (e.id_carona = c.id_carona)
	left join item_empenho as ie on (ie.id_item = ic.id_item and e.id_empenho = ie.id_empenho)
    join item as i on i.id_item = ic.id_item
    join marca on marca.id_marca = i.id_marca
    join fase_carona as fc on fc.id_fase=c.id_fase
    join orgao as o on o.id_orgao = c.id_orgao 
    where c.id_pregao = '"""+validar(id_pregao)+"' order by c.data_carona desc;""")
    cursor.execute(query)
    return [list(row) for row in cursor.fetchall()]

###CONSULTAS PELO ID CARONA

def consultar_id_pregao_da_carona(id_carona:str)->str:
    """Retorna o id do pregão da carona."""
    query=(
    """select
        id_pregao
    from carona where id_carona = '"""+validar(id_carona)+"';")
    cursor.execute(query)
    return [list(row) for row in cursor.fetchall()][0][0]

###CONSULTAS PELO ID EMPENHO

def consultar_id_pregao_do_empenho(id_empenho:str)->str:
    """Retorna o id do pregão do empenho."""
    query=(
    """select
        id_pregao
    from empenho where id_empenho = '"""+validar(id_empenho)+"';")
    cursor.execute(query)
    return [list(row) for row in cursor.fetchall()][0][0]

###PROCURAS

def procurar_uasg(uasg:str):
    """Retorna uma lista de uasgs parecidos com o parametro de entrada."""
    query=("select uasg from orgao where uasg like '"+validar(uasg)+"%' order by uasg;")
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]

def procurar_orgao(orgao:str):
    """Retorna uma lista de órgão cujos nome são parecidos com o parametro de entrada."""
    query=("select nome_orgao from orgao where nome_orgao like '%"+validar(orgao)+"%';")
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]

def procurar_orgao_com_uasg(uasg:str):
    """Retorna o nome do órgão com uma procura pelo seu código uasg."""
    query=("select nome_orgao from orgao where uasg = '"+validar(uasg)+"';")
    cursor.execute(query)
    resultado = cursor.fetchone()
    return resultado[0] if resultado != None else '-1'

def procurar_uasg_com_nome_orgao(orgao:str):
    """Retorna o código uasg com uma procura pelo nome do órgão."""
    query=("select uasg from orgao where nome_orgao = '"+validar(orgao)+"';")
    cursor.execute(query)
    resultado = cursor.fetchone()
    return resultado[0] if resultado != None else '-1'

def procurar_pregoes(pregao:str,uasg:str):
    """Retorna o número dos pregões participados pelo uasg indicado."""
    id_orgao = consultar_id_orgao(uasg)
    query=(
    """select
        numero_pregao
    from pregao
    where numero_pregao like '%"""+validar(pregao)+"""%' and id_orgao = '"""+validar(id_orgao)+"';")
    cursor.execute(query)
    resultado = [list(row) for row in cursor.fetchall()]
    return resultado

###ALTERAÇÕES

def alterar_fase_pregao(uasg:str,pregao:str,fase:str):
    """Altera a fase de determinado pregão, necessário passar todos os argumentos."""
    id_fase = consultar_id_fase_pregao(fase)
    if id_fase == '-1':
        return False
    try:
        query = ("update pregao set id_fase = '"+id_fase+"'"
                "where numero_pregao = '"+validar(pregao)+"' and id_orgao = (select id_orgao from orgao where orgao.uasg ='"+validar(uasg)+"');")
        cursor.execute(query)
        cursor.commit()
        return True
    except:
        return False

def alterar_data_arp(id_pregao:str,data:str):
    try:
        query = ("update pregao set data_ata = '"+validar(data)+"' "
                "where id_pregao = '"+validar(id_pregao)+"';")
        cursor.execute(query)
        cursor.commit()
        return True
    except:
        return False
    
def alterar_data_abertura(id_pregao:str,data:str):
    try:
        query= ("update pregao set data_abertura = '"+validar(data)+"' "
                "where id_pregao = '"+validar(id_pregao)+"';")
        cursor.execute(query)
        cursor.commit()
        return True
    except:
        return False

###INSERÇÕES

def inserir_itens_planilha(uasg, pregao, item, modelo, valor, quantidade, fornecedor, marca, categoria,preco_custo, frete):
    """Insere os itens do pregão."""
    id_pregao = consultar_id_pregao(uasg, pregao)
    if frete == "None": frete = 0.0
    query = ("exec dbo.sp_inserir_item @frete="+validar(frete)+
            ", @preco_custo="+validar(preco_custo)+
            ", @item="+validar(item)+
            ", @modelo='"+validar(modelo)+
            "', @valor="+validar(valor)+
            ", @quantidade="+validar(quantidade)+
            ", @id_pregao="+str(id_pregao)+
            ", @fornecedor='"+validar(fornecedor)+
            "', @marca='"+validar(marca)+
            "', @categoria='"+validar(categoria)+"';")
    cursor.execute(query)
    conn.commit()
    
def inserir_pregao(uasg:str,pregao:str,data:str,fase:str):
    """Insere o pregão com base no id do órgão e no nome da fase."""
    id_orgao = consultar_id_orgao(uasg)
    id_fase = consultar_id_fase_pregao(fase)
    if consultar_id_pregao(uasg,pregao)=='-1':
        query = ("insert into pregao (id_orgao, numero_pregao, data_abertura, id_fase) "
                "values ('"+validar(id_orgao)+"','"+validar(pregao)+"',convert(datetime,'"+validar(data)+":00',120),'"+validar(id_fase)+"');")
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

def inserir_itens_ganho(uasg:str,pregao:str,itens:list):
    """Insere o item como ganho no banco de dados."""
    for item in itens:
        id_item = consultar_id_item(item[0],uasg,pregao)
        if (id_item == '-1'):
            return False
        query=( "update item set colocacao = 1, valor_ofertado = '"+validar(item[1])+"' where id_item = '"+validar(id_item)+"';")
        cursor.execute(query)
    try:
        conn.commit()
        return True
    except:
        return False

def inserir_carona(uasg:str,pregao:str,data:str,orgao:str,fase:str='Aceita'):
    """Insere uma nova carona no banco de dados. Quando a fase não for passada, será inserido como Aceita"""
    id_pregao = consultar_id_pregao(uasg,pregao)
    id_orgao = consultar_id_orgao_nome(orgao)
    id_fase = consultar_id_fase_carona(fase)
    if('-1' in [id_pregao,id_orgao,id_fase]):
        return False
    query=( "insert into carona (data_carona, id_pregao, id_orgao, id_fase) "
            "values ('"+validar(data)+"', '"+validar(id_pregao)+"', '"+validar(id_orgao)+"','"+validar(id_fase)+"')")
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
            query=( "insert into item_carona (id_item, id_carona, quantidade, valor_ofertado) "
                    "values ('"+validar(id_item)+"','"+validar(id_carona)+"','"+validar(item[1])+"','"+validar(item[2])+"')")
            cursor.execute(query)
        else:
            conn.commit()
            return True
    except:
        return False

def inserir_empenho(uasg:str,pregao:str,data:str,nota:str,fase:str='Solicitado'):
    """Insere um empenho no banco de dados, caso a fase não seja especificada, será inserido como Solicitado."""
    id_orgao = consultar_id_orgao(uasg)
    id_pregao = consultar_id_pregao(uasg,pregao)
    id_fase = consultar_id_fase_empenho(fase)
    if( '-1' in [id_orgao,id_pregao,id_fase]): return False
    query = (   "insert into empenho (data_empenho,nota_empenho, id_pregao, id_fase, id_orgao) values"
                "('"+validar(data)+"','"+validar(nota)+"','"+validar(id_pregao)+"','"+validar(id_fase)+"','"+validar(id_orgao)+"')")
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
            id_item = consultar_id_item(item[0], uasg, pregao)
            query = (   "insert into item_empenho (quantidade, valor_ofertado, id_empenho, id_item) "
                        "values ('"+validar(item[1])+"','"+validar(item[2])+"','"+validar(id_empenho)+"','"+validar(id_item)+"');")
            cursor.execute(query)
            conn.commit()
        else:
            return True
    except:
        return False

def inserir_entrega_de_empenho(id_empenho:str,data:str):
    """Insere a data da entrega para o referido pregão."""
    query=("update empenho set data_entrega='"+validar(data)+"', id_fase='2' where id_empenho = '"+validar(id_empenho)+"';")
    try:
        cursor.execute(query)
        conn.commit()
        return True
    except:
        return False

