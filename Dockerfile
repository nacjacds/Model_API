# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Actualiza pip y setuptools
RUN python -m pip install --upgrade pip setuptools

# Copia los archivos requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos los archivos necesarios al contenedor
COPY . /app

# Copia los archivos de la carpeta data al contenedor
COPY data /app/data

# Expone el puerto en el que correrá la API
EXPOSE 8000

# Comando para correr la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]