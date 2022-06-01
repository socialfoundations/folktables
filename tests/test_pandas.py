from folktables import ACSDataSource, ACSIncome, ACSEmployment


data_source = ACSDataSource(survey_year='2018', horizon='1-Year', survey='person')
ca_data = data_source.get_data(states=["CA"], download=True)

num_features, num_labels, num_group = ACSIncome.df_to_numpy(ca_data)
pan_features, pan_labels, pan_group = ACSIncome.df_to_pandas(ca_data)

assert (pan_features.to_numpy() == num_features).all()
assert (pan_labels.to_numpy().squeeze() == num_labels).all()
assert (pan_group.to_numpy() == num_group).all()

num_features, num_labels, num_group = ACSEmployment.df_to_numpy(ca_data)
pan_features, pan_labels, pan_group = ACSEmployment.df_to_pandas(ca_data)

assert (pan_features.to_numpy() == num_features).all()
assert (pan_labels.to_numpy().squeeze() == num_labels).all()
assert (pan_group.to_numpy() == num_group).all()
