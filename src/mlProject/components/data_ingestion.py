import os
import urllib.request as request
import zipfile
import shutil
from pathlib import Path
from mlProject import logger
from mlProject.utils.common import get_size
from mlProject.entity.config_entity import DataIngestionConfig

# Make sure class name is exactly: DataIngestion
class DataIngestion:
    """
    Handles downloading and extracting data files from various sources.
    """
    def __init__(self, config: DataIngestionConfig):
        self.config = config
    
    def _is_kaggle_url(self):
        """Check if the URL is from Kaggle."""
        return "kaggle" in self.config.source_URL.lower()
    
    def _is_github_url(self):
        """Check if the URL is from GitHub."""
        return "github" in self.config.source_URL.lower()
    
    def _download_using_kaggle_api(self):
        """Download dataset using Kaggle API if available."""
        try:
            import kaggle
            if "datasets" in self.config.source_URL:
                parts = self.config.source_URL.split("datasets/")
                if len(parts) > 1:
                    dataset_name = parts[1].split("/download")[0]
                else:
                    dataset_name = self.config.source_URL
            else:
                dataset_name = self.config.source_URL.split("/")[-1]
                
            logger.info(f"Attempting to download Kaggle dataset: {dataset_name}")
            
            os.makedirs(os.path.dirname(self.config.local_data_file), exist_ok=True)
            
            kaggle.api.dataset_download_files(
                dataset_name,
                path=os.path.dirname(self.config.local_data_file),
                unzip=True
            )
            logger.info(f"Downloaded dataset using Kaggle API: {dataset_name}")
            return True
        except Exception as e:
            logger.warning(f"Kaggle API download failed: {e}")
            logger.info("Falling back to alternative download method")
            return False
    
    def download_file(self):
        """Download the data file from the source URL to the local path."""
        # Use Kaggle API first if it's a Kaggle URL
        if self._is_kaggle_url():
            if self._download_using_kaggle_api():
                return
        
        # Otherwise, use direct URL download
        try:
            logger.info(f"Downloading file from {self.config.source_URL}")
            
            # GitHub URLs may need to be adjusted for raw content
            download_url = self.config.source_URL
            if self._is_github_url() and "/blob/" in download_url:
                download_url = download_url.replace("/blob/", "/raw/")
                
            filename, headers = request.urlretrieve(
                url=download_url,
                filename=self.config.local_data_file
            )
            logger.info(f"Downloaded {filename}")
        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            raise
    
    def extract_zip_file(self):
        """Extract the downloaded ZIP file to the specified directory."""
        # Skip extraction if files already exist in the unzip directory
        if os.path.exists(self.config.unzip_dir) and len(os.listdir(self.config.unzip_dir)) > 0:
            logger.info(f"Files already exist in {self.config.unzip_dir}, skipping extraction")
            return
        
        # Check if the zip file exists
        if not os.path.exists(self.config.local_data_file):
            # Don't raise an error if files are already in the unzip directory
            alt_csv_path = str(self.config.local_data_file).replace('.zip', '.csv')
            if os.path.exists(alt_csv_path):
                logger.info(f"Using CSV file found at {alt_csv_path}")
                # Create unzip directory
                os.makedirs(self.config.unzip_dir, exist_ok=True)
                # Copy the CSV file to the unzip directory
                dest_file = os.path.join(self.config.unzip_dir, os.path.basename(alt_csv_path))
                shutil.copy2(alt_csv_path, dest_file)
                logger.info(f"Copied CSV file to {dest_file}")
                return
            else:
                logger.error(f"No data file found")
                return
            
        # Create unzip directory
        os.makedirs(self.config.unzip_dir, exist_ok=True)
        
        # Extract files
        try:
            with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
                zip_ref.extractall(self.config.unzip_dir)
            
            logger.info(f"Extracted ZIP file to {self.config.unzip_dir}")
        except Exception as e:
            logger.error(f"Error extracting ZIP file: {e}")
            raise
            
    def initiate_data_ingestion(self):
        """
        Execute the complete data ingestion process:
        1. Download the data file 
        2. Extract it (if it's a ZIP file)
        3. Return the path to the extracted data
        """
        logger.info("Starting data ingestion process")
        try:
            # Check if files already exist
            if os.path.exists(self.config.unzip_dir) and len(os.listdir(self.config.unzip_dir)) > 0:
                logger.info(f"Files already exist in {self.config.unzip_dir}, skipping download and extraction")
                return self.config.unzip_dir
                
            # Try to download the file
            self.download_file()
            
            # Try to extract the file
            self.extract_zip_file()
            
            logger.info("Data ingestion completed successfully")
            return self.config.unzip_dir
        except Exception as e:
            logger.error(f"Data ingestion failed: {e}")
            raise