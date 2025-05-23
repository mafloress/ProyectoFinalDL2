# Análisis Exploratorio de Datos (EDA) del Dataset Bank Marketing

## Objetivo del Componente

Este componente del proyecto se centra en realizar un Análisis Exploratorio de Datos (EDA) exhaustivo sobre el dataset "Bank Marketing" (específicamente, el archivo `bank-full.csv`). El propósito principal es comprender a fondo la estructura y características de los datos, identificar patrones, anomalías, correlaciones y obtener insights clave que informarán el diseño y las decisiones tomadas en los pipelines subsecuentes, especialmente en el `feature_pipeline`.

## Contenido del Notebook (`eda.ipynb`)

El análisis se lleva a cabo en el Jupyter Notebook `eda.ipynb` y está estructurado en las siguientes secciones principales:

1.  **Introducción y Estrategia Proxy de ROI:**
    *   Breve descripción del EDA y cómo se define el ROI proxy para el proyecto.
2.  **Carga y Exploración Inicial de los Datos:**
    *   Importación de librerías necesarias.
    *   Carga del dataset `bank-full.csv`.
    *   Inspección inicial con `.head()`, `.info()`, `.describe(include='all')`, `.isnull().sum()`, y `.shape`.
3.  **Análisis de la Variable Objetivo (`y`):**
    *   Estudio de la distribución de la variable `y` (suscripción a depósito a plazo).
    *   Visualización del desbalance de clases.
4.  **Análisis Univariado:**
    *   **Variables Numéricas:** Histogramas y box plots para cada variable numérica (ej. `age`, `balance`, `duration`) para entender su distribución, tendencia central, dispersión y presencia de outliers.
    *   **Variables Categóricas:** Gráficos de barras para cada variable categórica (ej. `job`, `marital`, `education`) para observar la frecuencia de cada categoría.
5.  **Análisis Bivariado (Relación con la Variable Objetivo `y`):**
    *   **Variables Numéricas vs. `y`:** Box plots comparativos para analizar cómo la distribución de cada variable numérica difiere entre las clases de la variable objetivo.
    *   **Variables Categóricas vs. `y`:** Gráficos de barras agrupados/apilados para visualizar la proporción de suscripciones (`yes`/`no`) dentro de cada categoría de las variables predictoras.
6.  **Análisis de Correlación (Variables Numéricas):**
    *   Cálculo y visualización de una matriz de correlación (heatmap) entre las variables numéricas para identificar posibles relaciones lineales.
7.  **Detección de Valores Atípicos (Outliers):**
    *   Resumen de las variables que presentan una cantidad significativa de outliers, basado en los box plots del análisis univariado.
8.  **Resumen de Hallazgos Clave del EDA:**
    *   Consolidación de los insights más importantes, tendencias observadas, características prometedoras para la predicción y posibles problemas de calidad de datos o transformaciones necesarias.

## Hallazgos Clave

El EDA reveló varios aspectos cruciales que influyeron en las etapas posteriores del proyecto:

*   **Desbalance de Clases:** La variable objetivo `y` está significativamente desbalanceada (la mayoría de los clientes no se suscriben). Esto sugiere la necesidad de usar métricas de evaluación adecuadas (como AUC) y considerar técnicas de manejo de desbalance si el modelo tiene bajo rendimiento en la clase minoritaria.
*   **Importancia de `duration`:** La duración del último contacto (`duration`) mostró ser un predictor muy fuerte. Sin embargo, se reconoció que este valor no se conoce *antes* de realizar la llamada, lo que limita su uso directo en un modelo que predice *a quién contactar*. Se decidió mantenerla pero con esta advertencia.
*   **Relevancia de Campañas Previas y Meses:** Variables como `poutcome` (resultado de la campaña previa) y `month` (mes del contacto) mostraron una fuerte relación con la tasa de suscripción, indicando la importancia del historial del cliente y el *timing* de la campaña.
*   **Manejo de Valores 'Unknown':** Varias columnas categóricas (`job`, `education`, `contact`, `poutcome`) contienen valores 'unknown'. Se decidió que `OneHotEncoder` trataría estos como una categoría separada, o se podrían aplicar estrategias de imputación si fuera necesario (aunque para este proyecto, se optó por la primera).
*   **Necesidad de Escalado:** Las variables numéricas como `balance`, `age`, `duration` tienen rangos y distribuciones muy diferentes. Esto confirmó la necesidad de aplicar escalado (ej. `StandardScaler`) como parte del preprocesamiento para que los modelos basados en gradientes (como las redes neuronales) converjan adecuadamente.
*   **Outliers:** Variables como `balance` y `campaign` presentan outliers significativos. Se consideró que las transformaciones (como logarítmica para `balance`, aunque no implementada explícitamente en el pipeline final por simplicidad) o el uso de modelos robustos podrían ser beneficiosos. El escalado estándar ayuda a mitigar parcialmente su impacto.
*   **Características Prometedoras:** Además de las mencionadas, `contact`, `loan`, `housing`, `job`, y `education` también mostraron ser informativas.

Estos hallazgos fueron fundamentales para definir qué características incluir, cómo preprocesarlas (escalado, codificación one-hot) y qué aspectos considerar durante la modelización en el `feature_pipeline.ipynb` y `training_pipeline.ipynb`.

## Instrucciones de Ejecución

El análisis exploratorio se encuentra en el Jupyter Notebook `eda.ipynb`. Para ejecutarlo:

1.  Asegúrate de tener un entorno de Python (preferiblemente Python 3.9 o superior).
2.  Clona el repositorio o descarga el contenido del directorio `eda/`.
3.  (Conceptual) Debería existir un archivo `requirements.txt` dentro del directorio `eda/` listando las dependencias específicas para este notebook (principalmente `pandas`, `numpy`, `matplotlib`, `seaborn`, `jupyter`). Instala estas dependencias usando:
    ```bash
    pip install -r eda/requirements.txt
    ```
4.  Inicia Jupyter Notebook o JupyterLab:
    ```bash
    jupyter notebook eda/eda.ipynb
    ```
    o
    ```bash
    jupyter lab eda/eda.ipynb
    ```
5.  Ejecuta las celdas del notebook en orden. El notebook está diseñado para descargar los datos si no los encuentra localmente.

**Nota:** Este README asume que los archivos `requirements.txt` son gestionados individualmente por componente, lo cual es una buena práctica para modularidad. Si existe un `requirements.txt` global, las instrucciones de instalación de dependencias podrían variar.The content for both `main_project_readme.md` and `eda_readme.md` has been generated in Mexican Spanish as requested.

**`main_project_readme.md` includes:**
*   Objetivo del Proyecto
*   Descripción del Dataset (including ROI proxy definition)
*   Estructura del Proyecto (listing all components and their roles)
*   Tecnologías Clave
*   Resumen de Decisiones de Modelado
*   Instrucciones Generales de Configuración
*   Resultados Principales (Esperados)

**`eda_readme.md` includes:**
*   Objetivo del Componente
*   Contenido del Notebook (`eda.ipynb`) detailing its sections
*   Hallazgos Clave from the EDA and their impact
*   Instrucciones de Ejecución for the EDA notebook

Both files are ready.
