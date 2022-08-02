class FileDownloadError(Exception):
    """Exception raised when the HTTP request to download the data fails."""


class UnsupportedOSError(Exception):
    """Exception raised when the user passes the value for an OS for which
    a dataset is not supported.
    """
