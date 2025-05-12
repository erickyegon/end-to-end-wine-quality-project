from dataclasses import dataclass
from pathlib import Path
import urllib.request as request
import zipfile
import os
import shutil

@dataclass(frozen=True)
class DataIngestionConfig:
    """Configuration class for data ingestion parameters."""
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path