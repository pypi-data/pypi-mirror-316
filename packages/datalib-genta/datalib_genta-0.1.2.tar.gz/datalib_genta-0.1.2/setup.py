from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file to use as long description
here = Path(__file__).parent
long_description = (here / "README.md").read_text()

setup(
    name="datalib_genta",
    version="0.1.2",
    description="A Python library for data manipulation, statistics, and visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Set the correct content type (markdown or reStructuredText)
    author="Ibrahim Trabelsi",
    author_email="Trabelsi_Ibrahim@hotmail.com",  # Update with your actual email
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "scikit-learn",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
