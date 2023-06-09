import pytest
import kscope
import socket
from pathlib import Path
import os

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
class TestBatchPrompting:
    @pytest.fixture
    def batch_prompting_config(self):
        _host = "localhost"
        _port = 4001
        model_name = "OPT-175B"  # "OPT-6.7B"
        _client = kscope.Client(gateway_host=_host, gateway_port=_port)
        _model = _client.load_model(model_name)
        _requested_activation = ["decoder.layers.30.fc1"]
        return {
            "_host": _host,
            "_port": _port,
            "model_name": model_name,
            "_client": _client,
            "_model": _model,
            "_requested_activation": _requested_activation,
        }

    def test_generation_single_prompt_str(self, batch_prompting_config):
        prompt = "What is this"
        response = batch_prompting_config["_model"].generate(prompt)
        assert isinstance(
            response.generation["text"], list
        ), f'Expected type list, found {type(response.generation["text"])}'
        assert (
            len(response.generation["text"]) == 1
        ), f'Expected 1 generation, found {len(response.generation["text"])}'

    def test_generation_single_prompt_list(self, batch_prompting_config):
        prompt = ["What is this"]
        response = batch_prompting_config["_model"].generate(prompt)
        assert isinstance(
            response.generation["text"], list
        ), f'Expected type list, found {type(response.generation["text"])}'
        assert (
            len(response.generation["text"]) == 1
        ), f'Expected 1 generation, found {len(response.generation["text"])}'

    def test_generation_multiple_prompts(self, batch_prompting_config):
        prompts = ["What is this", "Who is that", "When should we"]
        response = batch_prompting_config["_model"].generate(prompts)
        assert isinstance(
            response.generation["text"], list
        ), f'Expected type list, found {type(response.generation["text"])}'
        assert len(response.generation["text"]) == len(
            prompts
        ), f"Length mismatch between # input prompts and # output generations"

    def test_activation_single_prompt_str(self, batch_prompting_config):
        prompt = "What is this"
        response = batch_prompting_config["_model"].get_activations(
            prompt, batch_prompting_config["_requested_activation"]
        )
        assert isinstance(
            response.activations, list
        ), f"Expected type list, found {type(response.activations)}"
        assert (
            len(response.activations) == 1
        ), f"Expected 1 set of activations, found {len(response.activations)}"

    def test_activation_single_prompt_list(self, batch_prompting_config):
        prompt = ["What is this"]
        response = batch_prompting_config["_model"].get_activations(
            prompt, batch_prompting_config["_requested_activation"]
        )
        assert isinstance(
            response.activations, list
        ), f"Expected type list, found {type(response.activations)}"
        assert (
            len(response.activations) == 1
        ), f"Expected 1 set of activations, found {len(response.activations)}"

    def test_activation_multiple_prompts(self, batch_prompting_config):
        prompts = ["What is this", "Who is that", "When should we"]
        response = batch_prompting_config["_model"].get_activations(
            prompts, batch_prompting_config["_requested_activation"]
        )
        assert isinstance(
            response.activations, list
        ), f"Expected type list, found {type(response.activations)}"
        assert len(response.activations) == len(
            prompts
        ), f"Length mismatch between # input prompts and # output set of activations"
