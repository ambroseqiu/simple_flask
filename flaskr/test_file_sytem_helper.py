from flaskr.file_system_helper import FileSystemHelper
from flaskr.file_system_helper import remove_file, check_file_is_existed, write_binary_to_file,\
        is_directory, give_relative_return_abs_path, check_post_is_allowed
import os


# class TestFileSystemHelper(FileSystemHelper):

#     @property
#     def get_local_system_file_path(self):
#         return self._local_system_file_path_

#     @property
#     def get_file_order_by_(self):
#         return self._file_order_by_

#     @property
#     def get_order(self):
#         return self._reverse_

#     @property
#     def get_filter_string(self):
#         return self._filtering_string_


def test_is_directory_false():
    assert is_directory("/not/a/valid/path") is False


def test_is_directory_true():
    assert is_directory(os.getcwd()) is True


# def test_set_local_system_file_path_equal_expected():
#     fs = TestFileSystemHelper()
#     expected_file_path = "/any/directory/anyfile"
#     fs.set_local_system_file_path(expected_file_path)
#     assert fs.get_local_system_file_path == expected_file_path

