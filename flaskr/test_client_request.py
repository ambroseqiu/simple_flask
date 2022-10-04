import requests
import pytest, os


@pytest.fixture()
def request_info():
    print("====setup===")
    yield ServerInfo()
    print("===teardown===")





class ServerInfo:
    server_url = "http://flask_local_server:5000"
    local_system_file_path = "file"
    query = ""

    def set_request_data_path(self, test_file_path):
        self.local_system_file_path = os.path.join(self.local_system_file_path, test_file_path)

    def get_request_api_rul(self):
        return os.path.join(self.server_url, self.local_system_file_path, self.query)


class TestAPI:

    @staticmethod
    def create_file(file_name):
        file_path = os.path.join("./test_file", file_name)
        return open(file_path, "wb")

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
        assert api_url == "http://flask_local_server:5000/file/newfile.json/"

    @pytest.mark.parametrize("test_file_path,expected", [("text.txt", 200), ("img.png", 200), ("data.json", 200),
                                                         ("subdir/one.txt", 200)])
    def test_2_post_valid_request_return_200(self, request_info, test_file_path, expected):
        request_info.set_request_data_path(test_file_path)
        api_url = request_info.get_request_api_rul()
        response = requests.post(api_url, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        assert response.status_code == expected

    @pytest.mark.parametrize("test_file_path,expected", [("text.txt", 200), ("img.png", 200), ("data.json", 200)])
    def test_3_patch_valid_request_return_200(self, request_info, test_file_path, expected):
        request_info.set_request_data_path(test_file_path)
        api_url = request_info.get_request_api_rul()
        response = requests.patch(api_url)
        assert response.status_code == expected




# test_ = TestAPI()
# test_.test_1_get_request_return_200()



# r = requests.get('http://127.0.0.1:5000/file/')

# if r.status_code == 200:
#     print(r.text)


# def test_request_local_host_response_200():
#     r = requests.get('http://127.0.0.1:5000/file/')
#     assert r.status_code == 200