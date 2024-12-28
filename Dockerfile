# Usar una imagen base de Python 3.11.9
FROM python:3.11.9-slim

# Actualizar el sistema e instalar dependencias esenciales
RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake \
    build-essential \
    libatlas-base-dev \
    libboost-all-dev \
    git \
    bash \
    gcc \
    g++ \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Crear un directorio de trabajo
WORKDIR /appPy

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt /appPy/

# Instalar las dependencias de Python, incluyendo Gunicorn
RUN pip3 install --no-cache-dir -r requirements.txt gunicorn

# Copiar todo el código de la aplicación al contenedor
COPY . /appPy

# Configurar la variable de entorno para el PYTHONPATH
ENV PYTHONPATH=/appPy

# Exponer el puerto 5000 (por si es necesario más adelante)
EXPOSE 5000

# Usar Gunicorn para ejecutar la aplicación Flask
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app.main:app"]
