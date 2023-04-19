# Happy path test for on-prem
import kscope
import pytest
import os
import socket


@pytest.mark.skipif(hostname != "llm", reason="tests for on-premise only")
class TestSystem:

    _llm = None

    def __init__(self):
        self.client = kscope.Client(gateway_host="localhost", gateway_port=3001)

    def test_get_model():
        assert len(client.models) >= 1

    @pytest.mark.timeout(120)
    def test_load_model():
        # Use 6.7B for testing purposes
        _llm = self.client.load_model("OPT-6.7B")
        while _llm.state != "ACTIVE":
            time.sleep(1)
        assert _llm.state == "ACTIVE"

    def test_text_gen_length():
        text_gen = _llm.generate(
            "What is AI?", {"max_tokens": 10, "top_p": 2, "temperature": 0.4}
        )
        assert len(text_gen.generation["text"][0]) > 1 and len(
            text_gen.generation["logprobs"][0]
        ) == len(text_gen.generation["tokens"][0])

    def test_text_gen_nominal():
        text_gen = _llm.generate(
            "What is AI?", {"max_tokens": 10, "top_p": 2, "temperature": 0.4}
        )
        assert (
            type(text_gen.generation["text"][0]) == str
            and type(text_gen.generation["logprobs"][0][0]) == float
        )

    def test_text_gen_lower_bound():
        text_gen = _llm.generate(
            "What is AI?", {"max_tokens": 0, "top_p": 0, "temperature": 0.0}
        )
        assert (
            len(text_gen.generation["text"][0]) == 0
            and len(text_gen.generation["logprobs"][0]) == 0
        )

    def test_text_gen_upper_bound():
        text_gen = _llm.generate(
            "What is AI?",
            {"max_tokens": 60, "top_p": 10.0, "temperature": 10.0, "n": 2},
        )
        assert text_gen.generation["text"]
        assert text_gen.generation["logprobs"]

    def test_text_gen_upper_bound():
        assert len(_llm.module_names) > 1

    def test_activation_retireval():
        requested_activations = ["decoder.layers.0"]
        activations = _llm.get_activations("Inference", requested_activations)
        assert len(activations) > 1 and activations
