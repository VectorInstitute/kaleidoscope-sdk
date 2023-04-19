"""
TODOS:
    1. eventually we need to seperate this out to client and server utils
"""
import logging
import pickle
import codecs
import requests

logger = logging.getLogger(__name__)


def decode_str(obj_in_str):
    """Decodes passed object using pickle"""
    return pickle.loads(codecs.decode(obj_in_str.encode("utf-8"), "base64"))


def check_response(resp):
    """Decodes response status in an interpretable way"""
    if not resp.ok:
        if resp.status_code == 422:
            raise ValueError(
                f"Request to {resp.url} not sucessful, Error Code: {resp.status_code}, \
                please check your auth key"
            )
        elif resp.status_code == 400:
            raise ValueError(
                f"Request to {resp.url} not sucessful, Error Code: {resp.status_code}, \
                please check your request body"
            )
        raise ValueError(f"Request to {resp.url} not sucessful, Error Code: {resp.status_code}")
    logger.debug("addr %s response code %s", resp.url, resp.status_code)


def get(addr, auth_key=None, headers=None):
    """Retrieves a get request and returns any json data if provided"""
    if headers is None:
        headers = {}
    if auth_key:
        headers["Authorization"] = f"Bearer {auth_key}"

    resp = requests.get(addr, headers=headers, timeout=300)
    check_response(resp)

    return resp.json()


def post(addr, body, auth_key=None, headers=None):
    """Sends a post request and returns any json data if provided"""
    if headers is None:
        headers = {}
    if auth_key:
        headers["Authorization"] = f"Bearer {auth_key}"

    resp = requests.post(addr, json=body, headers=headers, timeout=300)
    check_response(resp)

    return resp.json()
