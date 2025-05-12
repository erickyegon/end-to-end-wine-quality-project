from mlProject.config.configuration import ConfigurationManager  # Added missing import
from mlProject.entity.config_entity import DataIngestionConfig
from mlProject.components.data_ingestion import DataIngestion
from mlProject import logger
import os

STAGE_NAME = "Data Ingestion stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        try:
            logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(data_ingestion_config)
            # Use the integrated method instead of calling individual methods
            data_ingestion.initiate_data_ingestion()
            logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
        except Exception as e:
            logger.exception(e)
            raise e

if __name__ == "__main__":
    try:
        pipeline = DataIngestionTrainingPipeline()
        pipeline.main()
    except Exception as e:
        logger.exception(e)
        raise e