import os
import pickle
import pandas as pd
import torch
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from torch_geometric.data import Data
from torch_geometric.utils import degree
from pygod.detector import GAAN

# Constantes
NUM_CLUSTERS = 3
EMBEDDING_DIM = 64


def load_adjacency_matrix(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)


def load_data(filename, columns_to_normalize):
    df = pd.read_csv(filename)
    #  ofertas = df['ofertados']
    scaler = MinMaxScaler()
    df[columns_to_normalize] = scaler.fit_transform(df[columns_to_normalize])
    ruc = df['id_ruc']
    df.drop(columns=['id_ruc'], inplace=True, axis=1)
    return df, ruc


def create_torch_data(matriz, df):
    mask = np.where(matriz == 1)
    combined_array = np.column_stack(mask)
    edge_index = torch.tensor(combined_array, dtype=torch.long).t()  # Transpone para conservar la estructura correcta
    x = torch.tensor(df.values, dtype=torch.float)
    data = Data(x=x, edge_index=edge_index)
    degrees = degree(data.edge_index[0], num_nodes=data.num_nodes)
    return data, degrees



def format_model_name(detector):
    # param_names = ["hid_dim", "num_layers", "epoch", "dropout", "save_emb", "weight"]
    param_names = ["hid_dim", "dropout", "num_layers", "epoch", "save_emb", "weight"]
    params = "-".join([f"{param}={getattr(detector, param)}" for param in param_names])
    model_name = type(detector).__name__
    return f"{model_name}_{params}", model_name


import itertools

hid_dims = [64]
dropouts = [0.0]
num_layers_list = [4]
epochs_list = [100]
weights = [0.3]

combinations = list(itertools.product(hid_dims, dropouts, num_layers_list, epochs_list, weights))
print(len(combinations))

ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_padre = os.path.dirname(ruta_actual)


def run_combination(combination):
    hid_dim, dropout, num_layers, epoch, weight = combination
    print(
        f"Running for hid_dim: {hid_dim}, dropout: {dropout}, num_layers: {num_layers}, epoch: {epoch}")
    # cantidad = 3
    matriz_adj_filename = os.path.join(ruta_padre, "matriz.dat")
    data_filename = os.path.join(ruta_padre, 'dataframe_filtrado.csv')
    columns_to_normalize = ['mean_award_colectivos']
    matriz = load_adjacency_matrix(matriz_adj_filename)
    print(matriz.shape)
    df, ruc = load_data(data_filename, columns_to_normalize)
    df.drop(columns=['filtro'], inplace=True, axis=1)
    data, degrees = create_torch_data(matriz, df)
    print(data)
    detector = GAAN(hid_dim=hid_dim, num_layers=num_layers, epoch=epoch,gpu=0, save_emb=True, dropout=dropout,
                    weight=weight)
    detector.fit(data)
    pred, score, prob, conf = detector.predict(data,
                                               return_pred=True,
                                               return_score=True,
                                               return_prob=True,
                                               return_conf=True)
    df['id_ruc'] = ruc
    df['probabilidad'] = pd.Series(prob)
    df['confidence'] = pd.Series(conf)
    df['score'] = pd.Series(score)
    df['pred'] = pd.Series(pred)
    df['degree'] = degrees
    f, c = df[df["pred"] == 1].shape
    print(f"Filas- {f}")
    df.to_csv(os.path.join(ruta_padre, 'anomalo.csv'), index=False)
    print("Terminado\n")


def main():
    for i in combinations:
        run_combination(i)


if __name__ == "__main__":
    main()
