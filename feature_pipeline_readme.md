# Pipeline de Características (Feature Pipeline)

## Objetivo del Componente

Este pipeline es responsable de tomar los datos crudos del dataset "Bank Marketing", realizar la limpieza necesaria, y aplicar un preprocesamiento robusto. Esto incluye la transformación de la variable objetivo, la identificación y separación de variables numéricas y categóricas, el escalado de características numéricas, la codificación (one-hot encoding) de características categóricas, y el manejo específico de valores 'unknown'. El resultado final es un conjunto de características procesadas y listas para ser utilizadas en el entrenamiento de modelos de machine learning.

## Descripción del Notebook (`feature_pipeline.ipynb`)

El Jupyter Notebook `feature_pipeline.ipynb` implementa los siguientes pasos clave:

1.  **Carga de Datos:** Se carga el dataset `bank-full.csv`. El notebook incluye lógica para descargar y descomprimir el archivo si no se encuentra localmente en un subdirectorio `data/`.
2.  **Conversión de la Variable Objetivo:** La variable objetivo `y` (que indica si un cliente se suscribió o no) se convierte a formato binario (0 para 'no', 1 para 'yes').
3.  **Identificación de Tipos de Columnas:** Se separan las columnas en numéricas y categóricas. La variable objetivo `y` se excluye de las características a transformar.
4.  **Manejo de Valores 'Unknown':** Se discute cómo `OneHotEncoder` manejará los valores 'unknown' presentes en algunas columnas categóricas. Con `handle_unknown='ignore'`, cualquier categoría no vista durante el `fit` (incluyendo 'unknown' si no estaba en el set de entrenamiento original para una columna específica, o nuevas categorías en datos futuros) será codificada como un vector de ceros, evitando errores en producción.
5.  **Aplicación de `ColumnTransformer`:**
    *   **Para Variables Numéricas:** Se aplica `StandardScaler` para estandarizar estas características (media cero y desviación estándar unitaria).
    *   **Para Variables Categóricas:** Se aplica `OneHotEncoder` para convertir las variables categóricas en un formato numérico que el modelo pueda procesar. `sparse_output=False` se usa para obtener un array denso.
6.  **Reconstrucción del DataFrame:** El array NumPy resultante de `ColumnTransformer` se convierte de nuevo en un DataFrame de Pandas, asignando nombres de columna adecuados a las nuevas características codificadas.
7.  **Guardado de Datos:** Las características procesadas, junto con la variable objetivo `y` y una copia de la columna original `campaign` (renombrada a `campaign_original` para el cálculo de ROI en la inferencia), se guardan en un archivo formato Parquet.

## Salida Principal

La salida principal de este pipeline es el archivo `processed_bank_data.parquet`, ubicado en el subdirectorio `feature_pipeline/data/`. Este archivo contiene:
*   Todas las características numéricas escaladas.
*   Todas las características categóricas codificadas (one-hot).
*   La variable objetivo `y` en formato binario.
*   La columna `campaign_original` con los valores crudos del número de contactos, esencial para el cálculo del ROI en el pipeline de inferencia.

Este archivo simula la salida que se almacenaría en un **Feature Store** en un sistema MLOps más maduro, proveyendo características consistentes y listas para el consumo.

## Decisiones Clave de Procesamiento

*   **Manejo de 'unknown':** Los valores 'unknown' en las variables categóricas son tratados como una categoría más por el `OneHotEncoder` si están presentes durante el ajuste. Si aparecen nuevas categorías (o 'unknown' en columnas donde no se vio antes) durante la transformación, `handle_unknown='ignore'` asegura que se codifiquen como ceros sin generar errores.
*   **Scaling (Escalado):** Se utiliza `StandardScaler` para las variables numéricas. Esto es crucial para modelos sensibles a la escala de las características, como las redes neuronales.
*   **Encoding (Codificación):** Se emplea `OneHotEncoder` para las variables categóricas, transformándolas en múltiples columnas binarias.

## Instrucciones de Ejecución

1.  Asegúrate de tener un entorno de Python (preferiblemente Python 3.9 o superior).
2.  Clona el repositorio o descarga el contenido del directorio `feature_pipeline/`.
3.  (Conceptual) Debería existir un archivo `requirements.txt` dentro del directorio `feature_pipeline/` listando las dependencias. Las dependencias principales para este notebook incluyen:
    *   `pandas`
    *   `numpy`
    *   `scikit-learn`
    *   `pyarrow` (para leer/escribir archivos Parquet)
    Instala estas dependencias usando:
    ```bash
    pip install -r feature_pipeline/requirements.txt
    ```
4.  Ejecuta el Jupyter Notebook `feature_pipeline.ipynb`.
    ```bash
    jupyter notebook feature_pipeline/feature_pipeline.ipynb
    ```
    o
    ```bash
    jupyter lab feature_pipeline/feature_pipeline.ipynb
    ```
5.  El notebook intentará descargar `bank-full.csv` a una carpeta `feature_pipeline/data/` si no existe. Si la descarga automática falla, deberás colocar manualmente `bank-full.csv` en esa ubicación.
6.  Tras la ejecución exitosa, el archivo `processed_bank_data.parquet` se encontrará en `feature_pipeline/data/`.

## Automatización

La intención es que este pipeline de características se ejecute de forma automatizada (por ejemplo, diariamente o según la frecuencia de actualización de los datos fuente) utilizando herramientas de orquestación como GitHub Actions. Esto aseguraría que las características estén siempre actualizadas y listas para el reentrenamiento del modelo o para inferencias batch.Okay, I will now provide the content for the Training Pipeline `README.md`.
