# Folktables


# TODO: Add to PyPI.
To make the shared code available outside the `pkg/tablebench` directory, you can make the code accessible as a Python package by running the following command in the `pkg` directory:
```
pip install -e .
```
This also installs the dependencies for our shared code listed in `setup.py` (e.g., NumPy, Pandas, etc.) if they are not available yet.
After installing the package, you can simply import the code with
```
import tablebench
```
