import requests
import pytest


@pytest.mark.skip(reason="no way of currently testing this")
def test_ping():
    "Verify the existance of Lingua server"
    server_url = "http://llm.cluster.local:3001/"
    assert requests.get(server_url).ok
