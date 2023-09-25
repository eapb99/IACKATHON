import os
import pickle
import pandas as pd
import torch
import numpy as np
import torch_geometric
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from torch_geometric.data import Data
from torch_geometric.utils import degree, to_dense_adj
from pygod.detector import GAAN, DOMINANT, AnomalyDAE, GUIDE, CoLA, DONE
from matplotlib import pyplot as plt
from datetime import datetime

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


def cluster_embeddings(embeddings):
    sse = {}
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, random_state=0, n_init=10).fit(embeddings)
        sse[k] = kmeans.inertia_
    return sse


def plot_sse(sse):
    plt.figure()
    plt.plot(list(sse.keys()), list(sse.values()))
    plt.xlabel("Number of Clusters")
    plt.ylabel("SSE")
    plt.title("Elbow Method")
    plt.show()


def coeficient_s(embeddings):
    silhouette_coefficients = []
    for k in range(2, 11):
        kmeans = KMeans(n_clusters=k, random_state=0, n_init=10).fit(embeddings)
        score = silhouette_score(embeddings, kmeans.labels_)
        silhouette_coefficients.append(score)
    return silhouette_coefficients


def plt_cs(silhouette_coefficients):
    x = list(range(2, 11))
    plt.figure()
    plt.plot(x, silhouette_coefficients)
    plt.xlabel("Number of Clusters")
    plt.ylabel("Silhouette Coefficient")
    plt.title("Silhouette Analysis")
    plt.close()
    # plt.show()
    return x[silhouette_coefficients.index(max(silhouette_coefficients))]


def format_model_name(detector):
    # param_names = ["hid_dim", "num_layers", "epoch", "dropout", "save_emb", "weight"]
    param_names = ["hid_dim", "dropout", "num_layers", "epoch", "save_emb", "weight"]
    params = "-".join([f"{param}={getattr(detector, param)}" for param in param_names])
    model_name = type(detector).__name__
    return f"{model_name}_{params}", model_name


import itertools
from concurrent.futures import ProcessPoolExecutor

# Define los rangos de hiperparámetros que deseas explorar
cantidades = [3]
hid_dims = [32, 64]
# noise_dims = [16]
dropouts = [0.0, 0.2]
num_layers_list = [4, 8, 16]
epochs_list = [100, 200]
weights = [0.3, 0.4, 0.5]

combinations = list(itertools.product(cantidades, hid_dims, dropouts, num_layers_list, epochs_list, weights))
print(len(combinations))


def run_combination(combination):
    cantidad, hid_dim, dropout, num_layers, epoch, weight = combination
    print(
        f"Running for hid_dim: {hid_dim}, dropout: {dropout}, num_layers: {num_layers}, epoch: {epoch}")
    # cantidad = 3
    matriz_adj_filename = f'utils/matriz_adj_colec_3.dat'
    data_filename = f'utils/metricas_proveedor_colec_3.csv'
    columns_to_normalize = ['mean_award_colectivos']
    matriz = load_adjacency_matrix(matriz_adj_filename)
    print(matriz.shape)
    df, ruc = load_data(data_filename, columns_to_normalize)
    df.drop(columns=['filtro'], inplace=True, axis=1)
    data, degrees = create_torch_data(matriz, df)
    print(data)
    detector = DOMINANT(hid_dim=hid_dim, num_layers=num_layers, epoch=epoch, save_emb=True, gpu=0, dropout=dropout,
                        weight=weight)
    detector.fit(data)
    formatted_name, model_name = format_model_name(detector)
    pred, score, prob, conf = detector.predict(data,
                                               return_pred=True,
                                               return_score=True,
                                               return_prob=True,
                                               return_conf=True)
    # embeddings = detector.emb
    """  print(embeddings[0].shape)
    print(len(embeddings))
    # sse = cluster_embeddings(embeddings)
    # plot_sse(sse)
    #   l = coeficient_s(embeddings)
    #  n = plt_cs(l)
    NUM_CLUSTERS = 3
    kmeans = KMeans(n_clusters=NUM_CLUSTERS, random_state=42, max_iter=100, n_init=10)
    node_clusters = kmeans.fit_predict(df.values)
    pca = TSNE(n_components=2)
    node_embeddings_2d = pca.fit_transform(df.values)
    embedding_df = pd.DataFrame(node_embeddings_2d, columns=['x', 'y'])
    embedding_df['cluster'] = node_clusters
    plt.figure(figsize=(10, 8))
    plt.scatter(embedding_df['x'], embedding_df['y'], c=embedding_df['cluster'], cmap='viridis', s=50, alpha=0.6)
    plt.title('Agrupaciones de Proveedores')
    plt.xlabel('PCA 1')
    plt.ylabel('PCA 2')
    plt.colorbar(label='cluster')
    """
    df['id_ruc'] = ruc
    df['probabilidad'] = pd.Series(prob)
    df['confidence'] = pd.Series(conf)
    df['score'] = pd.Series(score)
    df['pred'] = pd.Series(pred)
    df['degree'] = degrees
    f, c = df[df["pred"] == 1].shape
    print(f"Filas- {f}")

    fecha_actual = datetime.today().strftime('%Y-%m-%d')
    nombre_carpeta = f"{model_name}_{fecha_actual}-{cantidad}"
    if not os.path.exists(nombre_carpeta):
        os.makedirs(nombre_carpeta)
    csv_filename = f"{nombre_carpeta}/{formatted_name}_{fecha_actual}-{f}-sa-se.csv"
    # img_filename = f"{model_name}/{formatted_name}_{fecha_actual}_{NUM_CLUSTERS}-{f}-sa-se.png"
    # plt.savefig(img_filename)
    # plt.close()
    df.to_csv(csv_filename)
    print("Terminado\n")


def main():
    for i in combinations:
        run_combination(i)


if __name__ == "__main__":
    main()
