#QUERIES SQL PARA O SERVER ORACLE

def sql_contas_pagar_oracle(date_start, date_end, stores):
    return f"""
        SELECT
            TRA.RAZA_TRA,
            CPG.CODI_EMP,
            EMP.IDEN_EMP,
            PAG.NPAR_PAG,
            CPG.DMOV_CPG,
            PAG.DVEN_PAG,
            PAG.CODI_POR,
            (
                SELECT VALOR
                FROM TABLE(VALOR_ABERTO_PAGAR(PAG.CTRL_PAG))
            ) AS SALD_PAG,
            TDO.TIPO_TDO,
            CASE
                WHEN TDO.TIPO_TDO = 'C' THEN (
                    SELECT VALOR
                    FROM TABLE(VALOR_ABERTO_PAGAR(PAG.CTRL_PAG))) * -1
                ELSE (
                    SELECT VALOR
                    FROM TABLE(VALOR_ABERTO_PAGAR(PAG.CTRL_PAG))
                )
            END AS SALD_CORR
        FROM
            PAGAR PAG
            JOIN CABPAGAR CPG ON (CPG.CTRL_CPG = PAG.CTRL_CPG)
            JOIN TRANSAC TRA ON (TRA.CODI_TRA = CPG.CODI_TRA)
            JOIN TIPDOC TDO ON (TDO.CODI_TDO = CPG.CODI_TDO)
            JOIN CADEMP EMP ON (EMP.CODI_EMP = CPG.CODI_EMP)
        WHERE
            NOT EXISTS (
                SELECT *
                FROM
                    RCPPAGAR RCP
                WHERE
                    (RCP.CTRL_PAG = PAG.CTRL_PAG)
                    AND (RCP.TIPO_RCP = 'R')
                    AND (RCP.VLOR_RCP = PAG.VLOR_PAG)
            )
            AND (CPG.DMOV_CPG BETWEEN TO_DATE('{date_start}', 'YYYY-MM-DD') AND TO_DATE('{date_end}', 'YYYY-MM-DD'))
            AND (PAG.DVEN_PAG BETWEEN TO_DATE('{date_start}', 'YYYY-MM-DD') AND TO_DATE('{date_end}', 'YYYY-MM-DD'))
            AND (TDO.CODI_TDO IN (
                '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '18', '19', '23', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '40', '41', '50', '51', '60', '61', '101', '102', '103', '104', '105', '106', '107', '108', '110', '10000001', '10000003', '10000004', '10000005', '10000006', '10000007', '10000008', '10000009', '10000010', '10000011', '10000012', '30000001', '30000002'))
            AND (CPG.CODI_EMP IN {stores})
            AND (
                (SELECT VALOR
                FROM TABLE(VALOR_ABERTO_PAGAR(PAG.CTRL_PAG))
                ) > 0
            )
    """

def sql_contas_receber_oracle(date_start, date_end):
    return f"""
        SELECT
        t.raza_tra,
        c.codi_emp,
        emp.iden_emp,
        r.npar_rec,
        c.data_cbr,
        (SELECT valor FROM TABLE (valor_aberto_receber(r.ctrl_rec))) AS valor_aberto_receber,
        td.tipo_tdo as tipo_documento,
        CASE
            WHEN td.tipo_tdo = 'C' THEN (SELECT valor FROM TABLE (valor_aberto_receber(r.ctrl_rec))) * -1
            ELSE (SELECT valor FROM TABLE (valor_aberto_receber(r.ctrl_rec)))
        END AS valor_rec_corr
        FROM
        cabrec c
        JOIN receber r ON (c.ctrl_cbr = r.ctrl_cbr)
        JOIN transac t ON (t.codi_tra = c.codi_tra)
        JOIN tipdoc td ON (td.codi_tdo = c.codi_tdo)
        JOIN cademp emp on (emp.codi_emp = c.codi_emp)
        WHERE
        (c.ctrl_cbr IS NOT NULL)
        AND ((SELECT valor FROM TABLE (valor_aberto_receber(r.ctrl_rec))) > 0)
        AND (r.situ_rec <> 'C')
        AND (c.data_cbr BETWEEN TO_DATE('{date_start}', 'YYYY-MM-DD') AND TO_DATE('{date_end}', 'YYYY-MM-DD'))
    """