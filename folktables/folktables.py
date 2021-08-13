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
