from setuptools import setup, find_packages

setup(
    name="csv-to-excel-azure",
    version="1.0.0",
    author="Vipul Malhotra",
    author_email="vipulm124@gmail.com",
    description="A package to convert CSV files to Excel on Azure Blob Storage.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vipulm124/csv-excel-azure",
    packages=find_packages(),
    install_requires=[
        "azure-storage-blob",
        "pandas",
        "openpyxl"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
