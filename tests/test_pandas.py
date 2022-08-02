import numpy as np

from folktables import ACSDataSource, ACSIncome, ACSEmployment, ACSHealthInsurance, generate_categories


def test_pandas_with_numpy():
    data_source = ACSDataSource(survey_year='2018', horizon='1-Year', survey='person')
    ca_data = data_source.get_data(states=["CA"], download=True)

    num_features, num_labels, num_group = ACSIncome.df_to_numpy(ca_data)
    pan_features, pan_labels, pan_group = ACSIncome.df_to_pandas(ca_data)

    assert (pan_features.to_numpy() == num_features).all()
    assert (pan_labels.to_numpy().squeeze() == num_labels).all()
    assert (pan_group.to_numpy().squeeze() == num_group).all()

    assert pan_features.index.equals(pan_labels.index)
    assert pan_features.index.equals(pan_group.index)

    num_features, num_labels, num_group = ACSEmployment.df_to_numpy(ca_data)
    pan_features, pan_labels, pan_group = ACSEmployment.df_to_pandas(ca_data)

    assert (pan_features.to_numpy() == num_features).all()
    assert (pan_labels.to_numpy().squeeze() == num_labels).all()
    assert (pan_group.to_numpy().squeeze() == num_group).all()

    assert pan_features.index.equals(pan_labels.index)
    assert pan_features.index.equals(pan_group.index)

    num_features, num_labels, num_group = ACSHealthInsurance.df_to_numpy(ca_data)
    pan_features, pan_labels, pan_group = ACSHealthInsurance.df_to_pandas(ca_data)

    assert (pan_features.to_numpy() == num_features).all()
    assert (pan_labels.to_numpy().squeeze() == num_labels).all()
    assert (pan_group.to_numpy().squeeze() == num_group).all()

    assert pan_features.index.equals(pan_labels.index)
    assert pan_features.index.equals(pan_group.index)


def test_definitions_download():
    data_source = ACSDataSource(survey_year='2018', horizon='1-Year', survey='person')
    definition_df = data_source.get_definitions(download=True)

    # test some definition_df properties
    assert len(definition_df.columns) == 7
    assert (np.isin(definition_df[0].unique(),['NAME','VAL'])).all()
    assert (np.isin(definition_df[2].unique(), ['C', 'N'])).all()


def test_pandas_automatic_categories():
    data_source = ACSDataSource(survey_year='2018', horizon='1-Year', survey='person')
    ca_data = data_source.get_data(states=["CA"], download=True)

    definition_df = data_source.get_definitions(download=True)
    features = ACSIncome.features
    categories = generate_categories(features=features, definition_df=definition_df)

    pan_features, pan_labels, pan_group = ACSIncome.df_to_pandas(ca_data)

    # every key needs to be a requested feature
    assert (np.isin(list(categories.keys()), features)).all()
    # every numeric value of a feature needs a definition
    for feature in categories.keys():
        assert (np.isin(pan_features[feature].unique(),list(categories[feature].keys()))).all()

    pan2_features, pan2_labels, pan2_group = ACSIncome.df_to_pandas(ca_data,categories=categories)

    assert (pan_features.to_numpy().shape == pan2_features.to_numpy().shape)
    assert (pan_labels.to_numpy().squeeze().shape == pan2_labels.to_numpy().squeeze().shape)
    assert (pan_group.to_numpy().squeeze().shape == pan2_group.to_numpy().squeeze().shape)

    # amount of unique values in each feature should still be the same
    for feature in pan_features.columns:
        assert len(pan_features[feature].unique()) == len(pan2_features[feature].unique())
