import lingua
import pytest

# Verifies the posted data is echoed correctly
def test_post():
    response = lingua.utils.post("https://httpbin.org/post", "test post data")
    assert response['data'] == "test post data"

def test_get():
    response = lingua.utils.get("http://ip.jsontest.com")
    assert response

def test_check_response():
    with pytest.raises(ValueError):
        lingua.utils.get("https://httpbin.org/status/404")
