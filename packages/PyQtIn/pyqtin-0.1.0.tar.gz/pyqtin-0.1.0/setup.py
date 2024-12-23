from setuptools import setup, find_packages
from PYQTIN import Variant1

setup(
    name="PyQtIn",
    version="0.1.0",
    description="libary",
    author="Berg679",
    author_email="redmigardo@gmail.com",
    packages=find_packages(),
    install_requires=[],  # Сюда можно добавлять зависимости
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
