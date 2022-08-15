import pathlib

import pytest

from folktables import exceptions
from folktables.utils import download_utils
from folktables.utils import files_resources

MOCK_URL = 'http://test.com'


def test_download_file(tmp_path, requests_mock):
    """Tests we can successfully download a file from a specified URL
    and save it to a specified location.
    """
    file_path = tmp_path / 'test_file.txt'

    requests_mock.get(MOCK_URL, text='hello world')

    download_utils.download_file(MOCK_URL, file_path)

    assert file_path.is_file()

    with open(file_path, 'r') as file:
        assert file.read() == 'hello world'


def test_determine_files_to_download(tmp_path):
    """Tests that we can differentiate between which files need to be
    downloaded and which ones are already downloaded.
    """
    file_to_download = files_resources.FilesResource(
        url=MOCK_URL,
        download_path=pathlib.Path('foo', 'bar.zip'),
        file_name='bar.txt',
        data_dir=str(tmp_path)
    )
    existing_file = files_resources.FilesResource(url=MOCK_URL,
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
    file_to_download = files_resources.FilesResource(
        url=MOCK_URL,
        download_path=pathlib.Path('foo', 'bar.zip'),
        file_name='bar.txt',
        data_dir=str(tmp_path)
    )

    with pytest.raises(FileNotFoundError):
        download_utils.determine_files_to_download(
            files_resources=[file_to_download], download=False
        )


def test_download_datasets_with_multiple_files(tmp_path, requests_mock):
    """Tests we can successfully download multiple datasets by using multiple
    threads.
    """
    # Setup the resources/files we're going to be downloading.
    download_path_0 = tmp_path / 'test_file_0.txt'
    requests_mock.get(MOCK_URL, text='hello world')
    file_to_download_0 = files_resources.FilesResource(
        url=MOCK_URL,
        download_path=download_path_0,
        file_name='test_file_0.txt',
        data_dir=str(tmp_path)
    )

    download_path_1 = tmp_path / 'test_file_1.txt'
    requests_mock.get('http://foobar.com', text='foo bar')
    file_to_download_1 = files_resources.FilesResource(
        url='http://foobar.com',
        download_path=download_path_1,
        file_name='test_file_1.txt',
        data_dir=str(tmp_path)
    )

    # Test we can successfully download the files.
    download_utils.download_datasets([file_to_download_0, file_to_download_1])

    # Test we've successfully downloaded the first file.
    assert download_path_0.is_file()

    with open(download_path_0, 'r') as file:
        assert file.read() == 'hello world'

    # Test we've successfully downloaded the second file.
    assert download_path_1.is_file()

    with open(download_path_1, 'r') as file:
        assert file.read() == 'foo bar'


def test_download_datasets_only_one_file(tmp_path, requests_mock):
    """Tests we can successfully download only one dataset.
    """
    download_path = tmp_path / 'test_file.txt'
    requests_mock.get(MOCK_URL, text='hello world')
    file_to_download = files_resources.FilesResource(
        url=MOCK_URL,
        download_path=download_path,
        file_name='test_file.txt',
        data_dir=str(tmp_path)
    )

    download_utils.download_datasets([file_to_download])

    assert download_path.is_file()

    with open(download_path, 'r') as file:
        assert file.read() == 'hello world'


def test_download_datasets_raises_no_files_to_download():
    """Tests that we can catch the instance when there are no files to be
    downloaded and that a `NoFilesToDownload` exception is raised.
    """
    with pytest.raises(exceptions.NoFilesToDownload):
        download_utils.download_datasets([])
