from setuptools import setup, find_packages

setup(
    name="pyhelloworld",  # Nama library di PyPI
    version="0.1.0",  # Versi awal
    author="Firza Aditya ",
    author_email="elbuho1315@gmail.com",
    description="A simple library to say hello",
    long_description="A Python package to generate greeting strings.",
    long_description_content_type="text/plain",
    url="https://github.com/firzaelbuho/pyhelloworld",  # Opsional
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
