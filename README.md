# Folktables

**Folktables** is a Python package that provides access to datasets derived from the US Census, facilitating the benchmarking of machine learning algorithms. The package includes a suite of pre-defined prediction tasks in domains including income, employment, health, transportation, and housing, and also includes tools for creating new prediction tasks of interest in the US Census data ecosystem. The package additionally enables systematic studies of the effect of distribution shift, as each prediction task can be instantiated on datasets spanning multiple years and all states within the US.


## Table of Contents
1. [Basic installation instructions](#basic-installation-instructions)
2. [Quick start examples](#quick-start-examples)
3. [Prediction tasks in folktables](#prediction-tasks-in-folktables)
5. [Scope and limitations](#scope-and-limitations)
6. [Citing folkTables](#citing-folktables)
7. [References](#references)

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

## Prediction tasks in folktables
Folktables provides the following pre-defined prediction tasks:

- **ACSIncome**: predict whether an individual's income is above \$50,000, after filtering the ACS PUMS data sample to only include individuals above the age of 16, who reported usual working hours of at least 1 hour per week in the past year, and an income of at least \$100. The threshold of \$50,000 was chosen so that this dataset can serve as a comparable replacement to the [UCI Adult dataset](https://archive.ics.uci.edu/ml/datasets/adult), but the income threshold can be changed easily to define new prediction tasks. 

- **ACSPublicCoverage**: predict whether an individual is covered by public health insurance, after filtering the ACS PUMS data sample to only include individuals under the age of 65, and those with an income of less than \$30,000. This filtering focuses the prediction problem on low-income individuals who are not eligible for Medicare.

- **ACSMobility**: predict whether an individual had the same residential address one year ago, after filtering the ACS PUMS data sample to only include individuals between the ages of 18 and 35. This filtering increases the difficulty of the prediction task, as the base rate of staying at the same address is above 90\% for the general population. 

- **ACSEmployment**: predict whether an individual is employed, after filtering the ACS PUMS data sample to only include individuals between the ages of 16 and 90. 

- **ACSTravelTime**: predict whether an individual has a commute to work that is longer than 20 minutes, after filtering the ACS PUMS data sample to only include individuals who are employed and above the age of 16. The threshold of 20 minutes was chosen as it is the US-wide median travel time to work  in the 2018 ACS PUMS data release.

Each of these tasks can be instantiated on different ACS PUMS data samples, as illustrated in the [quick start examples](#quick-start-examples).



## Scope and limitations
Census data is often used by social scientists to study the extent of inequality in income, employment, education, housing or other aspects of life. Such important substantive investigations should necessarily inform debates about discrimination in classification scenarios within these domains. However, folktables' contribution is not in this direction. The package uses Census data for the empirical study of machine learning algorithms that attempt to predict outcomes for individuals. Folktables may be used to compare different methods on axes including accuracy, robustness, and fairness metric satisfaction, in an array of different concrete settings. The distinction we draw between benchmark data and substantive domain-specific investigations resonates with recent work that points out issues with using data about risk assessments tools from the criminal justice domain as machine learning benchmarks [[1]](#1).

Another notable if obvious limitation of our work is that it is entirely US-centric. A richer dataset ecosystem covering international contexts within the algorithmic fairness community is still lacking. Although empirical work in the Global South is central in other disciplines, there continues to be much need for the North American fairness community to engage with it more strongly [[2]](#2).


## Citing folktables
TODO!



## References
<a id="1">[1]</a> 
M. Bao, A. Zhou, S. Zottola, B. Brubach, S. Desmarais, A. Horowitz, K. Lum, and S. Venkatasubramanian. It’s compaslicated: The messy relationship between rai datasets and algorithmic fairness benchmarks. arXiv preprint arXiv:2106.05498, 2021.

<a id="2">[2]</a> 
R. Abebe, K. Aruleba, A. Birhane, S. Kingsley, G. Obaido, S. L. Remy, and S. Sadagopan. Narratives and counternarratives on data sharing in africa. In Proc. of the ACM Conference on Fairness, Accountability, and Transparency, pages 329–341, 2021.
