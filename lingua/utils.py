"""
TODOS:
    1. eventually we need to seperate this out to client and server utils
"""
import logging

import requests

logger = logging.getLogger(__name__)

def check_response(resp):
    if not resp.ok:
        raise ValueError(
            "request to {} not sucessful, error code: {}".format(
                resp.url,
                resp.status_code
            )
        )
    logger.debug("addr %s response code %s", resp.url, resp.status_code)

def get(addr):
    resp = requests.get(addr)
    check_response(resp)
    return resp.json()

def post(addr, obj, auth_key=None):
    if auth_key:
        resp = requests.post(addr, data=obj, headers={'Authorization': 'Bearer '+auth_key})
    else:
        resp = requests.post(addr, data=obj)
    check_response(resp)
    return resp.json()
