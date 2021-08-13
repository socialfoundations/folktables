from setuptools import setup, find_packages

setup(
    name="folktables",
    version="0.0.11",
    author="John Miller, Frances Ding, Ludwig Schmidt, Moritz Hardt",
    author_email="miller_john@berkeley.edu",
    description="New machine learning benchmarks from tabular datasets.",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "requests",
        "sklearn",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
    ],
    python_requires=">=3.7",
)
