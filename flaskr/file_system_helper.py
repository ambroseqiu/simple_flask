import os, glob
from enum import IntEnum
from flask import current_app

app = current_app


class OrderBy(IntEnum):
    lastModified = 1
    size = 2
    filename = 3


class FileSystemHelperResponse(IntEnum):
    NOT_FOUND = 404
    SUCCESS = 200
    OPERATION_NOT_ALLOWED = 405


class FileSystemHelper:
    def __init__(self):
        self._local_system_file_path_ = "./file"
        self.__order_dict_ = {'lastModified': 1, "size": 2, "filename": 3}
        self._file_order_by_ = OrderBy(self.__order_dict_['filename'])
        self._reverse_ = False
        self._filtering_string_ = '*'

    def set_local_system_file_path(self, location) -> bool:
        if location is None:
            return True
        self._local_system_file_path_ = str(location)
        return is_directory(self._local_system_file_path_)

    def set_file_order_by(self, orderby_kind) -> bool:
        if orderby_kind in self.__order_dict_:
            self._file_order_by_ = OrderBy(self.__order_dict_[orderby_kind])
        elif orderby_kind is not None:
            return False
        return True

    def set_sort_order(self, order_string='Descending') -> bool:
        if order_string == 'Descending':
            self._reverse_ = False
        elif order_string == 'Ascending':
            self._reverse_ = True
        elif order_string is not None:
            return False
        return True

    def set_filtering_string(self, strings):
        if strings is not None:
            self._filtering_string_ = strings

    def get_filter_dict_by_string(self, dirs_list) -> bool:
        search_pattern = os.path.join(self._local_system_file_path_, self._filtering_string_)
        # print(search_pattern)
        for file in glob.iglob(search_pattern):
            dirs_list.append(os.path.basename(file))
        # print(dirs_list)
        return dirs_list != []

    def get_sort_dict(self, dirs_list) -> bool:
        if self._file_order_by_ == OrderBy.size:
            dirs_list.sort(key=lambda x: os.path.getsize(os.path.join(self._local_system_file_path_, x)), reverse=self._reverse_)
        elif self._file_order_by_ == OrderBy.lastModified:
            dirs_list.sort(key=lambda x: os.path.getmtime(os.path.join(self._local_system_file_path_, x)), reverse=self._reverse_)
        elif self._file_order_by_ == OrderBy.filename:
            dirs_list.sort(key=str.casefold, reverse=self._reverse_)
        else:
            return False
        return True

    def get_data_by_request(self, dirs_list, local_system_file_path=None, orderby_kind=None, orderby_direction=None,
                            orderby_name=None) -> FileSystemHelperResponse:

        if not self.set_local_system_file_path(local_system_file_path) \
                or not self.set_file_order_by(orderby_kind) \
                or not self.set_sort_order(orderby_direction):
            # print(self.set_local_system_file_path(local_system_file_path))
            # print(self.set_file_order_by(orderby_kind))
            # print(self.set_sort_order(orderby_direction))
            return FileSystemHelperResponse.NOT_FOUND

        self.set_filtering_string(orderby_name)
        self.get_filter_dict_by_string(dirs_list)
        self.get_sort_dict(dirs_list)
        return FileSystemHelperResponse.SUCCESS

    def get_json_from_list(self, dirs_list):
        d = {}
        if os.path.isdir(self._local_system_file_path_):
            d['isDirectory'] = "True"
            d['files'] = []
        else:
            d['isDirectory'] = "True"
            d['files'] = dirs_list
            return d
        for name in dirs_list:
            path = os.path.join(self._local_system_file_path_, name)
            if os.path.isdir(path):
                d['files'].append(name+'/')
            else:
                d['files'].append(name)
        return d


def get_binary_data_from_path(path_name):
    if not check_file_is_existed(path_name):
        return None
    with open(path_name, 'rb') as f:
        return f.read()


def check_post_is_allowed(file_path):
    dir_name = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    return (len(file_name.split('.')) > 0 and not check_file_is_existed(file_path)
            and is_directory(dir_name)
            and filename_is_valid(file_name))


def remove_file(file_path):
    os.remove(file_path)
    return FileSystemHelperResponse.SUCCESS


def write_binary_to_file(file_path, binary_data):

    with open(file_path, "wb+") as binary_file:
        binary_file.write(binary_data)

    return FileSystemHelperResponse.SUCCESS


def filename_is_valid(file_name) -> bool:
    name, extension = file_name.split('.')
    with app.app_context():
        return extension in app.config['VALID_FILE_EXTENSION']


def check_file_is_existed(path_name) -> bool:
    print(f"path_name: {path_name} : {os.path.isdir(path_name)}")
    return os.path.isfile(path_name)


def give_relative_return_abs_path(relative_path):
    return os.path.join(os.getcwd(), relative_path)


def is_directory(directory_path) -> bool:
    return os.path.isdir(directory_path)


if __name__ == '__main__':
    helper = FileSystemHelper()
    # dirs_list = []
    # code = helper.get_data_by_request(dirs_list, 'file', orderby_kind='size', orderby_direction='Ascending', orderby_name='*')
    # # print(os.getcwd())
    # # print(code)
    # print(dirs_list)
    # ret_dirs = helper.get_json_from_list(dirs_list)
    # print(ret_dirs)
    # print(json.dumps(ret_dirs))
    # data = bytes()
    # ret = helper.get_binary_data_from_path("./file/abc.txt", data)
    # print(data)

    filename_is_valid("./abcdefg.aat")

    # app = create_app()
    # with app.app_context():
    #     extension = app.config['VALID_FILE_EXTENSION']
    # print(extension)
