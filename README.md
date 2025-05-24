# Proyecto: Servicio de Predicción Batch para el ROI de Campañas de Marketing Bancario

## Objetivo del Proyecto

El objetivo general de este proyecto es desarrollar un servicio de predicción batch para estimar el Retorno de la Inversión (ROI) de campañas de marketing bancario. Esto se logra mediante la aplicación de un modelo de Deep Learning para predecir la probabilidad de suscripción de clientes a un depósito a plazo, utilizando herramientas MLOps para la gestión y automatización del ciclo de vida del modelo. El proyecto se basa en el conocido dataset "Bank Marketing" de UCI.

## Descripción del Dataset

Utilizamos el dataset **"Bank Marketing"**, obtenido del [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/bank+marketing). Específicamente, trabajamos con el archivo `bank-full.csv`, que contiene información sobre campañas de marketing directo de una institución bancaria portuguesa. El objetivo original de predicción del dataset es si un cliente se suscribirá (`yes`) o no (`no`) a un depósito a plazo.

En este proyecto, el **Retorno de la Inversión (ROI)** se define como un proxy calculado a partir de:
1.  La **probabilidad de suscripción** del cliente (predicha por nuestro modelo).
2.  Un **ingreso asumido** por cada suscripción exitosa (ej. $100 MXN).
3.  Un **costo asumido** por cada contacto realizado durante la campaña (ej. $1 MXN por contacto, obtenido de la columna `campaign` del dataset).

La fórmula proxy es: `ROI_campaña = (Ingreso_Total_Predicho - Costo_Total_Campaña) / Costo_Total_Campaña`.

## Estructura del Proyecto

El proyecto se organiza en los siguientes componentes principales:

1.  **`eda/` (Análisis Exploratorio de Datos):**
    *   Contiene un Jupyter Notebook (`eda.ipynb`) para explorar y visualizar el dataset, identificar patrones, entender la distribución de las variables y extraer insights iniciales.
2.  **`feature_pipeline/` (Pipeline de Características):**
    *   Un Jupyter Notebook (`feature_pipeline.ipynb`) que toma los datos crudos, realiza la limpieza, preprocesamiento (escalado de numéricas, codificación one-hot de categóricas) y la ingeniería de características necesaria.
    *   Guarda las características procesadas en un formato eficiente (ej. Parquet) para ser consumidas por el pipeline de entrenamiento.
3.  **`training_pipeline/` (Pipeline de Entrenamiento del Modelo):**
    *   Un Jupyter Notebook (`training_pipeline.ipynb`) que carga las características procesadas, entrena un modelo de Deep Learning (red neuronal densa con Keras/TensorFlow) para predecir la suscripción.
    *   Utiliza MLflow para el seguimiento de experimentos, registro de parámetros, métricas y el modelo entrenado.
4.  **`batch_inference_pipeline/` (Pipeline de Inferencia Batch):**
    *   Un Jupyter Notebook (`batch_inference_pipeline.ipynb`) que carga el modelo entrenado más reciente desde MLflow, toma un batch de datos de clientes (simulado a partir de los datos procesados), genera predicciones de suscripción y calcula el ROI estimado para la campaña sobre ese batch.
    *   Guarda los resultados de la inferencia.
5.  **`app/` (Aplicación de Demostración):**
    *   Una aplicación interactiva desarrollada con Chainlit (`app.py`) que permite ingresar manualmente los datos de un cliente, obtener una predicción de suscripción y un ROI estimado para ese perfil.
    *   Se empaqueta con Docker para facilitar su despliegue.

## Tecnologías Clave

*   **Lenguaje de Programación:** Python
*   **Análisis y Manipulación de Datos:** Pandas, NumPy
*   **Machine Learning (Preprocesamiento y Modelo):** Scikit-learn, TensorFlow/Keras
*   **MLOps y Gestión del Ciclo de Vida:**
    *   **Seguimiento de Experimentos:** MLflow
    *   **Automatización (Conceptual):** GitHub Actions (para orquestar los pipelines)
    *   **Feature Store / Model Registry (Conceptual):** Se discute el uso de MLflow para el registro de modelos; un Feature Store completo se considera como una extensión.
*   **Aplicación Interactiva:** Chainlit
*   **Contenerización:** Docker

## Resumen de Decisiones de Modelado

*   **Modelo de Suscripción:** Se optó por un modelo de Deep Learning (Red Neuronal Densa - DNN) implementado con Keras/TensorFlow para capturar relaciones no lineales complejas en los datos y predecir la probabilidad de suscripción.
*   **Métricas de Evaluación:**
    *   Para el modelo de suscripción: Área Bajo la Curva ROC (AUC) y Exactitud (Accuracy) son las métricas principales, adecuadas para problemas de clasificación binaria (especialmente con clases desbalanceadas como en este caso para AUC).
    *   Para la campaña: El ROI calculado (basado en la proxy definida) es la métrica de negocio clave.
*   **Herramientas MLOps:**
    *   **MLflow:** Se utiliza para el seguimiento de experimentos durante el entrenamiento, el versionado de modelos y el registro de métricas y parámetros.
    *   **GitHub Actions (Conceptual):** Se propone para la automatización y ejecución programada de los pipelines (feature, training, batch inference).
    *   **Feature Store / Model Registry (Conceptual):** Aunque no se implementa un Feature Store dedicado, el `feature_pipeline` produce un conjunto de datos procesados listos para el consumo. MLflow actúa como un registro de modelos básico.

## Instrucciones Generales de Configuración

1.  **Python:** Asegúrate de tener Python 3.9 o superior instalado.
2.  **Dependencias:** Cada subdirectorio principal (`eda`, `feature_pipeline`, `training_pipeline`, `batch_inference_pipeline`, `app`) contendrá (o debería contener) un archivo `requirements.txt` con sus dependencias específicas. Puedes instalarlas usando `pip install -r requirements.txt` dentro de cada directorio.
3.  **Ejecución de Pipelines:**
    *   Los pipelines de Jupyter Notebook (`.ipynb`) se ejecutan secuencialmente: `eda.ipynb` -> `feature_pipeline.ipynb` -> `training_pipeline.ipynb` -> `batch_inference_pipeline.ipynb`.
    *   Cada pipeline depende de los artefactos generados por el anterior (ej. datos procesados, modelo entrenado).
    *   La aplicación Chainlit (`app/app.py`) se ejecuta después de que el pipeline de entrenamiento haya generado un modelo y el pipeline de características un preprocesador, los cuales deben ser copiados a la carpeta `app/`.
    *   Se requiere una instancia de MLflow (local o remota) para los pipelines de entrenamiento e inferencia.
4.  **Aplicación Dockerizada:** La aplicación Chainlit se puede construir y ejecutar usando Docker con el `Dockerfile` proporcionado en el directorio `app/`.

## Resultados Principales (Esperados)

Este proyecto tiene como objetivo entregar:
*   Pipelines funcionales y automatizables (conceptualmente mediante GitHub Actions) para:
    *   El preprocesamiento y la creación de características.
    *   El entrenamiento y versionado de modelos de predicción de suscripción.
    *   La inferencia batch para la predicción de probabilidad de suscripción y el cálculo del ROI de campañas.
*   Una aplicación de demostración interactiva (Chainlit) para explorar el comportamiento del modelo con perfiles de clientes individuales.
*   Un ejemplo práctico del uso de herramientas MLOps (MLflow, Docker) en un contexto de predicción de marketing.Okay, I will now provide the content for the EDA `README.md`.
