from setuptools import setup, find_packages

setup(
    name="cerebro-client",  # Nombre del paquete en PyPI
    version="1.0.0",
    author="Percy Guerra",
    author_email="percy.guerra1@unmsm.edu.pe",
    description="Cliente Python para interactuar con la API de Cerebro Trading.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    #url="https://github.com/tuusuario/cerebro-client",  # Reemplaza con la URL de tu repositorio
    packages=find_packages(),
    install_requires=[
        "requests>=2.20.0",
        "pandas>=1.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
