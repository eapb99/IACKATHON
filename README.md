# IACKATHON

[IACKATHON](#iackathon)
  * [Nuestro Enfoque](#nuestro-enfoque)
    + [Metodología](#metodología)
  * [Estructura](#estructura)
    + [Compras Públicas](#compras-públicas)
    + [AnomalyDetection](#anomalydetection)
    + [Visualization](#visualization)
  * [Configuración del proyecto](#configuración-del-proyecto)
    + [Creación de Entorno Virtual](#creación-de-entorno-virtual)
    + [Instalación de Dependencias](#instalación-de-dependencias)
    + [Instalación de Torch](#instalación-de-torch)
      - [Sin GPU](#sin-gpu)
      - [Con GPU](#con-gpu)
  * [Orden de ejecución](#orden-de-ejecución)
  * [Dataset Utilizado](#dataset-utilizado)
  * [Resultados](#resultados)
    + [Capturas](#capturas)
    + [Nodos interactivos](#nodos-interactivos)
    + [Filtrar nodos](#filtrar-nodos)
  * [Implicaciones éticas y legales](#implicaciones-éticas-y-legales)
  * [Resultados](#resultados)
  * [Dataset Utilizado](#dataset-utilizado)

## Nuestro Enfoque
En Ecuador, el problema de la corrupción en los procesos de compras públicas es cada vez más agravante. Con lo sucedido en la pandemia del Covid-19 en el año 2020 involucrando el sector Salud, era claro que se debían buscar formas más eficientes y rápidas para detectar anomalías en estos procesos. Por esto, se desarrolló este proyecto el cual se enfoca en detectar proveedores con comportamientos anómalos en su historial de compras públicas de un determinado período de tiempo. 
### Metodología 

![image](https://github.com/eapb99/IACKATHON/assets/73547550/87236d7a-af18-4d47-a446-c3925559fc93)

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

- ### Compras Públicas
Este subproyecto se encarga de calcular métricas de transparencia. Estas métricas son esenciales para entender el comportamiento de un proveedor en los diferentes contratos en los que ha participado. El resultado de este proceso es un archivo CSV que contiene todas las métricas calculadas.

- ### AnomalyDetection
El subproyecto `AnomalyDetection` toma el CSV de las métricas de transparencia creado por el subproyecto `Compras Públicas` y lo analiza para encontrar proveedores anómalos basados en sus métricas. Como resultado, se genera un nuevo CSV que incluye las mismas métricas, pero con cuatro columnas adicionales que permiten identificar qué proveedores son anómalos y cuáles no.

- ### Visualization
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
   - Ejecuta el archivo `visualization` situado dentro del subproyecto `Visualization`.
   ```sh
   cd ../Visualization
   python visualization.py
   ```

## Dataset Utilizado

La data recopilada del API OCDS corresponde a los contratos de tipo SUBASTA INVERSA realizados en el año 2020 del sector SALUD. A esta data se la manipuló y luego se organizó en un json general el cual posee una lista de objetos que representan la información de cada contrato con el siguiente formato:

```
[
    {
        "_id": {
            "$oid": "640e11fa5fc36205c1a0306d"
        },
        "ocid": "ocds-5wno2w-SIE-01-HOJ-2020-562623",
        "amount_award": 27692,
        "current_stage": "contract",
        "datetime": {
            "$date": "2020-01-31T05:00:00.000Z"
        },
        "description": "ADQUISICION DE REACTIVOS DE BIOQUIMICA PARA LABORATORIO",
        "entity_id": "EC-RUC-2060018360001-562623",
        "entity_name": "HOSPITAL OSKAR JANDL",
        "hash": "3a26c7c2cebaebc7a3f367ec9a25e5aa82195c6a4567455f98ddb802fe2dffad",
        "items": [
            "2993283-DS-SO"
        ],
        "mainProcurementCategory": "goods",
        "numberTenderers": 2,
        "parties": [
            "EC-RUC-0993038997001-848130",
            "EC-RUC-0993222100001-966786",
            "EC-RUC-2060018360001-562623"
        ],
        "procurementMethod": "open",
        "procurementMethodDetails": "Subasta Inversa Electr\u00f3nica",
        "procurementMethodDetails_sercop": "Subasta Inversa Electr\u00f3nica",
        "sector": "SALUD",
        "suppliers": [
            "EC-RUC-0993222100001-966786"
        ],
        "tag": [
            "planning",
            "tender",
            "award",
            "contract",
            "implementation"
        ],
        "tenders": [
            "EC-RUC-0993038997001-848130"
        ],
        "title": "SIE-01-HOJ-2020-562623",
        "bids_amounts": [
            28258.78,
            28258.78,
            27692.3,
            27692
        ],
        "amount_planning": 28273.9,
        "bidders_ruc": [
            "EC-RUC-0993038997001-848130",
            "EC-RUC-0993222100001-966786",
            "EC-RUC-0993038997001-848130",
            "EC-RUC-0993222100001-966786"
        ],
        "date_list": [
            "2020-02-12T16:56:34-05:00",
            "2020-02-12T16:59:24-05:00",
            "2020-02-13T10:06:03-05:00",
            "2020-02-13T10:06:44-05:00"
        ],
        "num_bids": 4
    },
.
.
.    ,
    {
        "_id": {
            "$oid": "640e122b5fc36205c1a038a8"
        },
        "ocid": "ocds-5wno2w-SIEB-HEFFAA-001-2020-43246",
        "amount_award": 66145.92,
        "current_stage": "contract",
        "datetime": {
            "$date": "2020-01-29T05:00:00.000Z"
        },
        "description": "ADQUISICI\u00d3N  DE REACTIVOS PARA SISTEMA  AUTOMATIZADO DE DIAGN\u00d3STICO IN VITRO PARA DETECTAR SECUENCIAS ESPEC\u00cdFICAS DE \u00c1CIDOS NUCLEICOS MEDIANTE PCR, A UTILIZARSE EN EL LABORATORIO DE MICROBIOLOG\u00cdA DEL HE-1",
        "entity_id": "EC-RUC-1768012710001-43246",
        "entity_name": "HOSPITAL DE ESPECIALIDADES FUERZAS ARMADAS NO. 1",
        "hash": "8d8b73660f075b34c553ecd548d7b29fb131d01a3647902aca899bcdc09f5bb6",
        "items": [
            "2993618-DS-SO"
        ],
        "mainProcurementCategory": "goods",
        "numberTenderers": 1,
        "parties": [
            "EC-RUC-1768012710001-43246",
            "EC-RUC-1790691810001-4033"
        ],
        "procurementMethod": "open",
        "procurementMethodDetails": "Subasta Inversa Electr\u00f3nica",
        "procurementMethodDetails_sercop": "Subasta Inversa Electr\u00f3nica",
        "sector": "SALUD",
        "suppliers": [
            "EC-RUC-1790691810001-4033"
        ],
        "tag": [
            "planning",
            "tender",
            "award",
            "contract",
            "implementation"
        ],
        "tenders": [],
        "title": "SIEB-HEFFAA-001-2020-43246",
        "bids_amounts": [
            71316.4,
            66145.92
        ],
        "amount_planning": 71318.4,
        "bidders_ruc": [
            "EC-RUC-1790691810001-4033",
            "EC-RUC-1790691810001-4033"
        ],
        "date_list": [
            "2020-02-13T08:41:44-05:00",
            "2020-02-19T09:00:47-05:00"
        ],
        "num_bids": 2
    }
]
```

## Resultados

### Capturas

![image](https://github.com/eapb99/IACKATHON/assets/73547550/cf20e4f6-f37a-4e4d-bf76-d61946b1d6bb)

![image](https://github.com/eapb99/IACKATHON/assets/73547550/1a50ceca-f4c6-4d7c-9394-9e069e13fc69)

![image](https://github.com/eapb99/IACKATHON/assets/73547550/6d6307ca-af4f-4e99-bf7c-e19463d0e116)

### Nodos interactivos

![manipular nodos gif](https://github.com/eapb99/IACKATHON/assets/73547550/281522c7-82b2-41a3-8f68-f4d583c150b6)

### Filtrar nodos

![filtrar nodos gif](https://github.com/eapb99/IACKATHON/assets/73547550/a6c638b9-dc96-45db-9c06-bcc392dae4bf)

## Implicaciones éticas y legales

Es importante tener en cuenta las consideraciones éticas y legales al interpretar los resultados. Aunque el modelo identificó a varios proveedores como anómalos, esto no significa necesariamente que estén involucrados en actividades ilícitas o irregulares.  Un proveedor puede ser identificado como anómalo debido a una variedad de razones, como un número inusualmente alto de contratos, una cantidad significativa de contratos únicos, o una estructura de relaciones inusuales. Por lo tanto, es fundamental no sacar conclusiones apresuradas sobre la legalidad o ética de un proveedor basándose únicamente en los resultados obtenidos.
Además, es crucial mantener la confidencialidad de los datos y respetar las leyes de protección de datos. Aunque los datos utilizados en este estudio son de dominio público, la identificación de proveedores anómalos puede tener implicaciones legales y reputacionales para los proveedores involucrados. 
