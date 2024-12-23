# dummy-problems
Solving "simple" problems using machine learning to improve my understanding (and have some fun!).

# Project structure
I am mostly following the structure from https://python-poetry.org/docs/basic-usage/#project-setup and https://github.com/Lightning-AI/deep-learning-project-template.

There are three key elements: **dataloaders**, **models**, and **evaluation**. Additionally, **visualisation** tools will help with development and results.

## Dataloaders


## Models


## Evaluation 


## Visualisation


# Installation
## Docker (recommended)
To install the required dependencies and run the code, use a Docker container:
```
cd docker
docker compose up
```

## Pip (experimental)
To install as a Python package, run:
```
pip install dummy-problems
```

Note: published following: https://www.digitalocean.com/community/tutorials/how-to-publish-python-packages-to-pypi-using-poetry-on-ubuntu-22-04

# Example 1: generating a synthetic dataset and benchmarking different classifiers.
Firstly, run `notebooks/synthetic_data_generation.ipynb` to generate a dataset of uppercase grayscale images. Parameters can be easily modified to increase/reduce the size of the images and/or the randomness of the dataset.

Secondly, ...
