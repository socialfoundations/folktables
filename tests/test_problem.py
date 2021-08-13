import numpy as np
import pandas as pd

from folktables import BasicProblem


def test_basic_problem_simple():
    df = pd.DataFrame(data={'col1': [11, 12], 'col2': [21, 22], 'col3': [31, 32]})
    prob = BasicProblem(features=['col1', 'col2'],
                        target='col3')
    X, y, _ = prob.df_to_numpy(df)
    assert np.allclose(X, [[11, 21], [12, 22]])
    assert np.allclose(y, [31, 32])
