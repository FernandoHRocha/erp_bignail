import pyodbc
import credentials as dbi
conn = pyodbc.connect('Driver='+dbi.driver+';''Server='+dbi.server+';''Database='+dbi.database+';''Trusted_Connection='+dbi.trusted+';UID='+dbi.uid+';PWD='+dbi.pwd+';')

cursor = conn.cursor()

def validar(campo):#NÃO PERMITE SQL INJECTION
    campo = str(campo).replace("'","").replace("--","")
    return campo

def consulta_orgaos():
    """Retorna uma lista de todos os órgãos cadastrados e sua respectiva uasg."""
    consulta = []
    cursor.execute('exec sel_orgaos;')
    for row in cursor:
        aux = []
        aux.append(row[1])
        aux.append(row[0])
        consulta.append(aux)
    return consulta

def consultaNomeOrgao(uasg):
    cursor.execute("exec sp_getNomeOrgao @uasg = '"+uasg+"'")
    nome =''
    for row in cursor:
        nome = row[0]
    return nome

def listar_pregoes():#LISTA OS PREGÕES PELA DATA DE ABERTURA
    cursor.execute('exec sp_listPregoes')
    pregoes =[]
    for row in cursor:
        aux =[]
        for col in row:
            aux.append(col)
        pregoes.append(aux)
    return pregoes

def consulta_pregoes(uasg):
    cursor.execute("exec sel_pregoes @uasg = '"+uasg+"'")
    pregoes = []
    for row in cursor:
        pregoes.append(row[0])
    return pregoes

def inserir_orgao(uasg, orgao):
    query="INSERT INTO orgao (nome_orgao, uasg) VALUES ('"+ orgao+"','"+ uasg+"');"
    #cursor.execute(query)
    #conn.commit()

def inserir_pregao(uasg, numero, data, fase):#INSERE UM NOVO PREGÃO NO BD
    numero = str(numero)
    while(len(str(numero))<6):
        numero = "0"+numero
    query = "exec dbo.sp_inserir_pregao @uasg = "+validar(uasg)+",@pregao ='"+validar(numero)+"',@data = '"+validar(data)+"', @fase = "+validar(fase)+";"
    cursor.execute(query)
    conn.commit()

def obter_id_pregao(uasg, pregao):
    resultado = ''
    query = 'select id_pregao from pregao where pregao.id_orgao = (select id_orgao from orgao where uasg = '+uasg+') and pregao.numero_pregao = '+pregao
    cursor.execute(query)
    for x in cursor:
        resultado = x[0]
    return resultado

def inserir_items_planilha(uasg, pregao, item, modelo, valor, quantidade, fornecedor, marca, categoria,preco_custo, frete):
    id_pregao = obter_id_pregao(uasg, pregao)
    query = "exec dbo.sp_inserir_item @frete="+validar(frete)+", @preco_custo="+validar(preco_custo)+", @item="+validar(item)+', @modelo="'+validar(modelo)+'", @valor='+validar(valor)+", @quantidade="+validar(quantidade)+", @id_pregao="+str(id_pregao)+', @fornecedor="'+validar(fornecedor)+'", @marca="'+validar(marca)+'", @categoria="'+validar(categoria)+'";'
    cursor.execute(query)
    conn.commit()

def consultarCategorias():
    cursor.execute("select nome_categoria as Categoria from categoria order by nome_categoria")
    categorias = []
    for row in cursor:
        categorias.append(row[0])
    return categorias

def consultarMarcas():
    marcas=[]
    cursor.execute('select nome_marca as Marca from marca order by nome_marca')
    for row in cursor:
        marcas.append(row[0])
    return marcas

def consultar_itens_pregao(uasg,pregao):
    id_pregao = obter_id_pregao(uasg, pregao)
    cursor.execute('select item, quantidade, nome_marca, modelo, valor_ofertado, nome_fase from item left join pregao on pregao.id_pregao = item.id_pregao join marca on item.id_marca = marca.id_marca join fase_pregao on pregao.id_fase_pregao = fase_pregao.id_fase_pregao where item.id_pregao = '+str(id_pregao)+';')
    item=[]
    for x in cursor:
        aux=[]
        for y in x:
            aux.append(str(y))
        item.append(aux)
    return item