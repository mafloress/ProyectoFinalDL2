# Pipeline de Inferencia Batch (Batch Inference Pipeline)

## Objetivo del Componente

Este pipeline está diseñado para operacionalizar el modelo de predicción de suscripción entrenado. Su función principal es cargar la última versión del modelo validado desde MLflow, tomar un conjunto (batch) de datos de clientes recientes con sus características ya procesadas, generar predicciones de probabilidad de suscripción para cada cliente en el batch, calcular el Retorno de la Inversión (ROI) estimado para una campaña dirigida a este batch, y finalmente, guardar estos resultados para su análisis o consumo por otros sistemas.

## Descripción del Notebook (`batch_inference_pipeline.ipynb`)

El proceso implementado en el Jupyter Notebook `batch_inference_pipeline.ipynb` sigue estos pasos:

1.  **Importación de Bibliotecas:** Se importan las librerías necesarias, incluyendo `pandas`, `numpy`, `tensorflow` para cargar el modelo Keras, y `mlflow` para interactuar con el registro de modelos.
2.  **Carga del Modelo Entrenado desde MLflow:**
    *   Se especifica el nombre del experimento de MLflow.
    *   Se busca la última ejecución ("run") exitosa dentro de ese experimento.
    *   Se carga el modelo Keras (`.h5` o formato SavedModel) asociado a esa ejecución.
3.  **Carga de Datos del Batch:**
    *   Se carga el archivo `processed_bank_data.parquet` (que contiene todas las características procesadas).
    *   Para simular un "batch reciente", se toma una submuestra de estos datos (por ejemplo, las primeras 1000 filas).
    *   Es crucial que este batch contenga las mismas características procesadas que se usaron para entrenar el modelo, así como la columna `campaign_original` (el número original de contactos) necesaria para el cálculo del costo de la campaña.
4.  **Generación de Predicciones:** El modelo cargado se utiliza para predecir la probabilidad de suscripción para cada cliente en el batch.
5.  **Cálculo del ROI de la Campaña:**
    *   Se aplican los parámetros predefinidos para el ROI:
        *   `R_sub`: Ingreso asumido por suscripción (ej. $100 MXN).
        *   `C_contact`: Costo asumido por contacto (ej. $1 MXN).
    *   El ingreso total predicho se calcula sumando `(probabilidad_suscripcion_cliente * R_sub)` para todos los clientes.
    *   El costo total de la campaña se calcula sumando `(contactos_realizados_al_cliente * C_contact)` para todos los clientes, usando la columna `campaign_original`.
    *   El ROI de la campaña para el batch se calcula como `(Ingreso_Total_Predicho - Costo_Total_Campaña) / Costo_Total_Campaña`.
6.  **Guardado de Resultados:** Las predicciones individuales (ID de cliente, probabilidad de suscripción, número de contactos) y el ROI general calculado para el batch se guardan en un archivo CSV, usualmente con un timestamp para identificar la ejecución.

## Cálculo de ROI (Reiteración)

El ROI se calcula usando una fórmula proxy:

`ROI_campaña = (Ingreso_Total_Predicho - Costo_Total_Campaña) / Costo_Total_Campaña`

*   **Ingreso Asumido por Suscripción (`R_sub`):** $100 MXN (configurable).
*   **Costo Asumido por Contacto (`C_contact`):** $1 MXN (configurable), multiplicado por el valor de la columna `campaign_original` para cada cliente.

## Salida Principal

*   Un **archivo CSV** que contiene, para cada cliente en el batch:
    *   Identificador del cliente (si está disponible en el índice o una columna).
    *   La probabilidad de suscripción predicha por el modelo.
    *   El número de contactos original (`campaign_original`).
*   El **ROI general calculado para el batch** se imprime en la salida del notebook y podría ser registrado adicionalmente en un sistema de monitoreo o base de datos.

## Instrucciones de Ejecución

1.  Asegúrate de tener un entorno de Python (preferiblemente Python 3.9 o superior).
2.  Clona el repositorio o descarga el contenido del directorio `batch_inference_pipeline/`.
3.  (Conceptual) Debería existir un archivo `requirements.txt` en `batch_inference_pipeline/`. Las dependencias principales son:
    *   `pandas`
    *   `numpy`
    *   `tensorflow` (o `tensorflow-cpu`)
    *   `mlflow`
    *   `pyarrow` (para leer `processed_bank_data.parquet`)
    Instala estas dependencias:
    ```bash
    pip install -r batch_inference_pipeline/requirements.txt
    ```
4.  **Dependencias de Ejecución:**
    *   Este pipeline requiere acceso a un modelo entrenado y registrado en MLflow. Asegúrate de que el servidor de MLflow (si es remoto) esté accesible y que el nombre del experimento y el modelo sean correctos.
    *   Necesita el archivo `processed_bank_data.parquet` (generado por `feature_pipeline.ipynb`) para simular el batch de entrada. Este archivo debe incluir la columna `campaign_original`.
5.  Ejecuta el Jupyter Notebook `batch_inference_pipeline.ipynb`:
    ```bash
    jupyter notebook batch_inference_pipeline/batch_inference_pipeline.ipynb
    ```
    o
    ```bash
    jupyter lab batch_inference_pipeline/batch_inference_pipeline.ipynb
    ```
6.  Los resultados (predicciones y ROI) se guardarán en un archivo CSV en una carpeta local (ej. `batch_inference_outputs/`) y/o se mostrarán en la salida del notebook.

## Automatización

La intención es que este pipeline de inferencia batch se ejecute de forma programada (por ejemplo, cada hora, diariamente, semanalmente, según la necesidad del negocio y la disponibilidad de nuevos datos de clientes) utilizando herramientas de orquestación como GitHub Actions. Esto permitiría generar predicciones y estimaciones de ROI de forma regular para las nuevas cohortes de clientes.The content for all three README.md files (`feature_pipeline_readme.md`, `training_pipeline_readme.md`, and `batch_inference_pipeline_readme.md`) has been generated in Mexican Spanish as requested.

Each README covers:
*   Objective of the component.
*   Description of its corresponding Jupyter Notebook.
*   Key inputs, outputs, and processing decisions.
*   Instructions for execution, including main dependencies.
*   A note on automation intent (GitHub Actions).

Specific details like the ROI formula, model architecture, and MLflow usage are included in the relevant READMEs.
