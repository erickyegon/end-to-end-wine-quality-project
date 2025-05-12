from setuptools import setup, find_packages

setup(
    name="mlProject",
    version="0.0.1",
    author="Erick K. Yegon",
    author_email="keyegon@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)