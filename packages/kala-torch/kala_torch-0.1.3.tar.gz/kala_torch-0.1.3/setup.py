from setuptools import setup, find_packages
import os

# Read the contents of the README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kala_torch",
    version="0.1.3",
    author="N V R K SAI KAMESH YADAVALLI",
    author_email="saikamesh.y@gmail.com",
    description="A comprehensive PyTorch-based utility module.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kalasaikamesh944",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "torch>=1.11.0",
        "numpy>=1.19.0",
        "torchvision>=0.5.0",
        "tqdm>=4.36.0",
    ],
    entry_points={
        "console_scripts": [
            "kala-torch=kala_torch_module.main:main",
        ],
    },
)
