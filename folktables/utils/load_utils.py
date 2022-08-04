import pathlib
import zipfile

from folktables import exceptions


def extract_content_from_zip(data_dir, file_name, zip_file):
    """Extracts the contents from a Zip file, and removes the Zip file
    if its file path is not the same as that of the extracted
    file.

    Parameters
    ----------
    data_dir : str
        Path to the directory where the file will be stored.
    file_name : str
        Name that will be given to the extracted file.
    zip_file : pathlib.Path
        Path to where the Zip file is located.
    """
    if not isinstance(zip_file, pathlib.Path):
        # We want to make sure that even if the user doesn't pass a
        # pathlib.Path object, that this function doesn't break because
        # of that.
        zip_file = pathlib.Path(zip_file)

    if zip_file == pathlib.Path(data_dir, file_name):
        # We want to avoid the case in which the download path
        # (i.e., the zip asset) has the same name as the file to be extracted.
        raise exceptions.InvalidFilePath(
           f'Invalid `data_dir` and `file_name`. The path resolves to:\n'
           f'{pathlib.Path(data_dir, file_name).resolve()}'
           f'Please make sure that the above path is not the same as that '
           f'to which the data was downloaded:\n{zip_file.resolve()}'
        )

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extract(file_name, path=data_dir)

    zip_file.unlink()
