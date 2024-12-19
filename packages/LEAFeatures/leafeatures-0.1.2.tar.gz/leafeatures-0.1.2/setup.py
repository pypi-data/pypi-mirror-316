from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="LEAFeatures",
    version="0.1.2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,  
    package_data={
        "": ["data/*.json"],  # Specify patterns to include data files
    },
    install_requires=[ 
        "adjustText==1.3.0",
        "ase==3.23.0",
        "ElMD==0.5.14",
        "matminer==0.9.1",
        "matplotlib",
        "monty==2024.5.24",
        "numpy>=1.16",
        "pandas",
        "plotly==5.19.0",
        "pymatgen==2024.5.1",
        "scikit_learn==1.5.2",
        "scipy==1.10.1",
        "seaborn==0.13.2",
        "setuptools",
        "SMACT==2.5.3",
        "tqdm==4.66.4",
    ],
    description="Local Enviroment-induced Atomic Features (LEAF)",
    author="Andrij Vasylenko",
    url="https://github.com/lrcfmd/LEAF",
    license="MIT",
)
