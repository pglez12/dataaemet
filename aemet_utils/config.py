import pydantic
from pyaml_env import parse_config

from aemet_utils.connector import ConnectorConfig
from aemet_utils.sink import DummySinkConfig
from aemet_utils.source import DummySourceConfig

class Config(pydantic.BaseModel):
    source: DummySourceConfig
    sink: DummySinkConfig
    connector: ConnectorConfig
    orchestrator: dict
    dataform: dict

def get_config(config_path: str = "config.yaml") -> Config:
    config = parse_config(config_path)
    return Config(**config)
