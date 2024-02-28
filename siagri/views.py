from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from boiforte.settings import BOIFORTE_DB_HOST, BOIFORTE_DB_PASS, BOIFORTE_DB_PORT, BOIFORTE_DB_USER, BOIFORTE_DB_SID, ORACLE_CLIENT
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

    dsn = cx_Oracle.makedsn(BOIFORTE_DB_HOST, BOIFORTE_DB_PORT, service_name=BOIFORTE_DB_SID)
    conn = cx_Oracle.connect(user=BOIFORTE_DB_USER, password=BOIFORTE_DB_PASS, dsn=dsn)

    sql_query = f"""
    SELECT SUM(SALD_CORR) AS SOMA_SALDO_CORR 
    FROM (SELECT CPG.CODI_TRA, TRA.RAZA_TRA, CPG.CODI_EMP, PAG.NPAR_PAG, CPG.DMOV_CPG, PAG.DVEN_PAG, PAG.CODI_POR, 
            (SELECT VALOR from  table(VALOR_ABERTO_PAGAR(PAG.CTRL_PAG))) as SALD_PAG 
            , TDO.TIPO_TDO,  
  
            CASE 
                WHEN TDO.TIPO_TDO = 'C' THEN (SELECT VALOR FROM TABLE(VALOR_ABERTO_PAGAR(PAG.CTRL_PAG))) * -1
                ELSE (SELECT VALOR FROM TABLE(VALOR_ABERTO_PAGAR(PAG.CTRL_PAG)))
            END AS SALD_CORR

        from PAGAR PAG 
        join CABPAGAR CPG on (CPG.CTRL_CPG = PAG.CTRL_CPG) 
        join TRANSAC  TRA on (TRA.CODI_TRA = CPG.CODI_TRA) 
        join TIPDOC   TDO on (TDO.CODI_TDO = CPG.CODI_TDO) 

        where not exists(SELECT * 
                        from RCPPAGAR RCP 
                        where (RCP.CTRL_PAG = PAG.CTRL_PAG) 
                        and (RCP.TIPO_RCP = 'R') 
                        and (RCP.VLOR_RCP = PAG.VLOR_PAG)) 
        AND (CPG.DMOV_CPG BETWEEN TO_DATE('01-01-1900', 'DD-MM-YYYY') AND TO_DATE('30-12-2999', 'DD-MM-YYYY'))
        AND (PAG.DVEN_PAG BETWEEN TO_DATE('01-01-1900', 'DD-MM-YYYY') AND TO_DATE('30-12-2999', 'DD-MM-YYYY'))  
        AND (TDO.CODI_TDO in ('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','18','19','23','25','26','27','28','29','30','31','32','33','34','35','36','37','40','41','50','51','60','61','101','102','103','104','105','106','107','108','110','10000001','10000003','10000004','10000005','10000006','10000007','10000008','10000009','10000010','10000011','10000012','30000001','30000002'))   
        AND (CPG.CODI_EMP in ('1','2','3','4','5','6'))   AND ((SELECT VALOR from  table(VALOR_ABERTO_PAGAR(PAG.CTRL_PAG))) > 0)
    ) T    
    """

    sql = f"""

        SELECT 
            SUM(SALD_CORR) AS SOMA_SALD_CORR
        FROM (
            SELECT 
                CASE 
                    WHEN TDO.TIPO_TDO = 'C' THEN (SELECT VALOR FROM TABLE(VALOR_ABERTO_PAGAR(PAG.CTRL_PAG))) * -1
                    ELSE (SELECT VALOR FROM TABLE(VALOR_ABERTO_PAGAR(PAG.CTRL_PAG)))
                END AS SALD_CORR
            FROM 
                PAGAR PAG 
                JOIN CABPAGAR CPG ON (CPG.CTRL_CPG = PAG.CTRL_CPG) 
                JOIN TRANSAC  TRA ON (TRA.CODI_TRA = CPG.CODI_TRA) 
                JOIN TIPDOC   TDO ON (TDO.CODI_TDO = CPG.CODI_TDO) 
            WHERE 
                NOT EXISTS (
                    SELECT * 
                    FROM RCPPAGAR RCP 
                    WHERE 
                        (RCP.CTRL_PAG = PAG.CTRL_PAG) 
                        AND (RCP.TIPO_RCP = 'R') 
                        AND (RCP.VLOR_RCP = PAG.VLOR_PAG)
                ) 
                AND (CPG.DMOV_CPG BETWEEN TO_DATE('01-01-1900', 'DD-MM-YYYY') AND TO_DATE('30-12-2999', 'DD-MM-YYYY'))
                AND (PAG.DVEN_PAG BETWEEN TO_DATE('01-01-1900', 'DD-MM-YYYY') AND TO_DATE('30-12-2999', 'DD-MM-YYYY'))  
                AND (TDO.CODI_TDO IN ('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','18','19','23','25','26','27','28','29','30','31','32','33','34','35','36','37','40','41','50','51','60','61','101','102','103','104','105','106','107','108','110','10000001','10000003','10000004','10000005','10000006','10000007','10000008','10000009','10000010','10000011','10000012','30000001','30000002'))   
                AND (CPG.CODI_EMP IN ('1','2','3','4','5','6'))   
                AND ((SELECT VALOR FROM TABLE(VALOR_ABERTO_PAGAR(PAG.CTRL_PAG))) > 0)
        ) T

"""

    # Criar um cursor
    cursor = conn.cursor()

    # Exemplo de execução de uma consulta
    cursor.execute(sql)
    

    #colunas = ["nome", "cgc"]
    colunas = [col[0] for col in cursor.description]
    resultados = [dict(zip(colunas, row)) for row in cursor.fetchall()]

    return render(request, 'pagar.html', {'resultados': resultados})



@login_required
def siagri_contas_receber(request):



    return render(request, 'receber.html')