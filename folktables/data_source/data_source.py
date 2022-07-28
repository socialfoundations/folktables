from typing import Protocol


class DataSource(Protocol):
    """Defines an interface that all objects to (down)load a dataset must
    follow.
    """

    def get_data(self, **kwargs):
        """Gets the dataset the user is requesting."""

    def _load_data(self, **kwargs):
        """Loads the dataset from local memory."""

    async def _download_data(self, **kwargs):
        """Downloads the dataset from the corresponding URL."""
