FROM python:3.10-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de requisitos
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Instalar el cliente de BigQuery
# RUN pip install --no-cache-dir google-cloud-bigquery

# Copiar el resto de los archivos de la aplicación
COPY . .

# Set environment variables
ENV AEMET_API_KEY="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwcHR5bGxhbmFAZ21haWwuY29tIiwianRpIjoiMjJjNGNkZGQtZmQyNy00YTM3LWFlYmMtYjY3NjNiMjA4MmMzIiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE3MTgwOTMxNTksInVzZXJJZCI6IjIyYzRjZGRkLWZkMjctNGEzNy1hZWJjLWI2NzYzYjIwODJjMyIsInJvbGUiOiIifQ.dsLyBdXEMU2JoAYTjZTRyxtMje5t3iAT__9Moy7tl5g"
ENV PROJECT_ID="aemet-data"
ENV DATASET_ID="aemet_db"
ENV TABLE_ID="data_stagging2"

# Expose the port used by FastAPI
EXPOSE 8000

# Command to run the application using the environment variables
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
