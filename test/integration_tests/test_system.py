# Happy path test for on-prem
import pytest
import os
import socket
from pathlib import Path
import time

hostname = socket.gethostname()

# A setup method to initialize the Client class in kaleidoscope_sdk.py
JWT_TOKEN_FILE = Path(Path.home() / ".kaleidoscope.jwt")


def remove_jwt_system_file():
    if JWT_TOKEN_FILE.exists():
        os.remove(JWT_TOKEN_FILE)


@pytest.mark.skipif(hostname != "llm", reason="tests for on-premise only")
class TestSystem:
    # Authenticate before running to ensure service is functional end-to-end
    import kscope

    client = kscope.Client(
        gateway_host="localhost", gateway_port=5001
    )  # Leverage staging environment

    client.authenticate()

    @pytest.fixture
    def model(self):
        _llm = self.client.load_model("OPT-6.7B")
        return _llm

    def test_get_model(self):
        assert len(self.client.models) >= 1

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
