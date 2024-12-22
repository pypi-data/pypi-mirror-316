# setup.py

from setuptools import setup, find_packages

# Read the contents of the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Kala_NuroNetwork",
    version="0.1.0",
    description="A hybrid quantum-classical neural network framework using Kala_Quantum and Kala_Torch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="N V R K SAI KAMESH YADAVALLI",
    author_email="saikamesh.y@gmail.com",
    url="https://github.com/Kalasaikamesh944/Kala_NuroNetwork",
    packages=find_packages(),
    install_requires=[
        "torch",
        "Kala-Quantum-185",
        "Kala_Torch"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)