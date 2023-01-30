import requests
import pytest
import lingua


@pytest.fixture
def client():
    """Setup reusable testing client config"""
    client = lingua.Client('llm.cluster.local', 3001, 'test_auth_key')
    return client

@pytest.mark.skip(reason="VPN barrier")
def test_ping():
    "Verify the existance of Lingua server"
    server_url = "http://llm.cluster.local:3001/"
    assert requests.get(server_url).ok, "Server cannot be reached"

@pytest.mark.skip(reason="WIP")
def test_ping(client):
    "Verify the text generation of a sample LLM"
    opt_model = client.load_model("OPT")
    text_gen = opt_model.generate_text("What is the answer to life, the universe, and everything?", max_tokens=5, top_p=3, temperature=0.5)
    assert text_gen.text

    



