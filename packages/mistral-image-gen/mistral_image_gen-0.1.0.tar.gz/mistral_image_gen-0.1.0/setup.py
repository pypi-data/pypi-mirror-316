from setuptools import setup, find_packages
import io

setup(
    name="mistral-image-gen",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python library for generating images using Mistral AI API",
    long_description=io.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mistral-image-gen",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.31.0",
    ],
)
