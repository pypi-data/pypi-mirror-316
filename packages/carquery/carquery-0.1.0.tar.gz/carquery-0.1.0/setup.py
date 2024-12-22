from setuptools import setup, find_packages

setup(
    name="carquery",
    version="0.1.0",
    author="Salman Khan",
    author_email="salman@sprotechs.com",
    description="A Python library for fetching car data from CarQueryAPI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Salman0x01/Car-Model-Data-Scraper/tree/main",  # Replace with your GitHub repo URL
    packages=find_packages(),
    install_requires=[
        "requests",
        "prettytable",
        "tqdm"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
