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

## Instalación de dependencias
### Creación de entorno virtual
### Uso de GPU con CUDA
## Orden de ejecución

## Resultados
