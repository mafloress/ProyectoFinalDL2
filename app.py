import chainlit as cl
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import os

# --- Configuración de Rutas y Parámetros ---
MODEL_PATH = 'trained_model.keras'
PREPROCESSOR_PATH = 'preprocessor.joblib'

# Parámetros para el cálculo de ROI (deben coincidir con los usados en los pipelines)
R_SUB = 100  # Ingreso por suscripción (MXN)
C_CONTACT = 1 # Costo por contacto (MXN)
DEFAULT_CAMPAIGN_CONTACTS = 1 # Número de contactos asumido para un cliente individual en esta simulación

# Definir las columnas esperadas por el preprocesador en el orden correcto
# Esto debe coincidir EXACTAMENTE con cómo se entrenó el ColumnTransformer
EXPECTED_NUMERICAL_COLS = ['age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous']
EXPECTED_CATEGORICAL_COLS = ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'poutcome']
ALL_EXPECTED_COLS = EXPECTED_NUMERICAL_COLS + EXPECTED_CATEGORICAL_COLS

# Valores por defecto para las columnas que no se piden en la UI
# Estos son cruciales si la UI no pide todas las columnas que el preprocesador espera.
# Los valores deben ser razonables y del tipo de dato correcto.
# Para categóricas, deben ser categorías conocidas por el OneHotEncoder o se manejarán por handle_unknown='ignore'
DEFAULT_VALUES = {
    'day': 15, # Día del mes (numérico)
    'campaign': 1, # Número de contactos en esta campaña (numérico)
    'pdays': -1, # Días desde el último contacto previo (-1 si no contactado) (numérico)
    'previous': 0, # Número de contactos previos (numérico)
    'default': 'no', # ¿Tiene crédito en default? (categórico)
    'contact': 'unknown', # Tipo de contacto (categórico)
    'month': 'may', # Mes del último contacto (categórico)
    'poutcome': 'unknown' # Resultado de la campaña previa (categórico)
}

# Listas de opciones para los campos de entrada categóricos (basado en bank-full.csv)
JOB_OPTIONS = ["admin.", "blue-collar", "entrepreneur", "housemaid", "management", "retired", "self-employed", "services", "student", "technician", "unemployed", "unknown"]
MARITAL_OPTIONS = ["divorced", "married", "single"]
EDUCATION_OPTIONS = ["primary", "secondary", "tertiary", "unknown"]
HOUSING_OPTIONS = ["no", "yes"]
LOAN_OPTIONS = ["no", "yes"]

# --- Carga de Modelo y Preprocesador ---
model = None
preprocessor = None

@cl.on_chat_start
async def on_chat_start():
    global model, preprocessor
    loading_message = await cl.Message(content="Iniciando la aplicación de predicción de suscripción...\nCargando modelo y preprocesador...", author="Sistema").send()

    if not os.path.exists(MODEL_PATH):
        await cl.Message(content=f"Error crítico: El archivo del modelo '{MODEL_PATH}' no se encontró. La aplicación no puede funcionar.", author="Sistema").send()
        return
    if not os.path.exists(PREPROCESSOR_PATH):
        await cl.Message(content=f"Error crítico: El archivo del preprocesador '{PREPROCESSOR_PATH}' no se encontró. La aplicación no puede funcionar.", author="Sistema").send()
        return

    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        preprocessor = joblib.load(PREPROCESSOR_PATH)
        await loading_message.update(content="¡Modelo y preprocesador cargados exitosamente! \n\n**Parámetros para cálculo de ROI:**\n- Ingreso por suscripción (R_sub): ${R_SUB} MXN\n- Costo por contacto (C_contact): ${C_CONTACT} MXN (asumiendo {DEFAULT_CAMPAIGN_CONTACTS} contacto(s) para esta simulación individual).\n\nPor favor, ingresa los datos del cliente para la predicción.", author="Sistema")
        
        # Solicitar datos al usuario
        await request_user_input()

    except Exception as e:
        await loading_message.update(content=f"Error al cargar componentes: {str(e)}", author="Sistema")
        model = None
        preprocessor = None

async def request_user_input():
    """Solicita al usuario los datos necesarios para la predicción."""
    settings = await cl.ChatSettings(
        [
            cl.input_widget.NumberInput(id="age", label="Edad del Cliente", initial_value=30),
            cl.input_widget.Select(id="job", label="Trabajo", initial_value="management", values=JOB_OPTIONS),
            cl.input_widget.Select(id="marital", label="Estado Civil", initial_value="married", values=MARITAL_OPTIONS),
            cl.input_widget.Select(id="education", label="Nivel Educativo", initial_value="tertiary", values=EDUCATION_OPTIONS),
            cl.input_widget.NumberInput(id="balance", label="Saldo Promedio Anual (euros)", initial_value=1500),
            cl.input_widget.Select(id="housing", label="¿Tiene Préstamo Hipotecario?", initial_value="yes", values=HOUSING_OPTIONS),
            cl.input_widget.Select(id="loan", label="¿Tiene Préstamo Personal?", initial_value="no", values=LOAN_OPTIONS),
            cl.input_widget.NumberInput(id="duration", label="Duración del Último Contacto (segundos)", initial_value=180)
        ]
    ).send()
    await process_input(settings)


