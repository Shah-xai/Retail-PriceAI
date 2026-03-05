from NLP_regression.constants import *
from NLP_regression.utils.common import read_yaml, create_directories
from NLP_regression import logger
from pathlib import Path
from NLP_regression.entity.config_entity import DataIngestionConfig

class ConfigurationManager:
    def __init__(self, config_file_path: Path = CONFIG_FILE_PATH,
                  params_file_path: Path = PARAMS_FILE_PATH):
        self.config = read_yaml(config_file_path)
        self.params = read_yaml(params_file_path)
        create_directories([self.config.artificats_root])
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:

        config = self.config.data_ingestion
        create_directories([config.root_dir])
        data_ingestion_config = DataIngestionConfig(
            root_dir=Path(config.root_dir),
            source_URL=config.source_URL,
        )
        logger.info(f"Data Ingestion Config: {data_ingestion_config}")
        return data_ingestion_config
