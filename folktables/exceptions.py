class FolktablesException(Exception):
    """Base exception for all exceptions raised by Folktables."""


class FileDownloadError(FolktablesException):
    """Exception raised when the HTTP request to download the data fails."""


class UnsupportedOSError(FolktablesException):
    """Exception raised when the user passes the value for an OS for which
    a dataset is not supported.
    """


class InvalidFilePath(FolktablesException):
    """Exception raised when the user wants to assign the same file path to
    the data being extracted from a zip file as the zip file itself. Note
    that if we were to allow this, then the promise that the data has been
    extracted is broken as we don't want to be dealing with zip files after
    extracting the data from it.
    """


class NoFilesToDownload(FolktablesException):
    """Exception raised when there are no files to be downloaded (i.e.,
    the list is empty), but the functions to download files are still called.
    """
