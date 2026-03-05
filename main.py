from NLP_regression import logger
from NLP_regression.pipeline.data_ingestion_pipeline import DataIngestionPipeline

logger.info("Starting the data ingestion process...")
data_ingestion_pipeline = DataIngestionPipeline()  
data_ingestion_pipeline.main()
logger.info("Data ingestion process completed successfully.")
