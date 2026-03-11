from NLP_regression import logger
from NLP_regression.config.configuration import ConfigurationManager
from NLP_regression.components.data_transformation import DataTransformation

class DataTransformationPipeline:
    def __init__(self):
        self.config = ConfigurationManager()

    def main(self):
        data_transformation_config = self.config.get_data_transformation_config()
        data_transformation = DataTransformation()
        data_transformation.initiate_data_transformation(data_transformation_config)
if __name__ == "__main__":
    data_transformation_pipeline = DataTransformationPipeline()
    data_transformation_pipeline.main()