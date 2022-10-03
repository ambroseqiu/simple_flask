import requests

r = requests.get('http://127.0.0.1:5000/file/')

if r.status_code == 200:
    print(r.text)


def test_request_local_host_response_200():
    r = requests.get('http://127.0.0.1:5000/file/')
    assert r.status_code == 200