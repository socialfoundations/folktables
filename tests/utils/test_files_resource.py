import pathlib

from folktables.utils import files_resources


def test_files_reousrce():
    """Tests the `file_path` property."""
    resource = files_resources.FilesResource(
        url='http://foo',
        download_path=pathlib.Path('foo', 'bar.zip'),
        file_name='bar.test',
        data_dir='foo'
    )

    assert resource.file_path == pathlib.Path('foo', 'bar.test')
