# Usar una imagen base de Python
FROM python:3.8

# Copiar los archivos de la aplicación al directorio /app
COPY . /app

# Instalar las dependencias de la aplicación
RUN pip install -r requirements.txt

# Exponer el puerto 5000 para recibir las peticiones HTTP
EXPOSE 5000

# Ejecutar la aplicación cuando se inicie el contenedor
CMD ["python", "server.py"]