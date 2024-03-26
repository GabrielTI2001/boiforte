from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from boiforte.settings import BOIFORTE_DB_HOST, BOIFORTE_DB_PASS, BOIFORTE_DB_PORT, BOIFORTE_DB_USER, BOIFORTE_DB_SID, ORACLE_CLIENT
from datetime import date, datetime, timedelta
import json, locale, sqlalchemy, cx_Oracle
import pandas as pd
from siagri.queries import sql_contas_pagar_oracle, sql_contas_receber_oracle


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
@permission_required('siagri.ver_contas_pagar_receber', raise_exception=True)
def siagri_contas_pagar_receber(request):
    #dsn = cx_Oracle.makedsn(BOIFORTE_DB_HOST, BOIFORTE_DB_PORT, service_name=BOIFORTE_DB_SID)
    #conn = cx_Oracle.connect(user=BOIFORTE_DB_USER, password=BOIFORTE_DB_PASS, dsn=dsn)
    dsn = f"{BOIFORTE_DB_HOST}:{BOIFORTE_DB_PORT}/?service_name={BOIFORTE_DB_SID}"
    conn = f"oracle+cx_oracle://{BOIFORTE_DB_USER}:{BOIFORTE_DB_PASS}@{dsn}"
    engine = sqlalchemy.create_engine(conn)

    current_date = date.today().strftime('%Y-%m-%d')

    search_start = request.GET.get('start', current_date)
    search_end = request.GET.get('end', (date.today() + timedelta(days=120)).strftime('%Y-%m-%d'))
    search_store = f"({', '.join([f'{value}' for value in request.GET.getlist('store')])})" if request.GET.getlist('store') else (1, 2, 3, 4, 5, 6, 7)

    #CONSULTA SQL QUE BUSCA AS LOJAS
    query_sql_lojas = "SELECT CODI_EMP, IDEN_EMP FROM CADEMP"
    df_lojas = pd.read_sql(query_sql_lojas, engine)
    lojas = df_lojas.to_dict('records')

    #MAIN DATAFRAME PAGAR
    df_pagar = pd.read_sql(sql_contas_pagar_oracle(date_start=search_start, date_end=search_end, stores=search_store), engine)
    df_receber = pd.read_sql(sql_contas_receber_oracle(date_start=search_start, date_end=search_end), engine)

    #TOP 10 CONTAS PAGAR (GROUPED)
    resultados_pagar = df_pagar.groupby('raza_tra')['sald_corr'].sum().reset_index().sort_values('sald_corr', ascending=False).head(10)
    dict_resultados_pagar = resultados_pagar.set_index('raza_tra')['sald_corr'].to_dict()

    #TOP 10 CONTAS RECEBER (GROUPED)
    resultados_receber = df_receber.groupby('raza_tra')['valor_rec_corr'].sum().reset_index().sort_values('valor_rec_corr', ascending=False).head(10)
    dict_resultados_receber = resultados_receber.set_index('raza_tra')['valor_rec_corr'].to_dict()

    #TOTAL CONTAS A PAGAR
    total_pagar = df_pagar['sald_corr'].sum()
    total_receber = df_receber['valor_rec_corr'].sum()

    #TOTAL DE CONTAS VENCIDAS
    contas_vencidas_pagar = df_pagar[df_pagar['dven_pag'] < current_date]
    total_vencidos_pagar = contas_vencidas_pagar['sald_corr'].sum()

    contas_vencidas_receber = df_receber[df_receber['data_cbr'] < current_date]
    total_vencidos_receber = contas_vencidas_receber['valor_rec_corr'].sum()

    context = {
        'lojas': lojas,
        'resultados_pagar': dict_resultados_pagar,
        'resultados_receber': dict_resultados_receber,
        'total_pagar': locale.format_string('%.2f', float(total_pagar), True),
        'total_pagar_vencidos': locale.format_string('%.2f', float(total_vencidos_pagar), True),
        'total_receber': locale.format_string('%.2f', float(total_receber), True),
        'total_receber_vencidos': locale.format_string('%.2f', float(total_vencidos_receber), True),
        'search_start': search_start,
        'search_end': search_end,
        'search_store': search_store
    }

    return render(request, 'pagar-receber.html', context)



