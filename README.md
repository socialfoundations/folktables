# Folktables

**Folktables** is a Python package that provides access to datasets derived from the US Census, facilitating the benchmarking of machine learning algorithms. The package includes a suite of pre-defined prediction tasks in domains including income, employment, health, transportation, and housing, and also includes tools for creating new prediction tasks of interest in the US Census data ecosystem. The package also enables systematic studies of the effect of distribution shift, as each prediction task can be instantiated on datasets spanning multiple years and all states within the US.


## Table of Contents
1. [Basic installation instructions](#basic-installation-instructions)
2. [Quick start examples](#quick-start-examples)
3. [Datasets in folktables](#datasets-in-folktables)
5. [Frequently asked questions](#frequently-asked-questions)
6. [Citing folkTables](#citing-folktables)

Folktables is still under active development! If you find bugs or have feature
requests, please file a
[Github issue](https://github.com/zykls/folktables/issues). 
We welcome all kinds of issues, especially those related to correctness, documentation, performance, and new features.


## Basic installation instructions
1. (Optionally) create a virtual environment
```
python3 -m venv folkenv
source folkenv/bin/activate
```
2. Install via pip
```
pip install folktables
```
You can also install folktables directly from source.
```
git clone https://github.com/zykls/folktables.git
cd folktables
pip install -r requirements.txt
```


## Quick start examples
Folktables contains a suite of prediction tasks derived from US Census data that
can be easily downloaded and used for a variety of benchmarking tasks.

### Evaluating algorithms for fair machine learning
We first construct a data source for the 2018 yearly [American Community
Survey](https://www.census.gov/programs-surveys/acs), download the
corresponding data for California, and use this data to instantiate a
prediction task of interest, for example, the `ACSEmployment` task.
```py
from folktables import ACSDataSource, ACSEmployment

data_source = ACSDataSource(survey_year='2018', horizon='1-Year', survey='person')
acs_data = data_source.get_data(states=["CA"], download=True)
features, label, group = ACSEmployment.df_to_numpy(acs_data)
```
Next we train a simple model on this dataset and use the `group` labels to
evaluate the models violation of [equality of opportunity](https://fairmlbook.org/), a common fairness
metric.
```py
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test, group_train, group_test = train_test_split(
    features, label, group, test_size=0.2, random_state=0)

###### Your favorite learning algorithm here #####
model = LogisticRegression()
model.fit(X_train, y_train)

yhat = model.predict(X_test)

white_tpr = np.mean(yhat[(y_test == 1) & (group_test == 1)])
black_tpr = np.mean(yhat[(y_test == 1) & (group_test == 2)])

# Equality of opportunity violation: 0.0455
white_trp - black_trp
```
The ACS data source contains data for all fifty states, each of which has a
slightly different distribution of features and response. This increases the
diversity of environments in which we can evaluate our methods. For instance, we
can generate another `ACSEmployment` task using data from Texas and repeat the
experiment
```py
acs_tx = data_source.get_data(states=["TX"], download=True)
tx_features, tx_label, tx_group = ACSEmployment.df_to_numpy(acs_tx)

features, label, group = ACSEmployment.df_to_numpy(acs_tx)
X_train, X_test, y_train, y_test, group_train, group_test = train_test_split(
    features, label, group, test_size=0.2, random_state=0)

model = LogisticRegression()
model.fit(X_train, y_train)

yhat = model.predict(X_test)
white_trp = np.mean(yhat[(y_test == 1) & (group_test == 1)])
black_trp = np.mean(yhat[(y_test == 1) & (group_test == 2)])

# Equality of opportunity violation: 0.0397
white_trp - black_trp
```

### Distribution shift across states



### Distribution shift across time

### Creating a new prediction task
Folktables also makes it seamless to create a new prediction task based on US Census data.
TODO!

## Datasets in folktables
TODO!


## Frequently asked questions
TODO!


## Citing folktables
TODO!
