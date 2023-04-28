import kscope
from kscope import GatewaySession, Client
import pytest
from pathlib import Path
import os
import socket

hostname = socket.gethostname()

# A setup method to initialize the Client class in kaleidoscope_sdk.py
JWT_TOKEN_FILE = Path(Path.home() / ".kaleidoscope.jwt")

if not JWT_TOKEN_FILE.exists():
    if hostname == "llm":
        client = kscope.Client(gateway_host="localhost", gateway_port=4001)
        client.authenticate()
    else:
        try:
            f = open(JWT_TOKEN_FILE, "w")
            f.write("Sample auth")
        finally:
            f.close()


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


@pytest.mark.skipif(hostname != "llm", reason="tests for on-premise only")
class TestSDKUtils:
    @pytest.fixture
    def session(self):
        """Setup reusable client testing config"""
        session = GatewaySession("localhost", 4001, "test_auth_key")
        return session

    # def test_client_null_input(self):
    #     """Verify instantiated client with no inputs"""
    #     with pytest.raises(SystemExit) as pytest_wrapped_e:
    #         client = kscope.Client(None, None)
    #     assert pytest_wrapped_e.type == SystemExit
    #     assert pytest_wrapped_e.value.code == 1

    def test_client_host_input(self, session):
        """Verify instantiated client host"""
        assert session.gateway_host == "localhost"

    def test_client_port_input(self, session):
        """Verify instantiated client port"""
        assert session.gateway_port == 4001

    def test_client_auth_input(self, session):
        """Verify authentication with input and non-existing JWT file"""
        if JWT_TOKEN_FILE.exists():
            os.remove(JWT_TOKEN_FILE)
        assert session.auth_key == "test_auth_key"

    def test_client_auth_existing_input(self):
        """Verify authentication from existing JWT file without input"""
        session = GatewaySession("localhost", 4001, "test_auth")
        if JWT_TOKEN_FILE.exists():
            os.remove(JWT_TOKEN_FILE)
        try:
            with open(JWT_TOKEN_FILE, "w") as f:
                f.write("sample_auth_key")
        except Exception as e:
            print(f"Error occurred while writing to file: {str(e)}")
        assert session.auth_key != "sample_auth_key"

    def test_client_base_address(self, session):
        """Verify client base address"""
        assert session.base_addr == "http://localhost:4001/"

    def test_client_get_models(self, session):
        """Verify client model instances data structure"""
        assert type(session.get_models()) == list

    def test_client_load_model(self):
        """Verify unacceptable model load"""
        with pytest.raises(ValueError):
            session = Client("localhost", 4001)
            session.load_model("test")

    # def test_client_load_model(self):
    #     """Verify activate OPT model base address"""
    #     session = Client("localhost", 4001)
    #     session.authenticate() # Leverage valid credentials
    #     opt_model = session.load_model("OPT")
    #     assert opt_model.base_addr == "http://localhost:4001/models/OPT/"
