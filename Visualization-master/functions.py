import numpy as np


def initial_positions_grid(G, caracteristicas):
    # Obtener clusters únicos
    unique_clusters = caracteristicas['cluster'].unique()

    # Calcular un espaciado basado en la raíz cuadrada del número de clusters
    spacing = int(np.ceil(np.sqrt(len(unique_clusters))))

    # Definir posiciones iniciales para centroides de clusters en una cuadrícula
    cluster_pos = {}
    for i, cluster in enumerate(unique_clusters):
        x = i % spacing
        y = i // spacing
        cluster_pos[cluster] = (x, y)

    # Asignar a cada nodo una posición inicial basada en su cluster
    init_pos = {}
    for node in G.nodes():
        cluster = caracteristicas.iloc[node]['cluster']
        init_pos[node] = cluster_pos[cluster]

    return init_pos


def scale_shell_positions(pos, scales):
    """
    Escala las posiciones de los nodos en un layout tipo shell.

    Parámetros:
    pos (dict): Diccionario de posiciones generadas por nx.shell_layout.
    scales (list): Lista de factores de escala para cada capa. Por ejemplo, [0.5, 1, 1.5]
                  escalará la capa más interna a la mitad de su radio original,
                  dejará la capa del medio igual, y expandirá la capa externa en 1.5 veces.

    Devuelve:
    dict: Diccionario de posiciones ajustadas.
    """
    scaled_pos = {}
    for node, position in pos.items():
        x, y = position
        distance_from_center = np.sqrt(x ** 2 + y ** 2)

        # Detecta a qué capa pertenece el nodo basado en su distancia al centro
        layer = int(round(distance_from_center))

        # Escala las coordenadas
        scaling_factor = scales[layer]
        scaled_pos[node] = (x * scaling_factor, y * scaling_factor)

    return scaled_pos


def initial_positions(G, caracteristicas):
    # Obtener clusters únicos
    unique_clusters = caracteristicas['cluster'].unique()

    # Definir posiciones iniciales para centroides de clusters (este es solo un ejemplo básico)
    cluster_pos = {}
    for i, cluster in enumerate(unique_clusters):
        angle = 2 * np.pi * i / len(unique_clusters)
        cluster_pos[cluster] = (np.cos(angle), np.sin(angle))

    # Asignar a cada nodo una posición inicial basada en su cluster
    init_pos = {}
    for node in G.nodes():
        cluster = caracteristicas.iloc[node]['cluster']
        init_pos[node] = cluster_pos[cluster]

    return init_pos
