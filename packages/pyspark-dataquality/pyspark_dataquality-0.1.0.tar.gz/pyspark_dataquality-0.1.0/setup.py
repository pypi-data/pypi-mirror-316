from setuptools import setup, find_packages

setup(
    name="pyspark_dataquality",
    version="0.1.0",
    author="Abhishek Kumar",
    author_email="officialabhishek1997@gmail.com",
    description="This library is used for Data Quality",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "Jinja2==3.1.4",
        "MarkupSafe==3.0.2",
        "py4j==0.10.9.7",
        "pyspark==3.5.3"
    ],
)
