import yaml
import os

class Config:
    def __init__(self, config_file="config.yaml"):
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, "r") as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo de configuración '{self.config_file}' no se encontró.")
        except yaml.YAMLError as e:
            raise ValueError(f"Error al cargar el archivo de configuración '{self.config_file}': {e}")

    def get(self, key, default=None):
        value = self.config.get(key, default)
        if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
            return os.getenv(value[1:-1], default)
        return value

def get_config(file_path):
    return Config(file_path).config

# Ejemplo de cómo utilizar la configuración
config = Config()

# Ejemplo de cómo obtener un valor específico del archivo de configuración
AEMET_API_KEY = config.get("AEMET_API_KEY")
PROJECT_ID = config.get("PROJECT_ID", "aemet-data")
DATASET_ID = config.get("DATASET_ID", "aemet_db")
TABLE_ID = config.get("TABLE_ID", "data_stagging2")