from NLP_regression import logger
from NLP_regression.config.configuration import ConfigurationManager
from NLP_regression.components.data_ingestion import DataIngestion

class DataIngestionPipeline:
    def __init__(self):
        self.config = ConfigurationManager()

    def main(self):
        data_ingestion_config = self.config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_data()

if __name__ == "__main__":
    data_ingestion_pipeline = DataIngestionPipeline()
    data_ingestion_pipeline.main()