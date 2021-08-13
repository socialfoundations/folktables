"""Run tests for the examples in the README."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from folktables import ACSDataSource, ACSEmployment

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
        features, label, group, test_size=0.2, random_state=0)

    model = make_pipeline(StandardScaler(), LogisticRegression())
    model.fit(X_train, y_train)

    yhat = model.predict(X_test)

    white_tpr = np.mean(yhat[(y_test == 1) & (group_test == 1)])
    black_tpr = np.mean(yhat[(y_test == 1) & (group_test == 2)])

    assert np.allclose(white_tpr - black_tpr, 0.04549392964278809)

if __name__ == "__main__":
    test_download()
    test_train()
