from abc import ABC, abstractmethod


class DataSource(ABC):
    """Defines an interface that all objects to (down)load a dataset must
    follow.
    """

    @abstractmethod
    def get_data(self, **kwargs):
        """Gets the dataset the user is requesting."""
