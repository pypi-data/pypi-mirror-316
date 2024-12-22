from setuptools import setup, find_packages
import os


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="unosql",  
    version="1.1.0",  
    description="unosql - A Lightweight NoSQL Database for MicroPython",
    long_description=long_description,  
    long_description_content_type="text/markdown", 
    author="Arman Ghobadi",  
    author_email="arman.ghobadi.ag@gmai.com",  
    url="https://github.com/armanghobadi/unosql",  
    packages=find_packages(),  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
)
