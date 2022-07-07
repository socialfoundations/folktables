"""Implements abstract classes for folktables data source and problem definitions."""

from abc import ABC, abstractmethod

import numpy as np
import pandas as pd


class DataSource(ABC):
    """Provides access to data source."""

    @abstractmethod
    def get_data(self, **kwargs):
        """Get data sample from universe.

        Returns:
            Sample."""
        pass


class Problem(ABC):
    """Abstract class for specifying learning problem."""

    @abstractmethod
    def df_to_numpy(self, df):
        """Return learning problem as numpy array."""
        pass

    # Returns the column name
    @property    
    @abstractmethod
    def target(self):
        pass

    @property
    @abstractmethod
    def features(self):
        pass

    @property
    @abstractmethod
    def target_transform(self):
        pass


class BasicProblem(Problem):
    """Basic prediction or regression problem."""

    def __init__(self,
                 features,
                 target,
                 target_transform=None,
                 group=None,
                 group_transform=lambda x: x,
                 preprocess=lambda x: x,
                 postprocess=lambda x: x):
        """Initialize BasicProblem.

        Args:
            features: list of column names to use as features
            target: column name of target variable
            target_transform: feature transformation for target variable
            group: designated group membership feature
            group_transform: feature transform for group membership
            preprocess: function applied to initial data frame
            postprocess: function applied to final numpy data array
        """
        self._features = features
        self._target = target
        self._target_transform = target_transform
        self._group = group
        self._group_transform = group_transform
        self._preprocess = preprocess
        self._postprocess = postprocess

    def df_to_numpy(self, df):
        """Return data frame as numpy array.
        
        Args:
            DataFrame.
        
        Returns:
            Numpy array, numpy array, numpy array"""

        df = self._preprocess(df)
        res = []
        for feature in self.features:
            res.append(df[feature].to_numpy())
        res_array = np.column_stack(res)
        
        if self.target_transform is None:
            target = df[self.target].to_numpy()
        else:
            target = self.target_transform(df[self.target]).to_numpy()
        
        if self._group:
            group = self.group_transform(df[self.group]).to_numpy()
        else:
            group = np.zeros(len(target))

        return self._postprocess(res_array), target, group

    def df_to_pandas(self, df, categories=None, dummies=False):
        """Filters and processes a DataFrame (received from ```ACSDataSource''').
        
        Args:
            df: pd.DataFrame (received from ```ACSDataSource''')
            categories: nested dict with columns of categorical features
                and their corresponding encodings (see examples folder)
            dummies: bool to indicate the creation of dummy variables for
                categorical features (see examples folder)
        
        Returns:
            pandas.DataFrame."""
        
        df = self._preprocess(df)

        variables = df[self.features]

        if categories:
            variables = variables.replace(categories)
        
        if dummies:
            variables = pd.get_dummies(variables)

        variables = pd.DataFrame(self._postprocess(variables.to_numpy()),
                                 columns=variables.columns)

        if self.target_transform is None:
            target = df[self.target]
        else:
            target = self.target_transform(df[self.target])

        target = pd.DataFrame(target).reset_index(drop=True)

        if self._group:
            group = self.group_transform(df[self.group])
            group = pd.DataFrame(group).reset_index(drop=True)
        else:
            group = pd.DataFrame(0, index=np.arange(len(target)), columns=["group"])

        return variables, target, group

    def generate_categories(self, definition_df):
        """
        Generates a categories dictionary using the provided definition dataframe. Does not create a category mapping
        for variable requiring the 2010 Public use microdata area code (PUMA) as these need an additional definition
        file which are not unique without the state code.
        """
        categories = {}
        for feature in self.features:
            if 'PUMA' in feature:
                continue

            # extract definitions for this feature
            coll_definition = definition_df[(definition_df[0] == 'VAL') & (definition_df[1] == feature)]

            # extracts if the feature is numeric or categorical --> 'N' == numeric
            coll_type = coll_definition.iloc[0][2]
            if coll_type == 'N':
                # do not add to categories
                continue

            # transform to numbers as definitions are strings.
            mapped_col = pd.to_numeric(coll_definition[4], errors='coerce').fillna(-99999999999999.0)

            mapping_dict = {key: value.replace(';', ',') for (key, value) in
                            zip(mapped_col.tolist(), coll_definition[6].tolist())}

            # add default value
            if -99999999999999.0 not in mapping_dict:
                mapping_dict[-99999999999999.0] = 'N/A'
            mapping_dict[float('nan')] = mapping_dict[-99999999999999.0]
            del mapping_dict[-99999999999999.0]

            categories[feature] = mapping_dict
        return categories

    @property
    def target(self):
        return self._target
    
    @property
    def target_transform(self):
        return self._target_transform
    
    @property
    def features(self):
        return self._features
    
    @property
    def group(self):
        return self._group

    @property
    def group_transform(self):
        return self._group_transform
