# Folktables

**Folktables** is a Python package that provides access to datasets derived from the US Census, facilitating the benchmarking of machine learning algorithms. The package includes a suite of pre-defined prediction tasks in domains including income, employment, health, transportation, and housing, and also includes tools for creating new prediction tasks of interest in the US Census data ecosystem. The package additionally enables systematic studies of the effect of distribution shift, as each prediction task can be instantiated on datasets spanning multiple years and all states within the US.


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
### Loading pre-defined prediction tasks
Folktables contains a suite of prediction tasks derived from US Census data that can be easily downloaded and inputted into learning algorithms of interest. 
We first construct a data source and download data from the 1-Year sample in
2018 for California (`CA`) and New York (`NY`). Next we instantiate the
prediction task of interest, for example, ACSEmployment, on this data sample.
```py
from folktables import ACSDataSource, ACSEmployment

data_source = ACSDataSource(survey_year='2018', horizon='1-Year', survey='person')
acs_data = data_source.get_data(states=['CA', 'NY'], download=True)
features, label, group = ACSEmployment.df_to_numpy(acs_data)
```
Finally, we can apply machine learning algorithms to the instantiated prediction task. For example, we may train a logistic regression model from sci-kit learn.
```py
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test, group_train, group_test = train_test_split(features, label, group, test_size=0.2, random_state=0)
model = LogisticRegression()
model.fit(X_train, y_train)
model.score(X_test, y_test)
```

### Creating a new prediction task
Folktables also makes it seamless to create a new prediction task based on US Census data.
TODO!

## Datasets in folktables
TODO!


## Frequently asked questions
TODO!


## Citing folktables
TODO!
