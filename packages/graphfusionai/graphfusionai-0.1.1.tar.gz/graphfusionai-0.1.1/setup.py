from setuptools import setup, find_packages
import os

# Load the README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="graphfusionai",
    version="0.1.2",
    description="GraphFusionAI: A framework for neural memory networks and knowledge graphs",
    long_description=long_description,  
    long_description_content_type="text/markdown",  
    author="Kiplangat Korir",
    author_email="Korir@GraphFusion.onmicrosoft.com",
    url="https://github.com/GraphFusion/graphfusion",  
    packages=find_packages(where="graphfusionai"),
    package_dir={"": "graphfusionai"},
    install_requires=[
        "torch",
        "transformers",
        "networkx",
        "scikit-learn",
        "numpy",
        "pandas",
        "matplotlib",
        "tqdm",
        "flask",
        "pytest"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",

    keywords='AI, neural memory, knowledge graphs, deep learning',
    license='MIT',
)
