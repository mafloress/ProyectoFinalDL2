# Aplicación de Demostración: Predicción de ROI para Clientes Bancarios

## 1. Objetivo del Componente

Este componente consiste en una aplicación web interactiva, desarrollada con **Chainlit**, que sirve como demostración de la funcionalidad del modelo de predicción de suscripción y el cálculo del Retorno de la Inversión (ROI) asociado. La aplicación permite a un usuario ingresar manualmente las características clave de un cliente y, a cambio, visualiza la probabilidad de que dicho cliente se suscriba a un depósito a plazo, junto con una estimación del ROI para ese perfil específico.

## 2. Descripción de la Aplicación (`app.py`)

La aplicación (`app.py`) proporciona una interfaz de usuario simple y directa para interactuar con el modelo de predicción.

*   **Tecnología:**
    *   **Chainlit:** Se utiliza para construir la interfaz de usuario basada en chat y para manejar la interacción con el usuario.
*   **Funcionalidad Principal:**
    1.  **Carga de Artefactos:** Al iniciar, la aplicación carga un modelo de Keras pre-entrenado (`trained_model.keras`) y un objeto preprocesador de Scikit-learn (`preprocessor.joblib`). Estos artefactos deben estar presentes en el mismo directorio que `app.py`.
    2.  **Entrada de Datos del Usuario:** A través de la interfaz de Chainlit, el usuario puede ingresar manualmente valores para un conjunto seleccionado de características del cliente, como edad, trabajo, estado civil, nivel educativo, saldo, si tiene préstamos, y la duración del último contacto.
    3.  **Preprocesamiento de Datos:** Los datos ingresados por el usuario se combinan con valores por defecto para las características no solicitadas en la UI, formando un DataFrame completo. Este DataFrame luego se procesa utilizando el `preprocessor.joblib` cargado, que aplica las transformaciones necesarias (escalado, codificación one-hot) para que los datos sean compatibles con el modelo.
    4.  **Generación de Predicciones:** Con los datos preprocesados, el modelo Keras (`trained_model.keras`) predice la probabilidad de que el cliente se suscriba al depósito a plazo.
    5.  **Cálculo y Visualización del ROI:** Se calcula un ROI simplificado para el perfil del cliente, utilizando la probabilidad predicha y los parámetros de ROI predefinidos. Tanto la probabilidad como el ROI estimado, junto con otros detalles relevantes, se muestran al usuario.
*   **Idioma:** Toda la interacción con el usuario, incluyendo etiquetas, mensajes y resultados, se presenta en español mexicano.

## 3. Dockerfile

Se incluye un `Dockerfile` para facilitar la creación de una imagen de contenedor para la aplicación, lo que simplifica su despliegue y asegura la consistencia del entorno.

*   **Pasos Principales del Dockerfile:**
    1.  **Imagen Base:** Utiliza `python:3.9-slim` como imagen base ligera de Python.
    2.  **Directorio de Trabajo:** Establece `/app` como el directorio de trabajo dentro del contenedor.
    3.  **Dependencias:** Copia `application_requirements.txt` y luego instala las dependencias de Python listadas en él usando `pip`.
    4.  **Copia de Archivos:** Copia los archivos esenciales de la aplicación (`app.py`, `trained_model.keras`, `preprocessor.joblib`) al directorio `/app` del contenedor.
    5.  **Exposición de Puerto:** Expone el puerto `8000`, que es el puerto por defecto en el que Chainlit ejecuta la aplicación.
    6.  **Comando de Ejecución:** Define el comando `CMD` para iniciar la aplicación Chainlit (`chainlit run app.py --host=0.0.0.0 -w`) cuando se inicie un contenedor a partir de la imagen.

## 4. Archivos Incluidos

El directorio de la aplicación (`app/`) contiene los siguientes archivos:

*   **`app.py`:** El script principal que contiene la lógica de la aplicación Chainlit.
*   **`Dockerfile`:** El archivo de configuración para construir la imagen Docker de la aplicación.
*   **`application_requirements.txt`:** Un archivo de texto que lista todas las dependencias de Python necesarias para ejecutar la aplicación.
*   **`trained_model.keras` (esperado):** El archivo del modelo de Keras entrenado. Este archivo debe ser generado por el `training_pipeline.ipynb` y colocado en este directorio.
*   **`preprocessor.joblib` (esperado):** El archivo del objeto preprocesador de Scikit-learn guardado (usualmente un `ColumnTransformer`). Este archivo debe ser generado por el `feature_pipeline.ipynb` y colocado en este directorio.

## 5. Instrucciones de Configuración y Ejecución

### A. Ejecución Local (usando la CLI de Chainlit)

1.  **Requisitos Previos:**
    *   Asegúrate de tener Python 3.9 o superior instalado.
    *   Coloca los archivos `trained_model.keras` y `preprocessor.joblib` (generados por los pipelines correspondientes) en el mismo directorio que `app.py`.
2.  **Instalar Dependencias:**
    Navega al directorio de la aplicación y ejecuta:
    ```bash
    pip install -r application_requirements.txt
    ```
3.  **Ejecutar la Aplicación:**
    En el mismo directorio, ejecuta el siguiente comando:
    ```bash
    chainlit run app.py -w
    ```
    La opción `-w` (watch) permite que la aplicación se recargue automáticamente si realizas cambios en el código.
4.  **Acceder:** Abre tu navegador web y ve a `http://localhost:8000`.

### B. Ejecución con Docker

1.  **Requisitos Previos:**
    *   Asegúrate de tener Docker instalado y en ejecución.
    *   Coloca los archivos `trained_model.keras` y `preprocessor.joblib` en el mismo directorio que el `Dockerfile` y `app.py`.
2.  **Construir la Imagen Docker:**
    Navega al directorio que contiene el `Dockerfile` y los archivos de la aplicación, y ejecuta:
    ```bash
    docker build -t bank-roi-app .
    ```
    Esto construirá una imagen Docker con el nombre `bank-roi-app`.
3.  **Ejecutar el Contenedor Docker:**
    Una vez construida la imagen, ejecuta el siguiente comando para iniciar un contenedor:
    ```bash
    docker run -p 8000:8000 bank-roi-app
    ```
    Esto mapea el puerto 8000 del contenedor al puerto 8000 de tu máquina local.
4.  **Acceder:** Abre tu navegador web y ve a `http://localhost:8000`.

## 6. Parámetros de ROI Utilizados en la Aplicación

Para el cálculo simplificado del ROI mostrado en la aplicación para un perfil de cliente individual, se utilizan los siguientes parámetros (estos deben ser consistentes con los definidos en los pipelines de inferencia):

*   **Ingreso Asumido por Suscripción (`R_SUB`):** $100 MXN.
*   **Costo Asumido por Contacto (`C_CONTACT`):** $1 MXN.
*   **Contactos Asumidos para Simulación Individual (`DEFAULT_CAMPAIGN_CONTACTS`):** 1 contacto.

Estos valores están definidos dentro de `app.py` y se utilizan para dar una estimación del ROI para el perfil específico ingresado por el usuario.
