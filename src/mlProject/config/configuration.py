from pathlib import Path
from mlProject.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
from mlProject.utils.common import read_yaml, create_directories
from mlProject.entity.config_entity import DataIngestionConfig


class ConfigurationManager:
    """
    Handles loading configuration, parameters, and schema from YAML files
    and provides component-specific configurations.
    """
    def __init__(
        self,
        config_filepath: Path = CONFIG_FILE_PATH,
        params_filepath: Path = PARAMS_FILE_PATH,
        schema_filepath: Path = SCHEMA_FILE_PATH
    ) -> None:
        """
        Initialize the ConfigurationManager by loading config files.
        
        Args:
            config_filepath: Path to the configuration YAML file
            params_filepath: Path to the parameters YAML file
            schema_filepath: Path to the schema YAML file
        """
        # Load configuration files
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)
        
        # Create root artifacts directory
        create_directories([self.config.artifacts_root])
        
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Returns DataIngestionConfig object with parameters from config.yaml
        
        Returns:
            DataIngestionConfig: Configuration object for data ingestion
        """
        config = self.config.data_ingestion
        
        # Create data ingestion directory
        create_directories([config.root_dir])
        
        # Create and return the data ingestion configuration
        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )
        
        return data_ingestion_config