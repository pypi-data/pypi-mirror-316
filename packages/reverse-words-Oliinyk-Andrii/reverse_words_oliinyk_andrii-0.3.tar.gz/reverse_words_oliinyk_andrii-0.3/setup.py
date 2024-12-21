from setuptools import setup, find_packages
import codecs
import os

with open("README.md", "r") as f:
    description = f.read()
# Setting up
setup(
    name="reverse_words_Oliinyk_Andrii",
    version='0.3',
    author="oliinyka",
    packages=find_packages(),
    install_requires=[],
    long_description_content_type="text/markdown",
    long_description=description
)