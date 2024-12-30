import pandas as pd

def carregar_aliquotas():
    aliquotas_estado = pd.read_csv('data/aliquotas_estado.csv')
    aliquotas_ncm = pd.read_csv('data/aliquotas_ncm.csv')
    
    aliquotas_ncm['ncm'] = aliquotas_ncm['ncm'].astype(str).str.strip()  
    return aliquotas_estado, aliquotas_ncm

def calcular_impostos(valor_base, estado, tipo_produto, ncm):
    aliquotas_estado, aliquotas_ncm = carregar_aliquotas()

    ncm_procurado = str(ncm).strip()
    ncm_row = aliquotas_ncm[aliquotas_ncm['ncm'] == ncm_procurado]
    
    if ncm_row.empty:
        raise ValueError(f"NCM '{ncm_procurado}' não encontrado na tabela.")

    imposto_seletivo = 'Sim' if ncm_row.iloc[0]['imposto_seletivo'] == 'Sim' else 'Não'

    aliquotas_estado_row = aliquotas_estado[(aliquotas_estado['estado'] == estado) &
                                            (aliquotas_estado['tipo_produto'] == tipo_produto)]
    
    if aliquotas_estado_row.empty:
        raise ValueError(f"Alíquotas para o estado '{estado}' e tipo de produto '{tipo_produto}' não encontradas.")

    icms_aliquota = aliquotas_estado_row.iloc[0].get('icms', 0)
    iss_aliquota = aliquotas_estado_row.iloc[0].get('iss', 0)
    pis_aliquota = aliquotas_estado_row.iloc[0].get('pis', 0)
    cofins_aliquota = aliquotas_estado_row.iloc[0].get('cofins', 0)

    icms_valor = icms_aliquota * valor_base
    iss_valor = iss_aliquota * valor_base
    pis_valor = pis_aliquota * valor_base
    cofins_valor = cofins_aliquota * valor_base

    impostos_antigos = icms_valor + pis_valor + cofins_valor + iss_valor

    cbs_aliquota = 0.0  
    ibs_aliquota = 0.0  

    if imposto_seletivo == 'Sim':
        cbs_valor = cbs_aliquota * valor_base
        ibs_valor = ibs_aliquota * valor_base
    else:
        cbs_valor = 0
        ibs_valor = 0

    total_impostos_atual = cbs_valor + ibs_valor

    return {
        "antes_da_reforma": {
            "icms": round(icms_valor, 2),
            "iss": round(iss_valor, 2),
            "pis": round(pis_valor, 2),
            "cofins": round(cofins_valor, 2),
            "total_impostos": round(impostos_antigos, 2),
            "valor_total": round(valor_base + impostos_antigos, 2)
        },
        "depois_da_reforma": {
            "cbs": round(cbs_valor, 2),
            "ibs": round(ibs_valor, 2),
            "total_impostos": round(total_impostos_atual, 2),
            "valor_total": round(valor_base + total_impostos_atual, 2)
        }
    }
