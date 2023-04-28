# Happy path test for on-prem
import pytest
import os
import socket
from pathlib import Path
import time
import kscope


def authenticate_user():
    """A setup to authenticate the user to a client or write dummy data if testing on CI/CD workflows"""
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


hostname = socket.gethostname()

authenticate_user()


@pytest.mark.skipif(hostname != "llm", reason="tests for on-premise only")
class TestSystem:
    # Authenticate before running to ensure service is functional end-to-end

    @pytest.fixture
    def client_config(self):
        client = kscope.Client(
            gateway_host="localhost", gateway_port=4001
        )  # Leverage staging environment
        return client

    @pytest.fixture
    def model(self, client_config):
        _llm = client_config.load_model("OPT-6.7B")
        return _llm

    def test_get_model(self, client_config):
        assert len(client_config.models) >= 1

    def test_load_model(self, model):
        timeout = time.time() + 60 * 5  # Period of 5 minutes
        while model.state != "ACTIVE" and time.time() < timeout:
            time.sleep(1)
            print("Loading OPT-6.7B")
        assert model.state == "ACTIVE"

    def test_text_gen_length(self, model):
        text_gen = model.generate(
            "What is AI?", {"max_tokens": 10, "top_p": 2, "temperature": 0.4}
        )
        assert len(text_gen.generation["text"][0]) > 1 and len(
            text_gen.generation["logprobs"][0]
        ) == len(text_gen.generation["tokens"][0])

    # Simple ISP tests
    def test_text_gen_nominal(self, model):
        text_gen = model.generate(
            "What is AI?", {"max_tokens": 10, "top_p": 2, "temperature": 0.4}
        )
        assert (
            type(text_gen.generation["text"][0]) == str
            and type(text_gen.generation["logprobs"][0][0]) == float
        )

    def test_text_gen_lower_bound(self, model):
        text_gen = model.generate(
            "What is AI?", {"max_tokens": 0, "top_p": 0, "temperature": 0.0}
        )
        assert (
            len(text_gen.generation["text"][0]) == 0
            and len(text_gen.generation["logprobs"][0]) == 0
        )

    def test_text_gen_upper_bound(self, model):
        text_gen = model.generate(
            "What is AI?",
            {"max_tokens": 60, "top_p": 10.0, "temperature": 10.0, "n": 2},
        )
        assert text_gen.generation["text"]
        assert text_gen.generation["logprobs"]

    def test_text_gen_upper_bound(self, model):
        assert len(model.module_names) > 1

    def test_activation_retireval(self, model):
        requested_activations = ["decoder.layers.0"]
        activations = model.get_activations("Inference", requested_activations)
        assert len(activations) > 1
