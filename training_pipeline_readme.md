# Pipeline de Entrenamiento del Modelo (Training Pipeline)

## Objetivo del Componente

El propósito fundamental de este pipeline es cargar las características preprocesadas (generadas por el `feature_pipeline`), definir una arquitectura de modelo de Deep Learning (Red Neuronal Densa - DNN), entrenar este modelo para predecir la probabilidad de que un cliente se suscriba a un depósito a plazo, y finalmente, registrar el modelo entrenado, sus parámetros y métricas de rendimiento utilizando MLflow. Este proceso asegura un entrenamiento de modelos reproducible y versionado.

## Descripción del Notebook (`training_pipeline.ipynb`)

El Jupyter Notebook `training_pipeline.ipynb` orquesta el proceso de entrenamiento a través de los siguientes pasos:

1.  **Importación de Bibliotecas:** Se importan las librerías necesarias, incluyendo `pandas` para manipulación de datos, `scikit-learn` para la división de datos y métricas, `tensorflow.keras` para la construcción del modelo DNN, y `mlflow` para el seguimiento.
2.  **Configuración de MLflow:** Se establece un nombre para el experimento en MLflow para organizar las diferentes ejecuciones de entrenamiento.
3.  **Carga de Datos Procesados:** Se carga el archivo `processed_bank_data.parquet` (la salida del `feature_pipeline`), que contiene las características listas para el modelado.
4.  **División de Datos:** Los datos se dividen en conjuntos de entrenamiento (70%), validación (15%) y prueba (15%). La estratificación se utiliza para mantener la proporción de la variable objetivo en cada conjunto, lo cual es importante dado el desbalance de clases.
5.  **Definición de la Arquitectura DNN (Keras):** Se construye un modelo secuencial de Keras. La arquitectura incluye:
    *   Una capa de entrada (`Input`) que coincide con el número de características procesadas.
    *   Capas densas (`Dense`) con funciones de activación ReLU.
    *   Capas de regularización `Dropout` para prevenir el sobreajuste.
    *   Una capa de salida `Dense` con una neurona y activación sigmoide, adecuada para la clasificación binaria (probabilidad de suscripción).
6.  **Compilación del Modelo:** El modelo se compila especificando:
    *   Optimizador: `Adam`.
    *   Función de Pérdida: `binary_crossentropy` (apropiada para clasificación binaria).
    *   Métricas: `accuracy` y `AUC` (Área Bajo la Curva ROC).
7.  **Entrenamiento del Modelo:**
    *   El entrenamiento se realiza dentro de un contexto de ejecución de MLflow (`mlflow.start_run()`).
    *   `mlflow.tensorflow.autolog()` se utiliza para registrar automáticamente parámetros, métricas y el modelo Keras.
    *   Se emplea un callback `EarlyStopping` para monitorear la pérdida en el conjunto de validación (`val_loss`) y detener el entrenamiento si no hay mejora después de un número determinado de épocas (paciencia), restaurando los mejores pesos del modelo.
8.  **Evaluación del Modelo:**
    *   El modelo entrenado se evalúa sobre el conjunto de prueba para obtener una estimación imparcial de su rendimiento en datos no vistos.
    *   Se calculan y registran métricas adicionales como precisión, recall y F1-score.
9.  **Registro del Modelo en MLflow:** Aunque `autolog` ya registra el modelo, se reitera que el modelo final (con los mejores pesos gracias a `EarlyStopping`) queda almacenado como un artefacto de la ejecución de MLflow.

## Modelo y Evaluación

*   **Arquitectura DNN:**
    *   Capa de Entrada: `Input(shape=(numero_de_caracteristicas,))`
    *   Primera Capa Densa: 128 neuronas, activación ReLU.
    *   Dropout: Tasa de 0.3.
    *   Segunda Capa Densa: 64 neuronas, activación ReLU.
    *   Dropout: Tasa de 0.3.
    *   Capa de Salida: 1 neurona, activación sigmoide.
