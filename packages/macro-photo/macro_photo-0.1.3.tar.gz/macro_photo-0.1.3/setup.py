from setuptools import setup, find_packages
import io

setup(
    name="macro-photo",
    version="0.1.3",
    author="MacroPhoto",
    author_email="bidifeb142@owube.com",
    description="A Python library for generating images using advanced AI technology",
    long_description=io.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/macro-photo/macro-photo",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.31.0",
        "colorama>=0.4.6",
    ],
)
