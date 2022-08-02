import pathlib
import zipfile


def extract_content_from_zip(data_dir, file_name, download_path):
    """Extracts the contents from a Zip file, and removes the Zip file
    if its file path is not the same as that of the extracted
    file.

    Parameters
    ----------
    data_dir : str
        Path to the directory where the file will be stored.
    file_name : str
        Name that will be given to the extracted file.
    download_path : str
        Path to where the Zip file is located.
    """
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extract(file_name, path=data_dir)

    # This is probably always True as the file we're extracting is
    # most likely not another ".zip" file.
    if download_path != pathlib.Path(data_dir, file_name):
        pathlib.Path.unlink(download_path)
