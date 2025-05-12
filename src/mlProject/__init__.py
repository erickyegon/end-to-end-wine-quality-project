import os
import sys
import logging
from logging.handlers import RotatingFileHandler

# Enhanced logging format with thread info for concurrent operations
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(threadName)s: %(message)s]"

# Environment-based log level
log_level = logging.DEBUG if os.environ.get("ML_ENV") == "development" else logging.INFO

# Create logs directory
log_dir = "logs"
log_filepath = os.path.join(log_dir, "running_logs.log")
os.makedirs(log_dir, exist_ok=True)

# Configure logging with rotation to prevent huge log files
logging.basicConfig(
    level=log_level,
    format=logging_str,
    handlers=[
        RotatingFileHandler(
            log_filepath, 
            maxBytes=10485760,  # 10MB
            backupCount=5       # Keep 5 backup files
        ),
        logging.StreamHandler(sys.stdout)
    ]
)

# Create logger with ML experiment context
logger = logging.getLogger("mlProjectLogger")

# Optional: Add experiment tracking info
def set_experiment_context(experiment_id=None, model_version=None, dataset=None):
    """Add ML experiment context to logs"""
    context = {}
    if experiment_id:
        context["experiment_id"] = experiment_id
    if model_version:
        context["model_version"] = model_version
    if dataset:
        context["dataset"] = dataset
    
    # Create filter to add context to log records
    class ContextFilter(logging.Filter):
        def filter(self, record):
            for k, v in context.items():
                setattr(record, k, v)
            return True
    
    logger.addFilter(ContextFilter())