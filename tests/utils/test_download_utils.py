import pathlib

import pytest

from folktables import exceptions
from folktables.utils import download_utils
from folktables.utils import files_resources

MOCK_URL = 'http://test.com'


class DownloadTestResource(files_resources.FilesResource):
    """Toy class to test the FilesResource ABC."""


def test_download_file(tmp_path, requests_mock):
    """Tests we can successfully download a file from a specified URL
    and save it to a specified location.
    """
    file_path = tmp_path / 'test_file.txt'

    requests_mock.get(MOCK_URL, text='hello world')

    download_utils.download_file(MOCK_URL, file_path)

    assert file_path.is_file()


def test_download_error(tmp_path, requests_mock):
    """Tests that if the HTTP request wasn't successful (i.e., it doesn't
    return a 200 status code) that a FilesDownloadError is raised.
    """
    file_path = tmp_path / 'test_file.txt'

    requests_mock.get(MOCK_URL, text='hello world', status_code=400)

    with pytest.raises(exceptions.FileDownloadError):
        download_utils.download_file(MOCK_URL, file_path)


def test_async_download_file(tmp_path, requests_mock):
    """Tests we can deconstruct a FilesResource in order to download a file.
    """
    file_path = tmp_path / 'test_file.txt'
    requests_mock.get(MOCK_URL, text='hello world')
    file_to_download = DownloadTestResource(url=MOCK_URL,
                                            download_path=file_path,
                                            file_name='bar.txt',
                                            data_dir=str(tmp_path))

    download_path = download_utils.async_download_file(file_to_download)
    assert download_path == file_path


def test_determine_files_to_download(tmp_path):
    """Tests that we can differentiate between which files need to be
    downloaded and which ones are already downloaded.
    """
    file_to_download = DownloadTestResource(url=MOCK_URL,
                                            download_path=pathlib.Path(
                                                'foo', 'bar.zip'
                                            ),
                                            file_name='bar.txt',
                                            data_dir=str(tmp_path))
    existing_file = DownloadTestResource(url=MOCK_URL,
                                         download_path=pathlib.Path(
                                                'foo', 'bar.zip'
                                            ),
                                         file_name='foo.txt',
                                         data_dir=str(tmp_path))

    existing_file_path = tmp_path / 'foo.txt'
    existing_file_path.write_text("hello world")

    files_to_download = download_utils.determine_files_to_download(
        files_resources=[file_to_download, existing_file], download=True
    )

    assert len(files_to_download) == 1
    assert files_to_download[0] == file_to_download


def test_determine_files_to_download_raies_file_not_found(tmp_path):
    """Tests that if a file needs to be downloaded and the `download` flag is
    not `True`, that a `FileNotFoundError` is raised.
    """
    file_to_download = DownloadTestResource(url=MOCK_URL,
                                            download_path=pathlib.Path(
                                                'foo', 'bar.zip'
                                            ),
                                            file_name='bar.txt',
                                            data_dir=str(tmp_path))

    with pytest.raises(FileNotFoundError):
        download_utils.determine_files_to_download(
            files_resources=[file_to_download], download=False
        )
