# ETL Aemet data

## Altostratus Data – Reto
### Descripción del Proyecto
![image](https://github.com/pglez12/dataaemet/assets/135646732/d588c54a-5ae3-4e70-8ed0-5e66715cabf4)

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

### Modo de Entrega

Proveer acceso de lectura a `data.team@altostratus.es` a:

1. Repositorio de GitHub con el código, documentación y enlaces al cloud y dashboard.
2. Proyecto de Google Cloud/AWS.
3. Dashboard.

## Estructura del Proyecto
```
dataaemet/
│
├── orchestrator/
│   └── workflow.yaml          # Workflow file for orchestrating tasks with Cloud Run (if needed)
│
├── connector/
│   ├── main.py                # Configuration and execution of FastAPI application
│   ├── connector.py           # Definition of Connector class
│   ├── locations.py           # Functions for managing weather stations
│   ├── sink.py                # Definition of BigQuerySink class
│   ├── source.py              # Definition of AEMETSource class
│   ├── config.py              # Definition of Config class and get_config function
│   ├── models.py              # Definition of Pydantic models for data validation
│   ├── config.yaml            # Configuration for the application (API and BigQuery)
│   ├── Dockerfile             # Definition of Docker container
│   └── requirements.txt       # Project dependencies
│
├── transformer/
│   ├── definitions/           # Directory for Dataform definitions
│   │   ├── data_staging.sqlx  # SQL for data processing view
│   │   └── process_weather_data.sqlx  # SQL for weather report table
│   ├── workflow_settings.yaml # Project and dataset configuration in Dataform
│   └── README.md              # Specific documentation for Dataform (if needed)
│
└── README.md                  # Main project documentation
```
