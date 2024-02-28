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


@login_required
def siagri_contas_pagar(request):
   
    sql_query = "SELECT RAZA_TRA FROM TRANSAC"
    
    params = oracledb.ConnectParams(host=BOIFORTE_DB_HOST, port=BOIFORTE_DB_PORT, service_name=BOIFORTE_DB_SID)
    conn = oracledb.connect(user=BOIFORTE_DB_USER, password=BOIFORTE_DB_PASS, params=params)
    
    cursor = conn.cursor()
    cursor.execute(sql_query)
    #colunas = ["nome", "cgc"]
    colunas = [col[0] for col in cursor.description]
    resultados = [dict(zip(colunas, row)) for row in cursor.fetchall()]

    return render(request, 'pagar.html', {'resultados': resultados})



@login_required
def siagri_contas_receber(request):

    sql_query = f"""
        SELECT
        c.codi_tra as Código_do_Parceiro,
        t.raza_tra as Razão_Social,
        c.codi_emp as codigo_loja,
        c.nume_cbr as N_documento_financeiro_receber,
        c.seri_cbr as Série_documento_contas_receber,
        r.npar_rec as npumero_parcela,
        c.data_cbr as dt_documento_receber,
        r.venc_rec as dt_venc_real_doc_receber,
        r.ven2_rec as dt_venc_impresso_doc_receber,
        r.codi_tco as codigo_tipo_cobranca,
        r.codi_por as codigo_portador,
        r.ctrl_cbr as Controle_tabela_cabrec,
        r.ctrl_rec as controle_tabela_receber,
        r.situ_rec as situacao_documento_receber,
        r.vlor_rec as vlr_parcela_dcoumento_receber,
        (
        SELECT
        valor
        FROM
        TABLE ( valor_aberto_receber(r.ctrl_rec) )
        ) AS valor_aberto_receber,
        td.desc_tdo as descricao_tipo_documento,
        td.tipo_tdo as tipo_documento,
        td.codi_tdo as codigo_tipo_documento,
        p.desc_por as descricao_tipo_documento,
        r.cond_con as codigo_condicao_pagamento,
        r.dpon_rec as desc_pontualidade_receber,
        r.cod1_pes as codigo_vendedor1,
        p1.nome_pes as nome_vendedor1,
        t.tjur_tra as tipo_juridica_fisica,
        t.cgc_tra as CNPJ_CPF,
        tc.desc_tco as descricao_tipo_cobranca,
        r.tjur_rec as tipo_juros,
        r.dini_rec as data_inicial_cobranca,
        r.jatv_rec as juros_ate_vencimento,
        r.japv_rec as juros_apos_vecimento,
        r.dant_rec as desconto_antecipacao,
        r.mult_rec as multa_poratraso,
        mun.desc_mun as cidade,
        mun.esta_mun as estado
        FROM
        cabrec c
        JOIN receber r ON ( c.ctrl_cbr = r.ctrl_cbr )
        LEFT OUTER JOIN propried pro ON ( c.prop_pro = pro.prop_pro )
        JOIN transac t ON ( t.codi_tra = c.codi_tra )
        LEFT OUTER JOIN limitecr lcr ON ( t.codi_tra = lcr.codi_tra )
        JOIN tipdoc td ON ( td.codi_tdo = c.codi_tdo )
        LEFT OUTER JOIN tipcob tc ON ( r.codi_tco = tc.codi_tco )
        LEFT OUTER JOIN cliente cl ON ( cl.codi_tra = t.codi_tra )
        LEFT OUTER JOIN indexador i ON ( i.codi_ind = r.codi_ind )
        LEFT OUTER JOIN conta ON ( r.codi_con = conta.codi_con )
        LEFT OUTER JOIN agenban a ON ( a.codi_age = conta.codi_age )
        LEFT OUTER JOIN banco b ON ( a.codi_ban = b.codi_ban )
        LEFT OUTER JOIN portador p ON ( r.codi_por = p.codi_por )
        LEFT JOIN pessoal p1 ON ( p1.codi_pes = r.cod1_pes )
        LEFT OUTER JOIN boleto bl ON ( bl.ctrl_bol = r.ctrl_bol )
        LEFT OUTER JOIN condicao cd ON ( r.cond_con = cd.cond_con )
        LEFT OUTER JOIN vendedorcli vd ON ( c.codi_tra = vd.codi_tra
        AND c.codi_emp = vd.codi_emp )
        LEFT OUTER JOIN vendedor cv1 ON ( cv1.codi_pes = vd.cod1_pes )
        LEFT OUTER JOIN vendedor cv2 ON ( cv2.codi_pes = vd.cod2_pes )
        LEFT OUTER JOIN vendedor cav1 ON ( cav1.codi_pes = r.cod1_pes )
        LEFT OUTER JOIN vendedor cav2 ON ( cav2.codi_pes = r.cod2_pes )
        LEFT OUTER JOIN municipio mun ON ( mun.codi_mun = t.ccod_mun )
        WHERE
        ( c.ctrl_cbr IS NOT NULL )

        AND ( (
        /*CONDICAO QUE FAZ VERIFICACAO SE O DOCUMENTO ESTA EM ABERTO*/
        SELECT
        valor
        FROM
        TABLE ( valor_aberto_receber(r.ctrl_rec))
        ) > 0 )
        AND
        /*DOCUMENTOS CANCELADOS NÃO TRAZ NA CONSULTA*/
        ( r.situ_rec <> 'C'
        )
    """

    return render(request, 'receber.html')