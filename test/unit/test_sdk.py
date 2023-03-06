import lingua
import sys

# Verifies the posted data is echoed correctly
def test_post():
    """Verify post function"""
    response = lingua.utils.post("https://httpbin.org/post", "test post data")
    assert response['data'] == 'test post data'

def test_get():
    """Verify get function"""
    response = lingua.utils.get("http://ip.jsontest.com")
    assert response
