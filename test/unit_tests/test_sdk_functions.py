"""Tests for Kaleidoscope SDK utility functions"""
import os
import socket
from pathlib import Path
import pytest
import kscope

hostname = socket.gethostname()

# A setup method to initialize the Client class in kaleidoscope_sdk.py
JWT_TOKEN_FILE = Path(Path.home() / ".kaleidoscope.jwt")


def remove_jwt_system_file():
    """Removes authentication token from recognized path"""
    if JWT_TOKEN_FILE.exists():
        os.remove(JWT_TOKEN_FILE)


@pytest.fixture
def client():
    """Setup reusable client testing config"""
    kscope_client = kscope.Client("llm.cluster.local", 3001, "test_auth_key")
    return kscope_client


# Verifies the posted data is echoed correctly
def test_post():
    """Tests if kscope utils successfully posts data"""
    test_data = "test post data"
    response = kscope.utils.post("https://httpbin.org/post", test_data)
    assert response


def test_get():
    """Tests if kscope utils successfully retrieves data"""
    response = kscope.utils.get("http://ip.jsontest.com")
    assert response


def test_check_response():
    """Tests if errors are successfully handled"""
    with pytest.raises(ValueError):
        kscope.utils.get("https://httpbin.org/status/404")


@pytest.mark.skipif(hostname != "llm", reason="tests for on-premise only")
def test_client_null_input():
    """Verify instantiated client with no inputs"""
    with pytest.raises(Exception):
        kscope.Client(None, None)


@pytest.mark.skipif(hostname != "llm", reason="tests for on-premise only")
def test_client_host_input(kscope_client):
    """Verify instantiated client host"""
    assert kscope_client.gateway_host == "llm.cluster.local"


@pytest.mark.skipif(hostname != "llm", reason="tests for on-premise only")
def test_client_port_input(kscope_client):
    """Verify instantiated client port"""
    assert kscope_client.gateway_port == 3001


@pytest.mark.skipif(hostname != "llm", reason="tests for on-premise only")
def test_client_auth_input(kscope_client):
    """Verify authentication with input and non-existing JWT file"""
    remove_jwt_system_file()
    assert kscope_client.auth_key == "test_auth_key"


@pytest.mark.skipif(hostname != "llm", reason="tests for on-premise only")
def test_client_auth_existing_input():
    """Verify authentication from existing JWT file without input"""
    remove_jwt_system_file()
    with open(JWT_TOKEN_FILE, "w", encoding="utf-8") as token_file:
        token_file.write("sample_auth_key")
    kscope_client = kscope.Client("llm.cluster.local", 3001)
    assert kscope_client.auth_key == "sample_auth_key"


# @pytest.mark.skipif(hostname != "llm", reason="tests for on-premise only")
# def test_client_auth_no_input(monkeypatch):
#   """TODO: replicate vector credential input test"""
#     remove_jwt_system_file()
#     inputs = iter(['username', 'password'])
#     with pytest.raises(SystemExit):
#         client = kscope.Client('llm.cluster.local', 3001)

# def test_client_authenticate_fail()
#   """TODO: expect system exit after user and password input failures for 3 iterations"""


@pytest.mark.skipif(hostname != "llm", reason="tests for on-premise only")
def test_client_base_address(kscope_client):
    """Verify client base address"""
    assert kscope_client.base_addr == "http://llm.cluster.local:3001/"


@pytest.mark.skipif(hostname != "llm", reason="tests for on-premise only")
def test_client_get_models(kscope_client):
    """Verify client model instances data structure"""
    assert isinstance(kscope_client.get_models()) is dict


@pytest.mark.skipif(hostname != "llm", reason="tests for on-premise only")
def test_client_load_model(kscope_client):
    """Verify unacceptable model load"""
    with pytest.raises(ValueError):
        kscope_client.load_model("test")


# def test_client_load_model(kscope_client):
#     """Verify activate OPT model base address"""
#     opt_model = kscope_client.load_model("OPT")
#     assert opt_model.base_addr == "http://llm.cluster.local:3001/models/OPT/"
