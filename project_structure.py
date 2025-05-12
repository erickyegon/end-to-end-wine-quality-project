import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

# Set project name
project_name = "mlProject"

# Define list of files to be created
list_of_files = [
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "main.py",
    "app.py",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb",
    "templates/index.html"
]

# Create directories and files
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")

# Initialize setup.py with basic content
with open("setup.py", "w") as f:
    f.write(f'''
from setuptools import setup, find_packages

setup(
    name="{project_name}",
    version="0.0.1",
    author="Erick Kiprotich Yegon",
    author_email="keyegon@com",
    description="A small package for ML pipeline project",
    packages=find_packages(),
    python_requires=">=3.7",
)
''')
logging.info(f"setup.py file has been configured.")

# Initialize requirements.txt with basic dependencies
with open("requirements.txt", "w") as f:
    f.write('''
numpy
pandas
scikit-learn
matplotlib
jupyter
pytest
tqdm
pathlib
pyyaml
''')
logging.info(f"requirements.txt has been configured with basic dependencies.")

print("Project structure created successfully!")
