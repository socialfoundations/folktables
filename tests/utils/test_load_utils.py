import pathlib
import zipfile

import pytest

from folktables import exceptions
from folktables.utils import load_utils


def test_extract_content_from_zip(tmp_path):
    """Tests we can successfully extract a file from a zip asset. Additionally,
    check that the zipp asset is deleted.
    """
    download_path = tmp_path / 'foo.zip'

    existing_file_path = tmp_path / 'foo.txt'
    existing_file_path.write_text("hello world")

    with zipfile.ZipFile(download_path, 'w') as asset:
        asset.write(existing_file_path, 'foo.txt')

    # Sanity check to make sure the zip file exists.
    assert download_path.exists()

    # Delete the file we just zipped from the directory and make sure
    # this operation is successful.
    existing_file_path.unlink()
    assert not existing_file_path.exists()

    load_utils.extract_content_from_zip(str(tmp_path),
                                        'foo.txt',
                                        download_path)

    assert pathlib.Path(tmp_path, 'foo.txt').exists()

    with open(existing_file_path, 'r') as file:
        assert file.read() == "hello world"

    assert not download_path.exists()


def test_extract_content_from_zip_raises_invalid_file_path():
    """Tests that an InvalidFilePath exception is raised if the we provide
    a file path equal to that of the zip file.
    """
    with pytest.raises(exceptions.InvalidFilePath):
        load_utils.extract_content_from_zip('test_dir',
                                            'foo.zip',
                                            'test_dir/foo.zip')
