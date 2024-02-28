from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from boiforte.settings import BOIFORTE_DB_HOST, BOIFORTE_DB_PASS, BOIFORTE_DB_PORT, BOIFORTE_DB_USER, BOIFORTE_DB_SID
import oracledb
import pandas as pd

@login_required
def index_siagri(request):
    # Configurar os parâmetros de conexão
    # dsn_tns = cx_Oracle.makedsn(BOIFORTE_DB_HOST, BOIFORTE_DB_PORT, BOIFORTE_DB_SID)
    # search = request.GET.get('search')  

    # # Estabelecer a conexão
    # try:
    #     conexao = cx_Oracle.connect(BOIFORTE_DB_USER, BOIFORTE_DB_PASS, dsn_tns)

    #     # Criar um cursor
    #     cursor = conexao.cursor()
        
    #     # Consulta SQL
    #     consulta_sql = f"SELECT RAZA_TRA, CGC_TRA FROM TRANSAC"
        
    #     # Executar a consulta
    #     cursor.execute(consulta_sql)
        
    #     # Recuperar os resultados como uma lista de dicionários
    #     #colunas = ["nome", "cgc"]
    #     colunas = [col[0] for col in cursor.description]
    #     resultados = [dict(zip(colunas, row)) for row in cursor.fetchall()]
        
    #     # Fechar o cursor e a conexão
    #     cursor.close()
    #     conexao.close()
    #     return render(request, 'index_siagri.html', {'dados': resultados}) 
        
    # except cx_Oracle.DatabaseError as e:
    #     print("Erro ao conectar ao banco de dados:", e)
    #     return render(request, 'index_siagri.html')
    
    return render(request, 'index_siagri.html')

import cx_Oracle
@login_required
def siagri_contas_pagar(request):
    
   
    sql_query = "SELECT RAZA_TRA FROM TRANSAC"
    dsn = cx_Oracle.makedsn(BOIFORTE_DB_HOST, BOIFORTE_DB_PORT, service_name=BOIFORTE_DB_SID)  # ou SID se estiver usando SID em vez de serviço

    
    # Estabelecer conexão
    conn = cx_Oracle.connect(user=BOIFORTE_DB_USER, password=BOIFORTE_DB_PASS, dsn=dsn)

    # Criar um cursor
    cursor = conn.cursor()

    # Exemplo de execução de uma consulta
    cursor.execute(sql_query)
    
    cursor = conn.cursor()
    cursor.execute(sql_query)
    #colunas = ["nome", "cgc"]
    colunas = [col[0] for col in cursor.description]
    resultados = [dict(zip(colunas, row)) for row in cursor.fetchall()]

    return render(request, 'pagar.html', {'resultados': resultados})



@login_required
def siagri_contas_receber(request):



    return render(request, 'receber.html')