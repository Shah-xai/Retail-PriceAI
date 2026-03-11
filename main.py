from NLP_regression import logger
from NLP_regression.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from NLP_regression.pipeline.data_transformation_pipeline import DataTransformationPipeline

logger.info("Starting the data ingestion process...")
data_ingestion_pipeline = DataIngestionPipeline()  
data_ingestion_pipeline.main()
logger.info("Data ingestion process completed successfully.")

logger.info("Starting the data transformation process...")
data_transformation_pipeline = DataTransformationPipeline()
data_transformation_pipeline.main()
logger.info("Data transformation process completed successfully.")

