import json
import pickle
import numpy as np
import pandas as pd
import os

ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_padre = os.path.dirname(ruta_actual)


def create_dataframe(result):
    data1 = {}
    for key, values in result.items():
        if values.get('filtro') == 1:
            data1[key] = values
    rows = []
    for key, value in data1.items():
        value.pop('BIDS', None)
        value['id_ruc'] = key
        rows.append(value)

    df = pd.DataFrame(rows)
    df = df[['id_ruc'] + [col for col in df.columns if col != 'id_ruc']]
    return df


def cargar_datos(dict_proveedores):

    df = pd.DataFrame.from_dict(dict_proveedores, orient='index')
    df = df[df['filtro'] == 1]
    df = df.reset_index().rename(columns={'index': 'id_ruc'})

    with open('dbProcurementNew4.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
    df = create_dataframe(dict_proveedores)
    return df, data


def construir_diccionario_bids(df, data):
    lista_rucs = df['id_ruc'].tolist()
    d = {}
    for ruc in lista_rucs:
        for values in data:
            bids = set(values['bidders_ruc'])
            if ruc in bids:
                d.setdefault(ruc, set()).update(bids)
    return d, lista_rucs


def construir_matriz_adjacencia(d, lista_rucs):
    Matriz = np.zeros((len(lista_rucs), len(lista_rucs)), dtype=int)
    for k, v in d.items():
        i = lista_rucs.index(k)
        for valor in v:
            if valor in lista_rucs:
                j = lista_rucs.index(valor)
                if i != j:
                    Matriz[i][j] = 1
    return Matriz


def filtrar_matriz_y_dataframe(Matriz, df):
    suma = Matriz.sum(axis=1)
    indices_filtrados = np.where(suma > 0)[0]
    MatrizFinal = Matriz[indices_filtrados][:, indices_filtrados]
    df_filtrado = df.iloc[indices_filtrados]
    return MatrizFinal, df_filtrado


def guardar_datos(MatrizFinal, df_filtrado):
    with open(os.path.join(ruta_padre, "matriz.dat"), 'wb') as file:
        pickle.dump(MatrizFinal, file)
    df_filtrado.to_csv(os.path.join(ruta_padre, 'dataframe_filtrado.csv'), index=False)


def save_files(diccionario):
    df, data = cargar_datos(diccionario)
    d, lista_rucs = construir_diccionario_bids(df, data)
    Matriz = construir_matriz_adjacencia(d, lista_rucs)
    MatrizFinal, df_filtrado = filtrar_matriz_y_dataframe(Matriz, df)
    guardar_datos(MatrizFinal, df_filtrado)
    print("Datos guardados correctamente.")
