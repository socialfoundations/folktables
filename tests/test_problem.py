import numpy as np
import pandas
import pytest
from sklearn.preprocessing import OneHotEncoder

from tablebench.data_source import BasicProblem


def test_basic_problem_simple():
    df = pandas.DataFrame(data={'col1': [11, 12], 'col2': [21, 22], 'col3': [31, 32]})
    prob = BasicProblem(feature_transforms={'col1': None, 'col2': None},
                        target='col3')
    X, y = prob.df_to_numpy(df)
    assert np.allclose(X, [[11, 21], [12, 22]])
    assert np.allclose(y, [31, 32])


def test_basic_problem_one_hot():
    df = pandas.DataFrame(data={'col1': [0, 1, 0],
                                'col2': [21, 22, 23],
                                'col3': [31, 32, 33]})
    def one_hot_transform(col):
        return OneHotEncoder(sparse=False).fit_transform(col.to_numpy()[..., np.newaxis])

    prob = BasicProblem(feature_transforms={'col1': one_hot_transform,
                                            'col2': None},
                        target='col3')
    X, y = prob.df_to_numpy(df)
    assert np.allclose(X, [[1, 0, 21],
                           [0, 1, 22],
                           [1, 0, 23]])
    assert np.allclose(y, [31, 32, 33])