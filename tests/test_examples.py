"""Run tests for the examples in the README."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from folktables import ACSDataSource, ACSEmployment

SEED = 0

def test_download():
    data_source = ACSDataSource(survey_year='2018', horizon='1-Year', survey='person')
    acs_data = data_source.get_data(states=["CA"], download=True)
    features, label, group = ACSEmployment.df_to_numpy(acs_data)

    assert features.shape == (378817, 16)
    assert label.shape == (378817, ) 
    assert group.shape == (378817, )

def test_train():
    data_source = ACSDataSource(survey_year='2018', horizon='1-Year', survey='person')
    acs_data = data_source.get_data(states=["CA"], download=True)
    features, label, group = ACSEmployment.df_to_numpy(acs_data)

    X_train, X_test, y_train, y_test, group_train, group_test = train_test_split(
        features, label, group, test_size=0.2, random_state=SEED)

    model = make_pipeline(StandardScaler(), LogisticRegression(random_state=SEED))
    model.fit(X_train, y_train)

    yhat = model.predict(X_test)

    white_tpr = np.mean(yhat[(y_test == 1) & (group_test == 1)])
    black_tpr = np.mean(yhat[(y_test == 1) & (group_test == 2)])

    ref_value = 0.04490694888127078
    assert np.allclose(white_tpr - black_tpr, ref_value, atol=1e-2), \
        f"Expected {ref_value}, got {white_tpr - black_tpr}"

if __name__ == "__main__":
    test_download()
    test_train()
