from setuptools import find_packages, setup
from os import path

working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding = 'utf-8') as f:
    long_description = f.read()

setup(
    name = "QuaNFS",
    version = "0.0.1",
    url = "https://github.com/PremSRajanampalle/QuantumBasedGeneticAlgorithm/tree/main",
    author = "Prem S Rajanampalle",
    author_email = "prem.rajanampalle@gmail.com",
    description = "A python package for implementing feature selection using quantum-based nature inspired algorithms",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    packages=find_packages(),
    install_requires = []
)