from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="countries-info-mg",
    version="1.0.0",
    author="MohaNed Ghawar",
    author_email="mohaned.ghawar@gmail.com",
    description="A comprehensive Python library for accessing detailed country information",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MohanedGhawar2019/countries-info",
    packages=find_packages(),
    package_data={
        'countries_info': ['countries.json'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
