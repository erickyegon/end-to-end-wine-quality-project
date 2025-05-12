# mlproj/logger.py
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

# Enhanced logging format
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

# Create logs directory
log_dir = "logs"
log_filepath = os.path.join(log_dir, "running_logs.log")
os.makedirs(log_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        RotatingFileHandler(
            log_filepath, 
            maxBytes=10485760,  # 10MB
            backupCount=5
        ),
        logging.StreamHandler(sys.stdout)
    ]
)

# Create and export the logger
logger = logging.getLogger("mlProjectLogger")