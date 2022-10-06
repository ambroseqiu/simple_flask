import requests
import pytest, os, shutil


def remove_file_without_folder(folder_name):
    # print(f'clean file system before uni test: {folder_name}')
    for file_name in os.listdir(folder_name):
        path = os.path.join(folder_name,file_name)
        if os.path.isdir(path):
            remove_file_without_folder(path)
        elif os.path.isfile(path):
            print(path)
            os.remove(path)

@pytest.fixture()
def request_info():
    folder_name = os.path.join(os.path.dirname(__file__), "file")
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)
    remove_file_without_folder(folder_name)
    yield ServerInfo()


class ServerInfo:
    server_url = "http://flask_local_server:5000"
    # server_url = "http://172.19.0.2:5000"
    local_system_file_path = "file"
    query = ""

    def set_request_data_path(self, test_file_path):
        self.local_system_file_path = os.path.join(self.local_system_file_path, test_file_path)

    def get_request_api_rul(self):
        return os.path.join(self.server_url, self.local_system_file_path, self.query)


class TestAPI:

    @staticmethod
    def create_request_file(file_name):
        curr_dir = os.path.dirname(__file__)
        file_path = os.path.join(curr_dir, "test_file", file_name)
        # print(f'file path: {file_path}')
        return {"file" : (file_name, open(file_path, "rb"))}

    @staticmethod
    def create_test_file(test_file_path):
        curr_dir = os.path.dirname(__file__)
        file_path = os.path.join(curr_dir, "file", test_file_path)
        test_file_path = os.path.join(curr_dir, "test_file", test_file_path)
        shutil.copy2(test_file_path,file_path)


    def test_1_get_request_return_200(self, request_info):
        api_url = request_info.get_request_api_rul()
        response = requests.get(api_url)
        assert response.status_code == 200

    def test_post_newfile_return_200(self, request_info):
        data = "key1=value1&key2=value2"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        request_info.set_request_data_path("newfile.json")
        api_url = request_info.get_request_api_rul()
        response = requests.post(api_url, data=data, headers=headers)
        assert response.status_code == 200

    @pytest.mark.parametrize("test_file_path,expected", [("test_file.txt", 200), ("test_file.json", 200)])
    def test_2_post_valid_request_return_200(self, request_info, test_file_path, expected):
        request_info.set_request_data_path(test_file_path)
        api_url = request_info.get_request_api_rul()
        files = TestAPI.create_request_file(test_file_path)
        response = requests.post(api_url, files=files)
        # print(requests.Request('POST', api_url, files=files).prepare().body.decode('utf8'))
        assert response.status_code == expected

    @pytest.mark.parametrize("test_file_path,expected", [("test_file.txt", 200), ("test_file.json", 200)])
    def test_3_patch_valid_request_return_200(self, request_info, test_file_path, expected):
        TestAPI.create_test_file(test_file_path)
        request_info.set_request_data_path(test_file_path)
        api_url = request_info.get_request_api_rul()
        files = TestAPI.create_request_file(test_file_path)
        response = requests.patch(api_url, files=files)
        assert response.status_code == expected

    @pytest.mark.parametrize("test_file_path,expected", [("test_file.txt", 200), ("test_file.json", 200)])
    def test_4_delete_valid_request_return_200(self, request_info, test_file_path, expected):
        TestAPI.create_test_file(test_file_path)
        request_info.set_request_data_path(test_file_path)
        api_url = request_info.get_request_api_rul()
        response = requests.delete(api_url)
        assert response.status_code == expected