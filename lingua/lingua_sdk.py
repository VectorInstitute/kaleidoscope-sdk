from collections import namedtuple
from dataclasses import dataclass, field
from functools import cached_property, partial
from getpass import getpass
import json
import requests
from pathlib import Path
import sys
import time
import torch
from typing import Dict
from urllib.parse import urljoin
from enum import Enum, auto

from .hooks import TestForwardHook
import utils

JWT_TOKEN_FILE = Path(Path.home() / '.lingua.jwt')


class Client:

    def __init__(self, gateway_host: str, gateway_port: int, auth_key: str = None, verbose: bool = False):
        """ Initializes the Lingua client which faciliates communication with the gateway service

        :param gateway_host: The host of the gateway service
        :param gateway_port: The port of the gateway service
        :param auth_key:  The authentication key for the gateway service
        :param verbose: Print debugging information
        """

        if not auth_key:
            if JWT_TOKEN_FILE.exists():
                with open(JWT_TOKEN_FILE, "r") as f:
                    auth_key = f.read()
            else:
                try:
                    print("You must authenticate with your LDAP credentials to use the Lingua service")
                    auth_key = self.authenticate()
                except Exception as err:
                    print(err)
                    sys.exit(1)

        self.verbose = verbose
        self._session = GatewaySession(gateway_host, gateway_port, auth_key)

        if self.verbose:
            print(f"Available models: {self.models} \nActive models instances: {self.model_instances}")


    def authenticate(self):
        """Authenticates this user with the gateway service via LDAP"""
        num_tries = 0
        while num_tries < 3:
            username = input("Username: ")
            password = getpass()
            result = requests.post(self.create_addr("authenticate"), auth=(username, password))
            if result.status_code == 200:
                print("Login successful.")
                auth_key = json.loads(result.text)['token']
                with open(JWT_TOKEN_FILE, "w") as f:
                    f.write(auth_key)
                return auth_key
            else:
                print("Authentication failed.")
                num_tries += 1

        raise Exception("Too many failed login attempts.")

    @cached_property
    def models(self):
        return self._session.get_models()

    @property
    def model_instances(self):
        return self._session.get_model_instances()

    def load_model(self, model_name: str):
        """Loads a model from the gateway service
        
        :param model_name: (str) The name of the model to load
        """

        model_instance_response = self._session.create_model_instance(model_name)

        model = Model(
            model_instance_response['id'],
            model_instance_response['name'],
            self._session
        )

        while not model.is_active():
            time.sleep(2)
        
        return model

class GatewaySession:
    """A session for a model instance"""
    
    def __init__(self, gateway_host: str, gateway_port: int, auth_key: str):
        self.gateway_host = gateway_host
        self.gateway_port = gateway_port
        self.auth_key = auth_key

        self.base_addr = f"http://{self.gateway_host}:{self.gateway_port}/"
        self.create_addr = partial(urljoin, self.base_addr)


    def create_model_instance(self, model_name: str):
        url = self.create_addr("models/instances")
        body = {"model_name": model_name}
        response = utils.post(url, body, auth_key=self.auth_key)

        return response

    def get_model_instance(self, model_instance_id: str):
        url = self.create_addr(f"models/instances/{model_instance_id}")

        response = utils.get(url, auth_key=self.auth_key)
        return response

    def generate(self, model_instance_id: str, prompt: str, generation_args: Dict):
        """Generates text from the model instance"""

        url = self.create_addr(f"models/instances/{model_instance_id}/generate")
        body = {"prompt": prompt, 'generation_args': generation_args}

        response = utils.post(url, body, auth_key=self.auth_key)

        return response


class Model():

    def __init__(self, model_instance_id: str, model_name: str, session: GatewaySession):
        """ Initializes a model instance

        :param client: (Client) Lingua client that this model belongs to
        :param model_name: (str): The name of the model
        """

        self.name = model_name
        self.id = model_instance_id
        self._session = session

    @property
    def state(self):
        return self._session.get_model_instance(self.id)['state']

    def is_active(self):
        """ Checks if the model instance is active"""
        return self.state == 'ACTIVE'

    def generate(self, prompt: str, generation_args: Dict = {}):
        """ Generates text from the model instance

        :param text: (str) The text to generate from
        :param kwargs: (dict) Additional arguments to pass to the model
        """

        generation_response = self._session.generate(self.id, prompt, generation_args)

        GenerationObj = namedtuple('GenObj', generation_response.keys())

        return GenerationObj(**generation_response)

    @cached_property
    def module_names(self):
        return self._session.get_model_instance(self.id)['module_names']