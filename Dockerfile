# Usar una imagen base de Python ligera
# Esta imagen es una buena opción para aplicaciones Python porque es relativamente pequeña
# y viene con Python y pip preinstalados. Python 3.9 es una versión estable.
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
# Todos los comandos subsiguientes se ejecutarán desde este directorio.
WORKDIR /app

# Copiar el archivo de requisitos de la aplicación al directorio de trabajo
# Este archivo (application_requirements.txt) listará todas las dependencias de Python
# que necesita nuestra aplicación Chainlit.
COPY application_requirements.txt .

# Instalar las dependencias de Python
# -r especifica que se lean los paquetes desde el archivo proporcionado.
# --no-cache-dir se usa para reducir el tamaño de la imagen, ya que no guarda el caché de descarga.
RUN pip install --no-cache-dir -r application_requirements.txt

# Copiar los archivos de la aplicación al directorio de trabajo
# Esto incluye el script principal de Chainlit (app.py), el modelo entrenado
# (asumimos 'trained_model.keras') y el preprocesador guardado (asumimos 'preprocessor.joblib').
# También podría incluir cualquier otro archivo estático o de configuración necesario.
COPY app.py .
COPY trained_model.keras .
COPY preprocessor.joblib .
# Si tuvieras una carpeta de 'assets' o 'static', la copiarías también:
# COPY assets/ ./assets/

# Exponer el puerto en el que Chainlit se ejecuta por defecto
# Chainlit utiliza el puerto 8000. Esto informa a Docker que la aplicación
# dentro del contenedor estará escuchando en este puerto.
EXPOSE 8000

# Comando para ejecutar la aplicación Chainlit cuando se inicie el contenedor
# "chainlit", "run", "app.py" son los comandos estándar para iniciar una app Chainlit.
# "-w" (o --watch) activa el modo de auto-recarga, útil durante el desarrollo.
# Para un entorno de "producción" más estable, se podría remover el "-w".
# "--host=0.0.0.0" es importante para que la app sea accesible desde fuera del contenedor.
CMD ["chainlit", "run", "app.py", "--host=0.0.0.0", "-w"]
