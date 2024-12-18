from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="conciliation_model",
    version="0.11.0",
    description="Prueba",
    author="Conciliaciones - Kuantik",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.7.1",
        "pymongo>=4.7.0",
        "inflect>=7.2.1",
        "boto3>=1.34.99",
        "boto3-stubs[s3]>=1.34.99",
        "loggerk>=0.0.5",
        "pandas>=2.2.2"
    ],
    python_requires=">=3.8",
)