@login_required
@permission_required('siagri.ver_contas_pagar_receber', raise_exception=True)
def siagri_contas_pagar(request):
    dsn_tns = cx_Oracle.makedsn(BOIFORTE_DB_HOST, BOIFORTE_DB_PORT, BOIFORTE_DB_SID)
    conexao = cx_Oracle.connect(BOIFORTE_DB_USER, BOIFORTE_DB_PASS, dsn_tns)
    cursor = conexao.cursor()
    cursor.execute(sql_contas_pagar_oracle(date_start='2022-01-01', date_end='2025-12-31', stores=(1, 2, 3, 4, 5, 6, 7)))
    colunas = [col[0] for col in cursor.description]
    resultados = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    resultados_ordenados = sorted(resultados, key=lambda x: x['DVEN_PAG'])
    cursor.close()
    conexao.close()

    contas = [{
        'razao_social': resultado['RAZA_TRA'],
        'empresa': resultado['IDEN_EMP'],
        'parcela': resultado['NPAR_PAG'],
        'data_vencimento': resultado['DVEN_PAG'].strftime('%d/%m/%Y'),
        'valor_pagamento': locale.format_string('%.2f', resultado['SALD_CORR'], True),
        'status': {'status': 'Vencida', 'color': 'warning'} if resultado['DVEN_PAG'] < datetime.today() - timedelta(days=1)  else {'status': 'No Prazo', 'color': 'success'}

    } for resultado in resultados_ordenados]

    context = {
        'resultados': contas,
        'total': sum(map(lambda obj: obj['SALD_CORR'], resultados))
    }

    return render(request, 'pagar.html', context)


@login_required
@permission_required('siagri.ver_contas_pagar_receber', raise_exception=True)
def siagri_contas_receber(request):
    dsn_tns = cx_Oracle.makedsn(BOIFORTE_DB_HOST, BOIFORTE_DB_PORT, BOIFORTE_DB_SID)
    conexao = cx_Oracle.connect(BOIFORTE_DB_USER, BOIFORTE_DB_PASS, dsn_tns)
    cursor = conexao.cursor()
    cursor.execute(sql_contas_receber_oracle(date_start='2022-01-01', date_end='2025-12-31'))
    colunas = [col[0] for col in cursor.description]
    resultados = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    resultados_ordenados = sorted(resultados, key=lambda x: x['DATA_CBR'])
    cursor.close()
    conexao.close()

    contas = [{
        'razao_social': resultado['RAZA_TRA'],   
        'empresa': resultado['IDEN_EMP'],
        'parcela': resultado['NPAR_REC'],
        'data_vencimento': resultado['DATA_CBR'].strftime('%d/%m/%Y'),
        'valor_pagamento': locale.format_string('%.2f', resultado['VALOR_REC_CORR'], True),
        'status': {'status': 'Vencida', 'color': 'warning'} if resultado['DATA_CBR'] < datetime.today() - timedelta(days=1)  else {'status': 'No Prazo', 'color': 'success'}
    } for resultado in resultados_ordenados]

    context = {
        'resultados': contas,
        'total': sum(map(lambda obj: obj['VALOR_REC_CORR'], resultados))
    }

    return render(request, 'receber.html', context)




