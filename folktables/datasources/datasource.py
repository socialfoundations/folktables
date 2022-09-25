from abc import ABC, abstractmethod


class DataSource(ABC):
    """Defines an interface that all objects to (down)load a dataset must
    follow.
    """
    def __init__(self, root_dir='data'):
        self._root_dir = root_dir

    @abstractmethod
    def get_data(self, **kwargs):
        """Gets the dataset the user is requesting."""
