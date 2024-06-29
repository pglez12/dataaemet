# ETL Aemet data
## Altostratus Data – Reto

### Descripción del Proyecto

Este proyecto implementa una arquitectura para ejecutar un proceso de extracción, carga y transformación (ELT) desde la API de AEMET (Agencia Estatal de Meteorología de España). La arquitectura está diseñada para extraer datos climatológicos diarios de todas las estaciones meteorológicas para un día determinado y procesarlos para su visualización en un dashboard en Looker Studio.

### Arquitectura

1. **Launcher:** Se ejecuta cada día a las 01:00 y inicia el Orchestrator.
2. **Orchestrator:** Inicia el Connector y, una vez que los datos se han cargado correctamente, inicia el Transformer en Dataform.
3. **Connector:** Extrae los datos de la API de AEMET y los carga en el dataset de Staging en BigQuery. Este proceso es idempotente y self-healing.
4. **Transformer:** Procesa los datos desde el dataset de Staging hasta el dataset de Reporting, dejando resultados intermedios en el dataset de Processing.
5. **Dashboard:** Los datos procesados se visualizan en un dashboard en Looker Studio con un mapa del tiempo, incluyendo temperaturas, presiones, etc.

### Endpoints

- `/api/valores/climatologicos/diarios/datos/fechaini/{fechaIniStr}/fechafin/{fechaFinStr}/todasestaciones`: Permite obtener los datos climatológicos diarios de todas las estaciones para un período determinado.

### Requisitos

1. **Connector idempotente:** No genera datos duplicados al invocarse varias veces en el mismo día.
2. **Connector self-healing:** Si la API de AEMET queda indisponible, automáticamente restablece la carga de los datos pendientes.
3. **Orchestrator:** Inicia el Transformer solo si se han cargado los datos satisfactoriamente.
4. **Transformer:** Usa vistas para los resultados intermedios y tablas para los datos en la zona de Reporting.
5. **Dashboard:** Incluye un mapa del tiempo con presiones, temperaturas, etc., y al menos un filtro de fecha y otro de localizaciones.

### Fecha de Entrega

Antes del 1 de julio de 2024.

### Modo de Entrega

Proveer acceso de lectura a `data.team@altostratus.es` a:

1. Repositorio de GitHub con el código, documentación y enlaces al cloud y dashboard.
2. Proyecto de Google Cloud/AWS.
3. Dashboard.

## Estructura del Proyecto

```text
- service/
  - main.py
  - connector.py
  - locations.py
  - sink.py
  - source.py
  - config.py
  - config.yaml
  - models.py
```

Archivos Principales
main.py
El archivo principal que configura y ejecuta la aplicación FastAPI. Contiene los endpoints para las cargas incrementales, backfill y actualización de ubicaciones.

connector.py
Implementa la lógica del Connector, responsable de la extracción y carga de datos desde la API de AEMET a BigQuery. Incluye métodos para cargas incrementales y backfill.

locations.py
Contiene la lógica para actualizar la información de las estaciones meteorológicas desde la API de AEMET y guardarla en BigQuery.

sink.py
Define la clase BigQuerySink que maneja la carga de datos en BigQuery y la recuperación de la última fecha de actualización.

source.py
Define la clase AEMETSource que maneja la extracción de datos desde la API de AEMET.

config.py
Carga y maneja la configuración del proyecto desde un archivo YAML.

config.yaml
Archivo de configuración que contiene las claves de la API, IDs del proyecto y detalles de la configuración del origen y el destino de los datos.

models.py
Define los modelos de datos utilizando Pydantic para la validación de entradas en los endpoints.

Cómo Ejecutar el Proyecto
Prerrequisitos
Python 3.8 o superior
Google Cloud SDK configurado
Claves de la API de AEMET
Instalación
Clonar el repositorio:
bash
Copiar código
git clone https://github.com/usuario/repo.git
cd repo
Crear y activar un entorno virtual:
bash
Copiar código
python -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
Instalar las dependencias:
bash
Copiar código
pip install -r requirements.txt
Configurar las variables de entorno en .env (si es necesario).
Ejecución
Ejecutar la aplicación:

bash
Copiar código
uvicorn main:app --reload
Pruebas
Realizar pruebas utilizando curl o cualquier herramienta de cliente HTTP:

bash
Copiar código
curl -X GET "http://localhost:8000/incremental_load"
Dashboard
Accede al dashboard en Looker Studio utilizando el enlace proporcionado en el repositorio.


```
altostratus-data-project/
│
├── cloud-run/
│   ├── main.py                # Configuración y ejecución de la aplicación FastAPI
│   ├── connector.py           # Definición de la clase Connector
│   ├── locations.py           # Funciones para gestionar las estaciones meteorológicas
│   ├── sink.py                # Definición de la clase BigQuerySink
│   ├── source.py              # Definición de la clase AEMETSource
│   └── config.yaml            # Configuración de la aplicación (API y BigQuery)
│
├── dataform/
│   └── dataform.sql           # SQL scripts para crear y transformar tablas y vistas en BigQuery
│
└── README.md                  # Documentación del proyecto
```
´´´