*   **Métricas de Evaluación Clave:**
    *   **Pérdida (Loss):** `binary_crossentropy` (durante el entrenamiento y evaluación).
    *   **Exactitud (Accuracy):** Proporción de predicciones correctas.
    *   **AUC (Area Under the ROC Curve):** Métrica robusta para clasificación binaria, especialmente útil con clases desbalanceadas. Indica la capacidad del modelo para distinguir entre clases.
    *   Adicionalmente se calculan Precision, Recall y F1-score sobre el conjunto de prueba.

## Uso de MLflow

MLflow juega un papel crucial en este pipeline:
*   **Seguimiento de Experimentos:** Cada ejecución del notebook de entrenamiento (o variaciones con diferentes hiperparámetros) puede ser registrada como una "run" dentro de un experimento definido.
*   **Registro de Parámetros:** Hiperparámetros como la tasa de aprendizaje, número de épocas, tamaño del batch, y la arquitectura del modelo son registrados.
*   **Registro de Métricas:** Todas las métricas evaluadas durante el entrenamiento (en cada época para los conjuntos de entrenamiento y validación) y en la evaluación final sobre el conjunto de prueba son almacenadas.
*   **Versionado y Almacenamiento de Modelos:** El modelo Keras entrenado se guarda como un artefacto. Esto permite cargar una versión específica del modelo en etapas posteriores, como en el pipeline de inferencia batch.

## Salida Principal

La salida principal de este pipeline es:
*   Un **modelo Keras (.h5 o formato SavedModel de TensorFlow) entrenado y sus pesos asociados**, almacenados como un artefacto dentro de la ejecución de MLflow correspondiente.
*   **Registros detallados en MLflow** que incluyen parámetros, métricas por época, métricas finales de evaluación y el propio modelo.

## Instrucciones de Ejecución

1.  Asegúrate de tener un entorno de Python (preferiblemente Python 3.9 o superior).
2.  Clona el repositorio o descarga el contenido del directorio `training_pipeline/`.
3.  (Conceptual) Debería existir un archivo `requirements.txt` en `training_pipeline/`. Las dependencias principales son:
    *   `pandas`
    *   `numpy`
    *   `scikit-learn`
    *   `tensorflow` (o `tensorflow-cpu` si no se usará GPU)
    *   `mlflow`
    *   `pyarrow` (para leer `processed_bank_data.parquet`)
    Instala estas dependencias:
    ```bash
    pip install -r training_pipeline/requirements.txt
    ```
4.  **Dependencia de Datos:** Este pipeline requiere el archivo `processed_bank_data.parquet` generado por `feature_pipeline.ipynb`. Asegúrate de que este archivo exista en la ruta esperada (por defecto, se busca en `../feature_pipeline/data/processed_bank_data.parquet`).
5.  **Servidor MLflow:** Necesitarás tener un servidor de MLflow ejecutándose o configurar MLflow para que guarde los datos localmente (por defecto, crea una carpeta `mlruns` en el directorio desde donde se ejecuta). Para iniciar un servidor local simple: `mlflow ui`.
6.  Ejecuta el Jupyter Notebook `training_pipeline.ipynb`:
    ```bash
    jupyter notebook training_pipeline/training_pipeline.ipynb
    ```
    o
    ```bash
    jupyter lab training_pipeline/training_pipeline.ipynb
    ```
7.  Los resultados del entrenamiento, incluyendo el modelo, se registrarán en MLflow. Puedes visualizarlos abriendo la interfaz de usuario de MLflow.

## Automatización

Al igual que otros pipelines, la intención es que el pipeline de entrenamiento pueda ser automatizado usando GitHub Actions. Esto permitiría reentrenar el modelo periódicamente o cuando se detecte una degradación significativa de su rendimiento (model drift) o un cambio en la distribución de los datos (data drift).
