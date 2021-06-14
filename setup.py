from setuptools import setup, find_packages

setup(
    name="tablebench",
    author="Frances Ding, Ludwig Schmidt, Moritz Hardt",
    description="New machine learning benchmarks from tabular datasets.",
    install_requires=[
		"click",
        "fairlearn",
        "ipympl",
        "joblib",
        "lightgbm",
        "matplotlib",
		"numba",
		"numpy",
        "pandas",
		"pytest",
		"scipy",
		"sklearn",
		"statsmodels",
		"tqdm",
        "xgboost",
    ],
    python_requires=">=3.7",
)