@cl.on_settings_update
async def on_settings_update(settings: dict):
    """Se llama cuando el usuario actualiza los settings (inputs)."""
    await cl.Message(content="Procesando nuevos datos...", author="Sistema", indent=1).send()
    await process_input(settings)

async def process_input(user_input: dict):
    global model, preprocessor
    if not model or not preprocessor:
        await cl.Message(content="El modelo o el preprocesador no están disponibles. No se puede predecir.", author="Sistema").send()
        return

    try:
        # Crear DataFrame con los datos del usuario y los valores por defecto
        data = {}
        # Llenar con datos de la UI
        for key, value in user_input.items():
            data[key] = value
        
        # Llenar con valores por defecto para las columnas no presentes en la UI
        for col, default_val in DEFAULT_VALUES.items():
            if col not in data:
                data[col] = default_val
        
        # Asegurar que el DataFrame tenga todas las columnas en el orden esperado
        # Crear un diccionario vacío para el DataFrame con todas las columnas esperadas
        ordered_data_dict = {col: [data.get(col)] for col in ALL_EXPECTED_COLS}


        # Convertir a DataFrame
        input_df = pd.DataFrame(ordered_data_dict)
        
        # Verificar tipos de datos (especialmente numéricos)
        for col in EXPECTED_NUMERICAL_COLS:
            input_df[col] = pd.to_numeric(input_df[col], errors='coerce')
        
        # Si algún numérico falla la conversión, podría ser un problema
        if input_df[EXPECTED_NUMERICAL_COLS].isnull().any().any():
            await cl.Message(content="Error: Algún valor numérico no es válido.", author="Sistema").send()
            return

        await cl.Message(
            content=f"**DataFrame creado para preprocesamiento (primeras filas):**\n```json\n{input_df.to_json(orient='records', indent=2)}\n```",
            author="Debug" # Mensaje de depuración
        ).send()

        # Preprocesar los datos
        # El preprocesador espera un DataFrame con las columnas en el orden original
        processed_input_array = preprocessor.transform(input_df)
        
        # await cl.Message(content=f"Forma del array preprocesado: {processed_input_array.shape}", author="Debug").send()


        # Realizar predicción
        prediction_proba = model.predict(processed_input_array)[0][0] # Obtener la probabilidad

        # Calcular ROI simplificado para este perfil
        ingreso_esperado = prediction_proba * R_SUB
        costo_estimado = DEFAULT_CAMPAIGN_CONTACTS * C_CONTACT
        roi_estimado = 0
        if costo_estimado > 0:
            roi_estimado = (ingreso_esperado - costo_estimado) / costo_estimado
        else: # Evitar división por cero si el costo es 0
             roi_estimado = ingreso_esperado / 1 # Asumir que si no hay costo, el ROI es el ingreso mismo (o infinito si es positivo)


        # Mostrar resultados
        resultado_msg = f"""---
**Resultado de la Predicción:**

*   **Probabilidad de Suscripción:** `{prediction_proba:.2%}`
*   **Ingreso Esperado (si se suscribe):** `${R_SUB:.2f} MXN`
*   **Costo Estimado del Contacto:** `${costo_estimado:.2f} MXN` (basado en {DEFAULT_CAMPAIGN_CONTACTS} contacto(s))
*   **ROI Estimado para este Perfil:** `{roi_estimado:.2%}`

---
**Nota:** Esta es una simulación basada en los datos proporcionados y los parámetros de ROI fijos.
Un 'duration' (duración del último contacto) alto tiende a incrementar la probabilidad de suscripción, pero este valor solo se conoce después de la llamada.
"""
        await cl.Message(content=resultado_msg, author="Predicción").send()

    except Exception as e:
        error_msg = f"Error durante la predicción: {str(e)}\n"
        error_msg += "Asegúrate de que los valores ingresados sean correctos y que el preprocesador esté alineado con los datos de entrada."
        await cl.Message(content=error_msg, author="Sistema").send()

if __name__ == "__main__":
    # Esta parte es para correr Chainlit desde la línea de comandos
    # chainlit run app.py -w
    pass
