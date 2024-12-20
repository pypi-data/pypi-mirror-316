from setuptools import setup, find_packages
import os

def load_requirements(filename="requirements.txt"):
    with open(filename, "r") as file:
        return file.read().splitlines()

setup(
    name="adimis_graph_builder",
    version="0.0.2",
    author="Aditya Mishra",
    author_email="aditya.mishra@adimis.in",
    description="Core utilities for the Adimis toolbox.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/adimis-ai/adimis-toolbox-core",
    packages=find_packages(),
    install_requires=load_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
