# IACKATHON

## Nuestro Enfoque
En Ecuador, el problema de la corrupción en los procesos de compras públicas es cada vez más agravante. Con lo sucedido en la pandemia del Covid-19 en el año 2020 involucrando el sector Salud, era claro que se debían buscar formas más eficientes y rápidas para detectar anomalías en estos procesos. Por esto, se desarrolló este proyecto el cual se enfoca en detectar proveedores con comportamientos anómalos en su historial de compras públicas de un determinado período de tiempo. 
### Metodología 
![image](https://github.com/eapb99/IACKATHON/assets/73547550/29b0751b-f2be-4e47-ae92-22816e8b2892)

A continuación los pasos a detalle:
1. Se recolectaron datos desde la API OCDS para el SERCOP del sector Salud para el 2020.
2. Luego de analizar los datos estadísticamente, se crearon y calcularon métricas las cuales puedan modelar el comportamiento de los proveedores al subastar. Para una revisión más a fondo revisar el siguiente documento: (link a drive pdf de métricas)
3. Según las iteraciones del modelo y los resultados del mismo, los datos fueron filtrados y pasaron de ser 1497 proveedores a solo 142 proveedores. Principalmente se quitaron los proveedores cuyos datos hacían ruido en el modelo y causaban sesgo.
4. Para el modelo se aplicó una arquitectura [GAAN](https://dl.acm.org/doi/pdf/10.1145/3340531.3412070?casa_token=KktMH3R7VWIAAAAA:qzMSvod5cSSeBJhCh1NnFNFWsYs2QujGyH7ciyXS7YENjrYIbSQZdnzQPBmGETPBHNIL5d-lIkcFQg) el cual es un modelo de detección de anomalías en grafos atribuidos que aplica el concepto de capas GAN (Generative Adversarial Network). Este tipo de modelo tiene dos componentes: un generador y un discriminador; entrena el generador para crear nodos falsos lo más parecido posibles a los originales y, a su vez, entrena un discriminador para que identifique lo más precisamente posible si un noo es falso o no. Luego de finalizar el entrenamiento se coloca un puntaje de anomalía a cada nodo.
5. Se realizaron varias iteraciones del modelo probando diferentes combinaciones de hiperparámetros y cambios a los datos de entrenamiento.
6. Con los resultados obtenidos del modelo, en conjunto con los de la recolección de datos y las métricas, se creó un grafo que modela las relaciones entre proveedores. Los nodos representan los proveedores y las aristas significan una participación en una misma subasta entre dos proveedores.
7. Finalmente, se muestran los nodos anómalos de color rojo con sus características respectivas para su análisis pertinente.
## Estructura
Este proyecto está compuesto por tres subproyectos internos, cada uno con una funcionalidad específica. A continuación, se describen brevemente cada uno de estos subproyectos:

### 1. Compras Públicas
Este subproyecto se encarga de calcular métricas de transparencia. Estas métricas son esenciales para entender el comportamiento de un proveedor en los diferentes contratos en los que ha participado. El resultado de este proceso es un archivo CSV que contiene todas las métricas calculadas.

### 2. AnomalyDetection
El subproyecto `AnomalyDetection` toma el CSV de las métricas de transparencia creado por el subproyecto `Compras Públicas` y lo analiza para encontrar proveedores anómalos basados en sus métricas. Como resultado, se genera un nuevo CSV que incluye las mismas métricas, pero con cuatro columnas adicionales que permiten identificar qué proveedores son anómalos y cuáles no.

### 3. Visualization
Finalmente, el subproyecto `Visualization` utiliza el último CSV generado para crear un grafo. En este grafo, los proveedores que han sido identificados como anómalos se representan en color rojo, permitiendo así una fácil identificación visual.

Cada uno de estos subproyectos contribuye a la finalidad principal del proyecto, que es analizar y visualizar el comportamiento de los proveedores en contratos públicos, identificando posibles anomalías.

## Configuración del proyecto

Antes de comenzar, asegúrate de tener Python instalado en tu sistema. Se recomienda tener version >=3.10. A continuación, se describen los pasos para configurar el entorno virtual y instalar las dependencias necesarias.

### Creación de Entorno Virtual

Para crear un entorno virtual usando `venv` de Python, sigue estos pasos:
```sh
# Navega al directorio del proyecto
cd ruta/al/proyecto
# Crea el entorno virtual
python3 -m venv venv
# Activa el entorno virtual
source venv/bin/activate  # En Linux/macOS
.\venv\Scripts\activate   # En Windows
```

### Instalación de Dependencias
Una vez activado el entorno virtual, instala las dependencias del proyecto con el archivo requirements.txt.
```sh
pip install -r requirements.txt
```
### Instalación de Torch
Este proyecto utiliza torch y torch_geometric, y la instalación varía si se desea usar GPU o no.
#### Sin GPU
Sigue estos comandos para la instalación sin GPU:
```sh
pip3 install torch torchvision torchaudio
pip install torch_geometric
pip install torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-2.0.0+cpu.html
pip install pygod
```
#### Con GPU
*Recuerda verificar que tu sistema cumple con los requisitos para la instalación con GPU y CUDA.*

Para la instalación con GPU se necesita tener instalado [CudaToolTik 11.7.1](https://developer.nvidia.com/cuda-11-7-1-download-archive)
```sh
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
pip install torch_geometric
pip install torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-2.0.0+cu117.html
pip install pygod
```

## Orden de ejecución

Para el correcto funcionamiento del proyecto, es esencial seguir el orden de ejecución de los subproyectos y sus archivos correspondientes:
1. **Compras Públicas**: 
   - Ejecuta el archivo `metricas` situado dentro del subproyecto `Compras Publicas`.
   ```sh
   cd ComprasPublicas
   python metricas.py
   ```
2. **Anomaly Detection**: 
   - Ejecuta el archivo `anomaly` situado dentro del subproyecto `Anomaly Detection`.
   ```sh
   cd ../AnomalyDetection
   python anomaly.py
   ```
3. **Visualization**: 
   - Ejecuta el archivo `anomaly` situado dentro del subproyecto `Visualization`.
   ```sh
   cd ../Visualization
   python visualization.py
   ```
## Resultados
