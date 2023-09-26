import json
import statistics
from statistics import mean
import numpy as np
import pandas as pd
import os
from matriz import save_files
ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_padre = os.path.dirname(ruta_actual)


def contratos_proveedor(data, ruc):
    colectivos = 0
    unicos = 0
    perdidos = 0
    ofertados = 0
    contratos_participados = 0
    monto_ganado = 0
    for obj in data:
        suppliers = obj.get('suppliers')
        if len(suppliers) == 0:
            continue
        bidders_ruc = obj.get('bidders_ruc')
        entity_id = obj.get('entity_id')
        parties = obj.get('parties', [])
        if entity_id in parties:
            parties.remove(entity_id)
        if ruc in parties:
            contratos_participados += 1
        if suppliers and suppliers[0] == ruc:
            unico = bidders_ruc.count(ruc) == len(bidders_ruc)
            if unico:
                unicos += 1
            else:
                colectivos += 1
            monto_ganado += obj.get('amount_award')
        #        tenders = list(set(parties) & set(bidders_ruc))
        if bidders_ruc and ruc in bidders_ruc:
            ofertados += 1
            if ruc != suppliers[0]:
                perdidos += 1
    return colectivos, unicos, perdidos, ofertados, contratos_participados, monto_ganado


def promedio_cantidad_ofertas(data):
    valores = data['amount']
    suma = 0.0
    num_ofertas = len(valores)
    for val in valores:
        suma += val / data['planning']
    return suma, num_ofertas


def update_dict_with_bid_info(temp_dict, bidders_ruc, bids_amounts, bids_dates, planning, award, num_tenders, ocid):
    for bidder, bid, date in zip(bidders_ruc, bids_amounts, bids_dates):
        if bidder not in temp_dict:
            temp_dict[bidder] = {'amount': [], 'date': [], 'norm_amount': []}
        temp_dict[bidder]['ocid'] = ocid
        temp_dict[bidder]['planning'] = planning
        temp_dict[bidder]['award'] = award
        temp_dict[bidder]['participantes'] = num_tenders + 1
        temp_dict[bidder]['ofertantes'] = len(set(bidders_ruc))
        temp_dict[bidder]['amount'].append(bid)
        temp_dict[bidder]['norm_amount'].append(bid / planning)
        temp_dict[bidder]['date'].append(date)

    return temp_dict


def update_provider_info(d, bidder, data):
    gc, gu, cp, co, ct, mg = contratos_proveedor(data, bidder)
    if ct != 0:
        total = gc + cp
        if total > 0:
            if gc > 2:
                d[bidder]['filtro'] = 1
            else:
                d[bidder]['filtro'] = 0
            d[bidder]['% colectivos'] = gc / total
            d[bidder]['% perdidos'] = cp / total
            d[bidder]['ofertados'] = total
    return d


def process_data(data):
    d = {}
    for obj in data:
        if len(obj['suppliers']) > 0:
            ganador = obj['suppliers'][0]
            ocid = obj['ocid']
            temp_dict = update_dict_with_bid_info({}, obj['bidders_ruc'], obj['bids_amounts'], obj['date_list'],
                                                  obj['amount_planning'], obj['amount_award'], obj['numberTenderers'],
                                                  ocid)
            for bidder, bids in temp_dict.items():
                if bidder not in d:
                    d[bidder] = {'BIDS': {'colectivos': [], 'unicos': [], 'perdidos': []},
                                 '% colectivos': 0.0, "% perdidos": 0.0}
                if bidder == ganador:
                    unico = obj['bidders_ruc'].count(bidder) == len(obj['bidders_ruc'])
                    if unico:
                        d[bidder]['BIDS']['unicos'].append(bids)
                    else:
                        d[bidder]['BIDS']['colectivos'].append(bids)
                else:
                    d[bidder]['BIDS']['perdidos'].append(bids)
                d = update_provider_info(d, bidder, data)
    return d


def add_standard_deviation(data):
    for key, value in data.items():
        totales = value['BIDS']['colectivos'] + value['BIDS']['perdidos']
        for bid in totales:
            amounts = bid['amount']
            bid['des'] = statistics.stdev(amounts) if len(amounts) > 1 else 0
            bid['des_norm'] = (statistics.stdev(amounts) if len(amounts) > 1 else 0) / bid['planning']
            bid['diff_award'] = abs((bid['award'] - amounts[-1]) / bid['award'])
            bid['diff_planning'] = abs((bid['planning'] - amounts[-1]) / bid['planning'])


def unique_winner(data):
    for key, value in data.items():
        unicos = value['BIDS']['colectivos'] + value['BIDS']['perdidos']
        if len(unicos) > 0:
            for bid in unicos:
                planning = bid['planning']
                ofertantes = bid['ofertantes']
                num_tenders = bid['participantes']
                indicador = abs(np.log10(ofertantes / num_tenders))
                if num_tenders == 1 or indicador > 1:
                    bid['indicador'] = 1.0
                else:
                    bid['indicador'] = indicador
        else:
            continue


