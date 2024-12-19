from setuptools import setup, find_packages

# Leer el contenido del archivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="practica_1_hack4u",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[],
    author="Aport",
    description="Una práctica de biblioteca donde consultar cursos de hack4u.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io",
    )
