from setuptools import setup, find_packages

setup(
    name="folktables",
    version="0.0.12",
    author="John Miller, Frances Ding, Ludwig Schmidt, Moritz Hardt",
    author_email="hardt@is.mpg.de",
    description="New machine learning benchmarks from tabular datasets.",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "requests",
        "scikit-learn",
    ],
    tests_require=[
        "requests-mock",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
    ],
    python_requires=">=3.7",
)
