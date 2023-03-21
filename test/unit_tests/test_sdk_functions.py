import kscope
import pytest
from pathlib import Path
import os

# A setup method to initialize the Client class in kaleidoscope_sdk.py
JWT_TOKEN_FILE = Path(Path.home() / ".kaleidoscope.jwt")


def remove_jwt_system_file():
    if JWT_TOKEN_FILE.exists():
        os.remove(JWT_TOKEN_FILE)


@pytest.fixture
def client():
    """Setup reusable client testing config"""
    client = kaleidoscope.Client("llm.cluster.local", 3001, "test_auth_key")
    return client


# Verifies the posted data is echoed correctly
def test_post():
    test_data = "test post data"
    response = kscope.utils.post("https://httpbin.org/post", test_data)
    assert response


def test_get():
    response = kscope.utils.get("http://ip.jsontest.com")
    assert response


def test_check_response():
    with pytest.raises(ValueError):
        kscope.utils.get("https://httpbin.org/status/404")


@pytest.mark.skip(reason="tested on-premise")
def test_client_null_input():
    """Verify instantiated client with no inputs"""
    with pytest.raises(Exception):
        client = kaleidoscope.Client(None, None)


@pytest.mark.skip(reason="tested on-premise")
def test_client_host_input(client):
    """Verify instantiated client host"""
    assert client.gateway_host == "llm.cluster.local"


@pytest.mark.skip(reason="tested on-premise")
def test_client_port_input(client):
    """Verify instantiated client port"""
    assert client.gateway_port == 3001


@pytest.mark.skip(reason="tested on-premise")
def test_client_auth_input(client):
    """Verify authentication with input and non-existing JWT file"""
    remove_jwt_system_file()
    assert client.auth_key == "test_auth_key"


@pytest.mark.skip(reason="tested on-premise")
def test_client_auth_existing_input():
    """Verify authentication from existing JWT file without input"""
    remove_jwt_system_file()
    with open(JWT_TOKEN_FILE, "w") as f:
        f.write("sample_auth_key")
    client = kaleidoscope.Client("llm.cluster.local", 3001)
    assert client.auth_key == "sample_auth_key"


@pytest.mark.skip(reason="tested on-premise")
# def test_client_auth_no_input(monkeypatch):
#   """TODO: replicate vector credential input test"""
#     remove_jwt_system_file()
#     inputs = iter(['username', 'password'])
#     with pytest.raises(SystemExit):
#         client = kaleidoscope.Client('llm.cluster.local', 3001)

# def test_client_authenticate_fail()
#   """TODO: expect system exit after user and password input failures for 3 iterations"""


@pytest.mark.skip(reason="tested on-premise")
def test_client_base_address(client):
    """Verify client base address"""
    assert client.base_addr == "http://llm.cluster.local:3001/"


@pytest.mark.skip(reason="tested on-premise")
def test_client_get_models(client):
    """Verify client model instances data structure"""
    assert type(client.get_models()) == dict


@pytest.mark.skip(reason="tested on-premise")
def test_client_load_model(client):
    """Verify unacceptable model load"""
    with pytest.raises(ValueError):
        client.load_model("test")


# def test_client_load_model(client):
#     """Verify activate OPT model base address"""
#     opt_model = client.load_model("OPT")
#     assert opt_model.base_addr == "http://llm.cluster.local:3001/models/OPT/"

# Verifies the posted data is echoed correctly
@pytest.mark.skip(reason="tested on-premise")
def test_post():
    """Verify post function"""
    response = kaleidoscope.utils.post("https://httpbin.org/post", "test post data")
    assert response["data"] == "test post data"


@pytest.mark.skip(reason="tested on-premise")
def test_get():
    """Verify get function"""
    response = kaleidoscope.utils.get("http://ip.jsontest.com")
    assert response