def add_general_standard_deviation(data):
    for key, value in data.items():
        colectivos = value['BIDS']['colectivos']
        perdidos = value['BIDS']['perdidos']
        all_des_colectivos = [bid['des_norm'] for bid in colectivos]
        all_des_perdidos = [bid['des_norm'] for bid in perdidos]
        diff_award_perdidos = [bid['diff_award'] for bid in perdidos]
        diff_planning_colectivos = [bid['diff_planning'] for bid in colectivos]
        diff_planning_perdidos = [bid['diff_planning'] for bid in perdidos]

        if len(all_des_colectivos) > 0:
            value['desviacion_mean_colectivos'] = sum(all_des_colectivos) / len(colectivos)
            value['diff_planning_mean_colectivos'] = sum(diff_planning_colectivos) / len(colectivos)
        else:
            value['desviacion_mean_colectivos'] = 0.0
            value['diff_planning_mean_colectivos'] = 0.0

        if len(all_des_perdidos) > 0:
            value['desviacion_mean_perdidos'] = sum(all_des_perdidos) / len(all_des_perdidos)
            value['diff_award_mean_perdidos'] = sum(diff_award_perdidos) / len(diff_award_perdidos)
            value['diff_planning_mean_perdidos'] = sum(diff_planning_perdidos) / len(diff_planning_perdidos)
        else:
            value['desviacion_mean_perdidos'] = 0.0
            value['diff_award_mean_perdidos'] = 0.0
            value['diff_planning_mean_perdidos'] = 0.0


def create_dict_desv(data):
    d = {}
    for ruc, info in data.items():
        contratos = info['BIDS']['colectivos'] + info['BIDS']['perdidos']
        if contratos:
            for bid in contratos:
                ocid = bid['ocid']
                if ocid not in d:
                    d[ocid] = {'desv': [], 'ruc': [], 'suma_desv': 0}
                d[ocid]['desv'].append(bid['des'])
                d[ocid]['ruc'].append(ruc)
                d[ocid]['suma_desv'] += (bid['des'])
    return d


def calculate_division(dic_desv):
    d = {}
    for ocid, info in dic_desv.items():
        desvL = info['desv']
        rucL = info['ruc']
        suma = info['suma_desv']
        for ruc, des in zip(rucL, desvL):
            if ruc not in d:
                d[ruc] = {'ocid_list': [], 'metrica_list': []}
            d[ruc]['ocid_list'].append(ocid)
            if suma > 0:
                d[ruc]['metrica_list'].append(des / suma)
            else:
                d[ruc]['metrica_list'].append(0.0)

    return d


def add_divi_des(data, divi):
    for ruc, info in data.items():
        colectivos = info['BIDS']['colectivos']
        perdidos = info['BIDS']['perdidos']
        contratos = colectivos + perdidos
        if ruc in divi:
            item_divi = divi[ruc]
            ocidL = item_divi['ocid_list']
            valores = item_divi['metrica_list']
            for contrato in contratos:
                ocid_fuera = contrato['ocid']
                for ocid, valor in zip(ocidL, valores):
                    if ocid == ocid_fuera:
                        contrato['frecuencia_des'] = valor


def add_metrics(data):
    for ruc, info in data.items():
        colectivos = info['BIDS']['colectivos']
        perdidos = info['BIDS']['perdidos']
        ganados = colectivos
        totales = perdidos + ganados

        indicadores = [item['indicador'] for item in totales]
        award_colectivos = [item['award'] for item in colectivos]
        amounts_colectivos = [item for sublist in colectivos for item in sublist['norm_amount']]
        amounts_perdidos = [item for sublist in perdidos for item in sublist['norm_amount']]
        metrica_colectivos = [item['frecuencia_des'] for item in colectivos]
        metrica_perdidos = [item['frecuencia_des'] for item in perdidos]

        min_indicador = min(indicadores) if indicadores else 0
        max_indicador = max(indicadores) if indicadores else 0
        range_indicador = max_indicador - min_indicador
        data[ruc]['mean_indice_ausencia'] = mean(indicadores) if indicadores else 0
        data[ruc]['range_indice_ausencia'] = range_indicador

        data[ruc]['mean_ofertas_colectivos'] = mean(amounts_colectivos) if amounts_colectivos else 0
        data[ruc]['mean_frecuencia_colectivos'] = mean(metrica_colectivos) if metrica_colectivos else 0
        data[ruc]['mean_award_colectivos'] = mean(award_colectivos) if award_colectivos else 0

        data[ruc]['mean_frecuencia_perdidos'] = mean(metrica_perdidos) if metrica_perdidos else 0
        data[ruc]['mean_ofertas_perdidos'] = mean(amounts_perdidos) if amounts_perdidos else 0


def create_file(data, name):
    with open(os.path.join(ruta_padre, f"{name}.json"), 'w') as file:
        json.dump(data, file, indent=3)


def create_metrics(data):
    data1 = {}
    for key, values in data.items():
        if values.get('filtro') == 1:
            data1[key] = values

    rows = []
    for key, value in data1.items():
        value.pop('BIDS', None)
        value['id_ruc'] = key
        rows.append(value)
    df = pd.DataFrame(rows)
    df = df[['id_ruc'] + [col for col in df.columns if col != 'id_ruc']]
    df.to_csv(os.path.join(ruta_padre, 'metricas_proveedor.csv'), index=False)


with open('dbProcurementNew4.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
result = process_data(data)
add_standard_deviation(result)
unique_winner(result)
add_general_standard_deviation(result)
suma_des = create_dict_desv(result)
divi = calculate_division(suma_des)
add_divi_des(result, divi)
add_metrics(result)
save_files(result)
#create_file(result, 'proveedores6')
