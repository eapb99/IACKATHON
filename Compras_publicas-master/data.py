import json

import pandas as pd
import os

ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_padre = os.path.dirname(ruta_actual)
with open('../proveedores6.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
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
df.to_csv(os.path.join(ruta_padre, 'metricas_proveedor_colec_3.csv'), index=False)
print(df.shape)
lista_rucs = df['id_ruc'].tolist()

import numpy as np
d = {}
n = len(lista_rucs)
Matriz = np.zeros((n, n), dtype=int)
ruc_to_index = {ruc: i for i, ruc in enumerate(lista_rucs)}
with open('dbProcurementNew4.json', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Iteramos a través de los elementos en data
for values in data:
    bids = set(values['bidders_ruc'])
    common_rucs = bids.intersection(ruc_to_index.keys())

    # Actualizamos el diccionario y la matriz para cada ruc en common_rucs
    for ruc in common_rucs:
        i = ruc_to_index[ruc]

        if ruc not in d:
            d[ruc] = bids
        else:
            d[ruc].update(bids)

        for valor in common_rucs:
            if valor != ruc:
                j = ruc_to_index[valor]
                Matriz[i][j] = 1
print(Matriz.shape)
