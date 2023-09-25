import pickle
import pandas as pd
import networkx as nx
from pyvis.network import Network


def str_name(node):
    formatted_details = [f"{key}: {value:.2f}" if isinstance(value, (int, float)) else f"{key}: {value}" for key, value
                         in node.items()]
    return "\n".join(formatted_details)


def rename_columns(df, old_names, new_names):
    column_mapping = dict(zip(old_names, new_names))
    df.rename(columns=column_mapping, inplace=True)


def load_data(adjacency_matrix_file, dataframe_file, old_names, new_names):
    with open(adjacency_matrix_file, "rb") as file:
        adjacency_matrix = pickle.load(file)
    df = pd.read_csv(dataframe_file, index_col=0)
    rename_columns(df, old_names, new_names)
    return adjacency_matrix, df


def create_graph(adjacency_matrix, df):
    G = nx.from_numpy_array(adjacency_matrix)
    df.drop(['probabilidad', 'score', 'confidence'], inplace=True, axis=1)
    for index, row in df.iterrows():
        node_id = index
        G.nodes[node_id]["label"] = ""
        G.nodes[node_id]["size"] = row["Ofertados"]
        for column in df.columns:
            if column not in ["Id_RUC", "Ofertados"]:
                G.nodes[node_id][column] = row[column]
    return G


def create_network(G):
    nt = Network(notebook=True, filter_menu=True, neighborhood_highlight=True)
    nt.from_nx(G)
    for node in nt.nodes:
        details = str_name(node)
        node["title"] = details
        node["value"] = node["size"]
        if node['Anomalia'] == 1:
            node['color'] = f'rgb(255,0,0)'
    nt.toggle_physics(False)
    #   nt.show_buttons(filter_=['physics'])
    return nt


def main(adjacency_matrix_file, dataframe_file, output_file, old_names, new_names):
    adjacency_matrix, df = load_data(adjacency_matrix_file, dataframe_file, old_names, new_names)
    G = create_graph(adjacency_matrix, df)
    nt = create_network(G)
    nt.show(output_file)


if __name__ == "__main__":
    adjacency_matrix_file = "utils/matriz_adj_colec_3.dat"
    dataframe_file = "utils/GAAN_hid_dim=64-noise_dim=16-dropout=0.0-num_layers=4-epoch=100-save_emb=True-weight=0.3_2023-08-18-13-3-sa-se.csv"
    output_file = "grafo-colect-3.html"
    old_names = ["% colectivos", "% perdidos", "ofertados", "desviacion_mean_colectivos",
                 "diff_planning_mean_colectivos",
                 "desviacion_mean_perdidos", "diff_award_mean_perdidos", "diff_planning_mean_perdidos",
                 "mean_indice_ausencia",
                 "range_indice_ausencia", "mean_ofertas_colectivos", "mean_frecuencia_colectivos",
                 "mean_award_colectivos",
                 "mean_frecuencia_perdidos", "mean_ofertas_perdidos", "id_ruc", "probabilidad", "confidence", "score",
                 "pred",
                 "degree"]

    new_names = ['Porcentaje Contrato Colectivos', 'Porcentaje Contrato Perdidos', 'Ofertados',
                 'Desviacion Estandar Promedio (Colectivo)',
                 'Promedio de la ultima oferta respecto al monto planeado(Colectivo)',
                 'Desviacion Estandar Promedio (Perdidos)',
                 'Promedio de la ultima oferta respecto al monto ganador(Perdidos)',
                 'Promedio de la ultima oferta respecto al monto planeado(Perdidos)', 'Promedio Indice de Clasifiacion',
                 'Rango Indice de ausencia', 'Promedio de ofertas(Colectivos)', 'Promedio de Frencuencia(Colectivos)',
                 'Monto Promedio Ganado((Colectivos)', 'Promedio de Frencuencia(Perdidos)', 'Monto Promedio (Perdidos)',
                 "Id_RUC", "probabilidad", 'confidence', 'score', 'Anomalia', 'Conexiones']

    main(adjacency_matrix_file, dataframe_file, output_file, old_names, new_names)
