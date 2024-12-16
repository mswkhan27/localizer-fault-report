# setup.py

from setuptools import setup, find_packages

setup(
    name="localizer",  # Package name
    version="0.1",
    description="A Python-based fault localization tool",
    author="Shehroz Khan, Gaadha Sudheerbabu, Dragos Truscan, Bianca Elena Staicu, Tanwir Ahmad",
    author_email="shehroz.khan@abo.fi",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
