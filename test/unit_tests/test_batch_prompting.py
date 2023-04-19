"""Module for testing batch prompt"""
import socket
import pytest
import kscope

hostname = socket.gethostname()


@pytest.mark.skipif(hostname != "llm", reason="tests for on-premise only")
class TestBatchPrompting:
    """A class for testing batch prompting on-prem"""

    _host = "llm.cluster.local"
    _port = 4001
    model_name = "OPT-175B"  # "OPT-6.7B"
    _client = kscope.Client(gateway_host=_host, gateway_port=_port)
    _model = _client.load_model(model_name)
    _requested_activation = ["decoder.layers.30.fc1"]

    def test_generation_single_prompt_str(self):
        """Generate for single prompt"""
        prompt = "What is this"
        response = self._model.generate(prompt)
        assert isinstance(
            response.generation["text"], list
        ), f'Expected type list, found {type(response.generation["text"])}'
        assert (
            len(response.generation["text"]) == 1
        ), f'Expected 1 generation, found {len(response.generation["text"])}'

    def test_generation_single_prompt_list(self):
        """Generate for prompt list"""
        prompt = ["What is this"]
        response = self._model.generate(prompt)
        assert isinstance(
            response.generation["text"], list
        ), f'Expected type list, found {type(response.generation["text"])}'
        assert (
            len(response.generation["text"]) == 1
        ), f'Expected 1 generation, found {len(response.generation["text"])}'

    def test_generation_multiple_prompts(self):
        """Generate for multiple prompt inputs"""
        prompts = ["What is this", "Who is that", "When should we"]
        response = self._model.generate(prompts)
        assert isinstance(
            response.generation["text"], list
        ), f'Expected type list, found {type(response.generation["text"])}'
        assert len(response.generation["text"]) == len(
            prompts
        ), "Length mismatch between # input prompts and # output generations"

    def test_activation_single_prompt_str(self):
        """Generate activations for single prompt"""
        prompt = "What is this"
        response = self._model.get_activations(prompt, self._requested_activation)
        assert isinstance(
            response.activations, list
        ), f"Expected type list, found {type(response.activations)}"
        assert (
            len(response.activations) == 1
        ), f"Expected 1 set of activations, found {len(response.activations)}"

    def test_activation_single_prompt_list(self):
        """Generate activations for prompt list"""
        prompt = ["What is this"]
        response = self._model.get_activations(prompt, self._requested_activation)
        assert isinstance(
            response.activations, list
        ), f"Expected type list, found {type(response.activations)}"
        assert (
            len(response.activations) == 1
        ), f"Expected 1 set of activations, found {len(response.activations)}"

    def test_activation_multiple_prompts(self):
        """Generate activations for multiple prompts"""
        prompts = ["What is this", "Who is that", "When should we"]
        response = self._model.get_activations(prompts, self._requested_activation)
        assert isinstance(
            response.activations, list
        ), f"Expected type list, found {type(response.activations)}"
        assert len(response.activations) == len(
            prompts
        ), "Length mismatch between # input prompts and # output set of activations"