@login_required
def siagri_test(request):
    dsn_tns = cx_Oracle.makedsn(BOIFORTE_DB_HOST, BOIFORTE_DB_PORT, BOIFORTE_DB_SID)
    conexao = cx_Oracle.connect(BOIFORTE_DB_USER, BOIFORTE_DB_PASS, dsn_tns)

    # Criar um cursor
    cursor = conexao.cursor()
    
    # Consulta SQL
    consulta_sql = f"""
        SELECT DISTINCT PRODSERV_1.CODI_PSV, 
            PRODSERV_1.PRSE_PSV,  
            PRODSERV_1.DESC_PSV,  
            PRODSERV_1.UNID_PSV,  
            PRODUTO_1.QTMC_PRO,  
            TIPOPRODU_1.CODI_TIP,  
            TIPOPRODU_1.DESC_TIP,  
            GRUPO_1.CODI_GPR,  
            GRUPO_1.DESC_GPR,  
            SUBGRUPO_1.CODI_SBG,  
            SUBGRUPO_1.DESC_SBG,  
            PRODUTO_1.CODI_TRA,  
            TRANSAC_1.RAZA_TRA,  
            CATEGFOR_1.CODI_CTF,  
            CATEGFOR_1.DESC_CTF,  
            EMBALA_1.CODI_EMB,  
            EMBALA_1.DESC_EMB,  
            DADOSPRO_1.LOCA_DAD,  
            DADOSPRO_1.CODI_EMP,  
            PRODUTO_1.CORI_PRO,  
            PRODSERV_1.CODI_GPR||PRODSERV_1.CODI_SBG PRODSERV_1_CODI_GPR_PRODS,  
            COALESCE(PRODUTO_1.CEST_PRO, 'B') COALESCE_PRODUTO_1_CEST_P,  
            COALESCE(PRODUTO_1.QTE1_PRO, 0) COALESCE_PRODUTO_1_QTE1_P,  
            COALESCE(PRODUTO_1.QTE2_PRO, 0) COALESCE_PRODUTO_1_QTE2_P,  
            COALESCE(PRODUTO_1.QTMC_PRO, 1) COALESCE_PRODUTO_1_QTMC_P, 
            PRODSERV_1.CODI_PRI, 
            PRI.DESC_PRI 
        FROM PRODSERV 			   PRODSERV_1 
        LEFT JOIN PRODUTO 		PRODUTO_1 	ON PRODSERV_1.CODI_PSV = PRODUTO_1.CODI_PSV 
        LEFT JOIN FORNEC 			FORNEC_1 	ON PRODUTO_1.CODI_TRA = FORNEC_1.CODI_TRA 
        LEFT JOIN TIPOPRODU 		TIPOPRODU_1 ON PRODSERV_1.CODI_TIP = TIPOPRODU_1.CODI_TIP 
        LEFT JOIN GRUPO 			GRUPO_1 		ON PRODSERV_1.CODI_GPR = GRUPO_1.CODI_GPR  
        LEFT JOIN SUBGRUPO 		SUBGRUPO_1 	ON PRODSERV_1.CODI_GPR = SUBGRUPO_1.CODI_GPR  
                                            AND PRODSERV_1.CODI_SBG = SUBGRUPO_1.CODI_SBG 
        LEFT JOIN TRANSAC 		TRANSAC_1 	ON PRODUTO_1.CODI_TRA = TRANSAC_1.CODI_TRA 
        LEFT JOIN CATEGFOR 		CATEGFOR_1 	ON FORNEC_1.CODI_CTF = CATEGFOR_1.CODI_CTF 
        LEFT JOIN EMBALA 			EMBALA_1 	ON PRODUTO_1.CODI_EMB = EMBALA_1.CODI_EMB 
        LEFT JOIN DADOSPRO 		DADOSPRO_1 	ON PRODSERV_1.CODI_PSV = DADOSPRO_1.CODI_PSV 
        LEFT JOIN PRINATIVOS 	PRI 			ON PRODSERV_1.CODI_PRI = PRI.CODI_PRI 
        WHERE NOT EXISTS (SELECT CODI_PSV FROM BEM B WHERE B.CODI_PSV = PRODSERV_1.CODI_PSV) 
        and ( PRODSERV_1.SITU_PSV = 'A')   and (PRODSERV_1.CODI_GPR IN ('25','17','33','10000010','27','26','30','18','10000011','1','31','37','8','22','3','10000012','19','10000003','36','10000013','10000014','10000004','15','13','21','16','10000001','11','29','5','10','10000015','23','32','12','14','10000006','10000007','7','9','2','10000016','28','6','24','35'))   and ( PRODSERV_1.PRSE_PSV IN ('P', 'K'))  and ((DADOSPRO_1.CODI_EMP IS NOT NULL AND DADOSPRO_1.CODI_EMP IN ('1','4','6','2')) or (DADOSPRO_1.CODI_EMP IS NULL))   
        
        UNION ALL 
        
        SELECT DISTINCT PRODSERV_1.CODI_PSV, 
            PRODSERV_1.PRSE_PSV, 
            PRODSERV_1.DESC_PSV, 
            PRODSERV_1.UNID_PSV, 
            PRODUTO_1.QTMC_PRO, 
            TIPOPRODU_1.CODI_TIP, 
            TIPOPRODU_1.DESC_TIP, 
            GRUPO_1.CODI_GPR, 
            GRUPO_1.DESC_GPR, 
            SUBGRUPO_1.CODI_SBG, 
            SUBGRUPO_1.DESC_SBG,  
            PRODUTO_1.CODI_TRA, 
            TRANSAC_1.RAZA_TRA, 
            CATEGFOR_1.CODI_CTF, 
            CATEGFOR_1.DESC_CTF, 
            EMBALA_1.CODI_EMB, 
            EMBALA_1.DESC_EMB, 
            DADOSPRO_1.LOCA_DAD, 
            B.CODI_EMP, 
            PRODUTO_1.CORI_PRO, 
            PRODSERV_1.CODI_GPR||PRODSERV_1.CODI_SBG PRODSERV_1_CODI_GPR_PRODS, 
            COALESCE(PRODUTO_1.CEST_PRO, 'B') COALESCE_PRODUTO_1_CEST_P, 
            COALESCE(PRODUTO_1.QTE1_PRO, 0) COALESCE_PRODUTO_1_QTE1_P, 
            COALESCE(PRODUTO_1.QTE2_PRO, 0) COALESCE_PRODUTO_1_QTE2_P, 
            COALESCE(PRODUTO_1.QTMC_PRO, 1) COALESCE_PRODUTO_1_QTMC_P, 
            PRODSERV_1.CODI_PRI, 
            PRI.DESC_PRI 
        FROM PRODSERV  PRODSERV_1 
            JOIN BEM B 	ON PRODSERV_1.CODI_PSV = B.CODI_PSV 
        LEFT JOIN PRODUTO PRODUTO_1 ON PRODSERV_1.CODI_PSV = PRODUTO_1.CODI_PSV 
        LEFT JOIN FORNEC FORNEC_1 ON PRODUTO_1.CODI_TRA = FORNEC_1.CODI_TRA 
        LEFT JOIN TIPOPRODU TIPOPRODU_1 ON PRODSERV_1.CODI_TIP = TIPOPRODU_1.CODI_TIP 
        LEFT JOIN GRUPO GRUPO_1 ON PRODSERV_1.CODI_GPR = GRUPO_1.CODI_GPR 
        LEFT JOIN SUBGRUPO SUBGRUPO_1 ON PRODSERV_1.CODI_GPR = SUBGRUPO_1.CODI_GPR 
            AND PRODSERV_1.CODI_SBG = SUBGRUPO_1.CODI_SBG 
        LEFT JOIN TRANSAC TRANSAC_1 ON PRODUTO_1.CODI_TRA = TRANSAC_1.CODI_TRA 
        LEFT JOIN CATEGFOR CATEGFOR_1 ON FORNEC_1.CODI_CTF = CATEGFOR_1.CODI_CTF 
        LEFT JOIN EMBALA EMBALA_1 ON PRODUTO_1.CODI_EMB = EMBALA_1.CODI_EMB 
        LEFT JOIN DADOSPRO DADOSPRO_1 ON PRODSERV_1.CODI_PSV = DADOSPRO_1.CODI_PSV 
        LEFT JOIN PRINATIVOS PRI ON PRODSERV_1.CODI_PRI = PRI.CODI_PRI 
        WHERE (1 = 1) 
        and ( PRODSERV_1.SITU_PSV = 'A')   
        and (PRODSERV_1.CODI_GPR IN ('25','17','33','10000010','27','26','30','18','10000011','1','31','37','8','22','3','10000012','19','10000003','36','10000013','10000014','10000004','15','13','21','16','10000001','11','29','5','10','10000015','23','32','12','14','10000006','10000007','7','9','2','10000016','28','6','24','35'))   
        and ( PRODSERV_1.PRSE_PSV IN ('P', 'K'))  
        and ((DADOSPRO_1.CODI_EMP IS NOT NULL AND DADOSPRO_1.CODI_EMP IN ('1','4','6','2')) or (DADOSPRO_1.CODI_EMP IS NULL))   
        and ((B.CODI_EMP IS NOT NULL AND B.CODI_EMP in ('1','4','6','2')) or (B.CODI_EMP IS NULL))         
    """

    sql2 = f"""

        SELECT PE.CODI_EMP, 
        PE.PEDI_PED, 
        PE.SERI_PED, 
        PE.CODI_TRA, 
        TR.RAZA_TRA, 
        PE.DEMI_PED, 
        PE.DATA_VLR, 
        PE.VCTO_PED, 
        PE.COD1_PES, 
        (SELECT PES.NOME_PES FROM PESSOAL PES WHERE (PES.CODI_PES = PE.COD1_PES)) AS NOME_PES, 
        PE.CCFO_CFO, 
        PE.COND_CON, 
        CO.DESC_CON, 
        PE.DPON_PED, 
        GP.CODI_GPR, 
        GP.DESC_GPR, 
        IPE.CODI_PSV, 
        PD.DESC_PSV, 
        IPE.CODI_PSV ||' - '|| PD.DESC_PSV AS DESC_PSV2, 
        IPE.CODI_PSV ||' - '|| PD.COMP_PSV AS COMP_PSV2, 
        PD.UNID_PSV, 
        PD.COMP_PSV, 
        IPE.TABE_CTA, 
        IPE.VLIQ_IPE, 
        PE.SASS_PED, 
        PE.CODI_TOP, 
        NEG.NUME_NEG, 
        PE.PEDO_PED, 
        PE.OBSE_PED, 
        PE.COBC_OBS, 
        (SELECT OB.DESC_OBS FROM OBSERVAC OB WHERE (OB.CODI_OBS = PE.CODI_OBS)) AS DESC_OBS, 
        (SELECT OB1.DESC_OBS FROM OBSERVAC OB1 WHERE  (OB1.CODI_OBS = PE.COBC_OBS)) AS OBCO_OBS, 
        PE.OCOM_PED, 
        PE.CODI_OBS, 
        PE.CODI_CIC, 
        PE.CODI_ZON, 
        IPE.DTPR_IPE, 
        (COALESCE(IPE.QTDE_IPE, 0)  /*QPERFILTRO*/) AS QPED_IPE, 
        PE.PROP_PRO, 
        PRO.DESC_PRO, 
        PE.CODI_EMP || '.' || PE.PEDI_PED || '.' || PE.SERI_PED GRUPO_PEDIDO, 
        COALESCE(IPE.QTDE_IPE, 0) - 
        (SELECT QENT 
            FROM  table( QTDE_ENTR_PED_VEN(IPE.CODI_EMP, 
                IPE.PEDI_PED, 
                IPE.SERI_PED, 
                IPE.CODI_PSV 
                ) ) 
            ) - COALESCE(IPE.QPER_IPE,0) AS QFAT_IPE, 
        (SELECT QENT 
            FROM  table( QTDE_ENTR_PED_VEN(IPE.CODI_EMP, 
                IPE.PEDI_PED, 
                IPE.SERI_PED, 
                IPE.CODI_PSV 
                ) ) 
            ) QENT_IPE, 
        (SELECT QDEV 
            FROM  table( QTDE_ENTR_PED_VEN(IPE.CODI_EMP, 
                IPE.PEDI_PED, 
                IPE.SERI_PED, 
                IPE.CODI_PSV 
                ) ) 
            ) QDEV_IPE, 
        I.ABRE_IND, 
        PE.CODI_IND, 
        COALESCE(TRVD.CODI_TRA, 0) AS VDCODI_TRA, 
        TRVD.RAZA_TRA AS VDRAZA_TRA, 
        EM.CODI_EMB, 
        EM.DESC_EMB, 
        (SELECT PSU.NOME_PES FROM PESSOAL PSU WHERE (PSU.CODI_PES = CDU.CODI_PES)) AS NOME_USU, 
        (SELECT MNP.DESC_MUN FROM MUNICIPIO MNP WHERE (MNP.CODI_MUN = PRO.CODI_MUN)) AS MUNIPRO, 
        PRO.ISNE_PRO, 
        PRO.LOC1_PRO AS LOCALPRO, 
        PRO.FONE_PRO AS FONEPRO, 
        TR.CGC_TRA, 
            PR.CEST_PRO, 
            PR.QTE1_PRO, 
            PR.QTE2_PRO, 
        MUN.DESC_MUN AS MUNCLI,MUN.ESTA_MUN AS UFCLI, 
        TBL.BASI_TAB, TBL.DESC_TAB, TBL.ACRE_TAB,IPE.VLOR_IPE,  
        CASE WHEN (SELECT COUNT(*)  
                    FROM OCORRENCIAS O  
                    WHERE O.CODI_EMP = PE.CODI_EMP  
                        AND O.PEDI_PED = PE.PEDI_PED  
                        AND O.SERI_PED = PE.SERI_PED  
                        AND O.CODI_PSV = IPE.CODI_PSV) > 0  
                THEN  
                COALESCE((  
                            SELECT O.QTDE_OCO 
                            FROM(select * from  OCORRENCIAS O                                                  
                            ORDER BY O.DATA_OCO DESC 
                            ) O                                                  
                            WHERE O.CODI_EMP = PE.CODI_EMP                                                
                            AND O.PEDI_PED = PE.PEDI_PED                                               
                            AND O.SERI_PED = PE.SERI_PED                                              
                            AND O.CODI_PSV = IPE.CODI_PSV                                             
                                            
                            and rownum <= 1 
                            ), 0)  
                ELSE  
                COALESCE(IPE.QPER_IPE,0)  
            END AS  QPER_IPE,        
        CASE WHEN (PE.PROP_PRO > 0) AND (PE.PROP_PRO IS NOT NULL) THEN REG2.DESC_REG ELSE  REG.DESC_REG END AS DESC_REG, 
        CASE WHEN (PE.PROP_PRO > 0) AND (PE.PROP_PRO IS NOT NULL) THEN ROT2.CODI_ROT ELSE  ROT.CODI_ROT END AS CODI_ROT,  
        CASE WHEN (PE.PROP_PRO > 0) AND (PE.PROP_PRO IS NOT NULL) THEN REG2.CODI_REG ELSE  REG.CODI_REG END AS CODI_REG,  
        CASE WHEN (PE.PROP_PRO > 0) AND (PE.PROP_PRO IS NOT NULL) THEN ROT2.DESC_ROT ELSE  ROT.DESC_ROT END AS DESC_ROT, 
        COALESCE (PR.PBRU_PRO * IPE.QTDE_IPE,0)  AS PBRU_PRO ,  COALESCE(PR.PLIQ_PRO * IPE.QTDE_IPE,0) AS PLIQ_PRO, 
        IPE.DSOF_IPE, IPE.VDOF_IPE, PE.VCTO_PED, PE.ORIG_PED, 
        CASE WHEN PE.ORIG_PED = '1' THEN 
            (SELECT   CAD2.CODI_USU  FROM NEGOCESP NCE  
                    INNER JOIN CADUSU CAD2 ON (NCE.CODI_USU = CAD2.CODI_USU) 
                WHERE (NCE.CTRL_NEG = NEG.CTRL_NEG  
                    AND NCE.CODI_EMP = NEG.CODI_EMP 
                    AND NCE.CODI_PES = NEG.CODI_PES)  )  
        ELSE '' END AS NOME_LANCOU_NEGOCIACAO, 
        CASE WHEN PE.ORIG_PED = '1' THEN  
            (SELECT  CAD1.CODI_USU  FROM CADUSU CAD1 
                WHERE (CAD1.CODI_USU = NEG.CODI_USU)) 
        ELSE '' END  AS NOME_ULTIMO_ALTERAR_NEGOCIACAO, 
        CASE WHEN PE.ORIG_PED = '1' THEN 
            (SELECT  CAD3.CODI_USU FROM CADUSU CAD3 
                WHERE (NEG.USLF_NEG =CAD3.CODI_USU)) 
        ELSE '' END  AS NOME_ULTIMO_LIBERAR_NEGOCIACAO, 
        PE.CFOR_TRA, 
        PE.TFAT_PED     
    , ((IPE.VLIQ_IPE - (case when (PGF.DFML_PGF = 'S' and coalesce(PE.FRET_PED, 0) > 0) then (((IPE.VLOR_IPE + IPE.DSAC_IPE + (IPE.VIPI_IPE / COALESCE(IPE.QTDE_IPE, 1)) + (IPE.VICS_IPE / COALESCE(IPE.QTDE_IPE, 1)) ) / COALESCE((PE.TPRO_PED + PE.VIPI_PED), 1)) * PE.FRET_PED) else 0 end))  * (IPE.QTDE_IPE - IPE.QPER_IPE)  * case when ((coalesce(PGF.DSOF_PGF, '0') in ('1', '2')) and (PE.VCTO_PED <= IPE.VDOF_IPE)) then                           1 - (IPE.DSOF_IPE / 100)                  else                          1                 end) - (IPE.CTAB_IPE  * (IPE.QTDE_IPE - IPE.QPER_IPE)) as VR_LUCRO, case when ((((IPE.VLIQ_IPE - (case when (PGF.DFML_PGF = 'S' and coalesce(PE.FRET_PED, 0) > 0) then (((IPE.VLOR_IPE + IPE.DSAC_IPE + (IPE.VIPI_IPE / COALESCE(IPE.QTDE_IPE, 1)) + (IPE.VICS_IPE / COALESCE(IPE.QTDE_IPE, 1)) ) / COALESCE((PE.TPRO_PED + PE.VIPI_PED), 1)) * PE.FRET_PED) else 0 end)) - case when coalesce(PGF.DIPM_PGF,'N') = 'S' then (IPE.ICMS_IPE /IPE.QTDE_IPE) else 0 end) * (IPE.QTDE_IPE - IPE.QPER_IPE) * case when ((coalesce(PGF.DSOF_PGF, '0') in ('1', '2')) and (PE.VCTO_PED <= IPE.VDOF_IPE)) then 1 - (IPE.DSOF_IPE / 100)       else 1 end) <> 0) then           ((((IPE.VLIQ_IPE - (case when (PGF.DFML_PGF = 'S' and coalesce(PE.FRET_PED, 0) > 0) then (((IPE.VLOR_IPE + IPE.DSAC_IPE + (IPE.VIPI_IPE / COALESCE(IPE.QTDE_IPE, 1)) + (IPE.VICS_IPE / COALESCE(IPE.QTDE_IPE, 1)) ) / COALESCE((PE.TPRO_PED + PE.VIPI_PED), 1)) * PE.FRET_PED) else 0 end)) - case when coalesce(PGF.DIPM_PGF,'N') = 'S' then (IPE.ICMS_IPE /IPE.QTDE_IPE) else 0 end) * (IPE.QTDE_IPE - IPE.QPER_IPE)          * case when ((coalesce(PGF.DSOF_PGF, '0') in ('1', '2')) and (PE.VCTO_PED <= IPE.VDOF_IPE)) then 1 - (IPE.DSOF_IPE / 100)           else 1           end) - ((IPE.CTAB_IPE)  * (IPE.QTDE_IPE - IPE.QPER_IPE))) * 100      / (((IPE.VLIQ_IPE - (case when (PGF.DFML_PGF = 'S' and coalesce(PE.FRET_PED, 0) > 0) then (((IPE.VLOR_IPE + IPE.DSAC_IPE + (IPE.VIPI_IPE / COALESCE(IPE.QTDE_IPE, 1)) + (IPE.VICS_IPE / COALESCE(IPE.QTDE_IPE, 1)) ) / COALESCE((PE.TPRO_PED + PE.VIPI_PED), 1)) * PE.FRET_PED) else 0 end)) - case when coalesce(PGF.DIPM_PGF,'N') = 'S' then (IPE.ICMS_IPE /IPE.QTDE_IPE) else 0 end) * (IPE.QTDE_IPE - IPE.QPER_IPE)        * case when ((coalesce(PGF.DSOF_PGF, '0') in ('1', '2')) and (PE.VCTO_PED <= IPE.VDOF_IPE)) then 1 - (IPE.DSOF_IPE / 100)      else 1         end)       else 0 end as MGR_LUCRO 
        FROM PEDIDO PE 
        /*bjoin*/ 
        INNER JOIN TRANSAC TR ON (TR.CODI_TRA = PE.CODI_TRA) 
        INNER JOIN CLIENTE CL ON (CL.CODI_TRA = PE.CODI_TRA) 
        INNER JOIN IPEDIDO IPE ON (IPE.CODI_EMP = PE.CODI_EMP) 
            AND (IPE.PEDI_PED = PE.PEDI_PED) 
            AND (IPE.SERI_PED = PE.SERI_PED) 
        INNER JOIN PRODSERV PD ON (PD.CODI_PSV = IPE.CODI_PSV) 
        INNER JOIN GRUPO GP ON (PD.CODI_GPR = GP.CODI_GPR) 
        INNER JOIN PRODUTO PR ON (PR.CODI_PSV = IPE.CODI_PSV)  
        LEFT JOIN EMBALA EM ON (EM.CODI_EMB = PR.CODI_EMB) 
        LEFT JOIN TABELA TBL ON (IPE.TABE_CTA = TBL.TABE_CTA AND IPE.CODI_PSV = TBL.CODI_PSV) 
        LEFT JOIN MUNICIPIO MUN ON (MUN.CODI_MUN = TR.CODI_MUN) 
        LEFT JOIN TRANSAC TRVD ON (TRVD.CODI_TRA = PE.CFOR_TRA) 
        LEFT JOIN CONDICAO CO ON (CO.COND_CON = PE.COND_CON)   
        LEFT JOIN FORNEC FO ON (FO.CODI_TRA = PE.CFOR_TRA)   
        LEFT JOIN FORNEC FA ON (PR.CODI_TRA = FA.CODI_TRA)     
        LEFT JOIN PROPRIED PRO ON (PRO.PROP_PRO = PE.PROP_PRO AND PRO.CODI_TRA = PE.CODI_TRA) 
        LEFT OUTER JOIN INDEXADOR I ON (I.CODI_IND = PE.CODI_IND)   
        LEFT OUTER JOIN CADUSU CDU ON (CDU.CODI_USU = PE.CODI_USU) 
        LEFT JOIN ENDERENTR ET ON (ET.CODI_END = PE.CODI_END) 
        LEFT JOIN REGIAO REG ON (CL.CODI_REG = REG.CODI_REG) 
        LEFT JOIN ROTA ROT ON (CL.CODI_ROT = ROT.CODI_ROT) 
        LEFT JOIN REGIAO REG2 ON (PRO.CODI_REG = REG2.CODI_REG) 
        LEFT JOIN ROTA ROT2 ON (PRO.CODI_ROT = ROT2.CODI_ROT)   
        LEFT JOIN NEGOCIACAO NEG ON (NEG.CTRL_NEG = PE.CTRL_NEG AND  
            NEG.CODI_PES = PE.COD1_PES AND  
            NEG.CODI_EMP = PE.CODI_EMP) 
        LEFT JOIN PARAMGERFATU PGF ON (PE.CODI_EMP = PGF.CODI_EMP) 
        /*ejoin*/ 
        where (PE.DEMI_PED between TO_DATE('2022-10-28', 'YYYY-MM-DD') AND TO_DATE('2023-12-31', 'YYYY-MM-DD')) and (PE.VCTO_PED between TO_DATE('2022-10-28', 'YYYY-MM-DD') AND TO_DATE('2023-12-31', 'YYYY-MM-DD')) 
        and (PE.CODI_EMP in ('1')) and (IPE.LRET_IPE in ('1','2','3','4','5','6') or IPE.LRET_IPE is null)   and (PE.SITU_PED <> '9')  and (PE.TFAT_PED = '1') 
        and ((COALESCE(IPE.QTDE_IPE, 0) - (select QENT  from  table( QTDE_ENTR_PED_VEN(IPE.CODI_EMP, IPE.PEDI_PED, IPE.SERI_PED, IPE.CODI_PSV))) - (case when (select count(*) from OCORRENCIAS O where O.CODI_EMP = PE.CODI_EMP and O.PEDI_PED = PE.PEDI_PED and O.SERI_PED = PE.SERI_PED and O.CODI_PSV = IPE.CODI_PSV) > 0 then                     coalesce((  select O.QTDE_OCO                                            from(select * from  OCORRENCIAS O                                                 order by O.DATA_OCO desc  ) O                                                where O.CODI_EMP = PE.CODI_EMP                                               and O.PEDI_PED = PE.PEDI_PED                                               and O.SERI_PED = PE.SERI_PED                                               and O.CODI_PSV = IPE.CODI_PSV                                                                                                         and rownum <= 1 ), 0)         else             coalesce(IPE.QPER_IPE,0)         end)) > 0.01) order by TR.RAZA_TRA, PE.CODI_TRA, PE.CODI_EMP,  PE.DEMI_PED, PE.PEDI_PED, PE.SERI_PED

    """
    sql3 = f"""

        select  pr.CODI_PSV, prd.CORI_PRO, pr.DESC_PSV, dpr.CODI_EMP, emp.IDEN_EMP, (select coalesce(ESTOQUE,0) from table(SALDO_INICIAL_UF (dpr.CODI_EMP,1,pr.CODI_PSV,TO_DATE('2024-03-22', 'YYYY-MM-DD'), 0, null) )) EST_FIS, 
        (select coalesce(sum(SALD_CTR),0)  from  table( SALDO_INICIAL_TIPOEST_UF (dpr.CODI_EMP, '1', pr.CODI_PSV, null, 'S', null, 0, null) )) EST_DIS, coalesce(dpr.EMIN_DAD,0) as EMIN_DAD, coalesce(dpr.EMAX_DAD,0) as 
        EMAX_DAD,  coalesce(dpr.QTMC_DAD,0) as QTMC_DAD, em.CODI_EMB, em.DESC_EMB, PRA.DESC_PRA PRINCIPIO_ATIVO from PRODSERV pr inner join PRODUTO prd on ( prd.CODI_PSV = pr.CODI_PSV )                    
        left join DADOSPRO dpr on (dpr.CODI_PSV =   pr.CODI_PSV and dpr.CODI_EMP in ('1','2', '3', '4', '5', '6' ) )  left join EMBALA em on (em.CODI_EMB = prd.CODI_EMB) left join FORNEC fab on (prd.CODI_TRA = fab.CODI_TRA)                                               
        inner join CADEMP emp on (emp.CODI_EMP = dpr.CODI_EMP) left join PRODUTO PRO on (PRO.CODI_PSV = PR.CODI_PSV) left join PRODUTOS_REC PRR on (PRR.CODI_PRR = PRD.CODI_PRR)                           
        left join PRODPRIATIVO_REC PAR on (PAR.CODI_PRR =  PRR.CODI_PRR) left join PRINCIPIOATIVO_REC PRA on (PRA.CODI_PRA = PAR.CODI_PRA) 
        where (pr.PRSE_PSV = 'P'or pr.PRSE_PSV = 'C' ) and (pr.CODI_TIP in ('10000008') )  order by dpr.CODI_EMP ,  pr.DESC_PSV

    """

    # Executar a consulta
    cursor.execute(sql3)
    
    # Recuperar os resultados como uma lista de dicionários
    #colunas = ["nome", "cgc"]
    colunas = [col[0] for col in cursor.description]
    resultados = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    
    # Fechar o cursor e a conexão
    cursor.close()
    conexao.close()
    return render(request, 'test.html', {'resultados': resultados}) 

