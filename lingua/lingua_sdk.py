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
from enum import Enum

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
            model_instance_response['model_name'],
            model_instance_response['id'],
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
        body = {"text": text, 'generation_args': generation_args}

        response = utils.post(url, body, auth_key=self.auth_key)

        return response


class ModelInstanceState(Enum):
    """The state of a model instance"""
    LAUNCHING = 0
    LOADING = 1
    ACTIVE = 2
    FAILED = 3
    COMPLETED = 4


class Model():

    def __init__(self, model_name: str, model_instance_id: str, session: GatewaySession):
        """ Initializes a model instance

        :param client: (Client) Lingua client that this model belongs to
        :param model_name: (str): The name of the model
        """

        self.name = model_name
        self.id = model_instance_id
        self._session = session

    @property
    def state(self):
        return ModelInstanceState(self._session.get_model_instance(self.id)['state'])

    def is_active(self):
        """ Checks if the model instance is active"""
        return self.state == ModelInstanceState.ACTIVE

    def generate(self, prompt: str, generation_args: Dict = {}):
        """ Generates text from the model instance

        :param text: (str) The text to generate from
        :param kwargs: (dict) Additional arguments to pass to the model
        """
        
        #TODO: Add validation for generation args

        return self._session.generate(self.id, prompt, generation_args)

    @cached_property
    def module_names(self):
        return self._session.get_model_instance(self.id)['module_names']


# @dataclass
# class Model():

#     def __init__(self, client: Client, model_name: str):
#         """ Initializes a model instance

#         :param client: (Client) Lingua client that this model belongs to
#         :param model_name: (str): The name of the model
#         """

#         self.client = client
#         self.model_name = model_name
        
#         self.base_addr = f"http://{self.client.gateway_host}:{self.client.gateway_port}/"
#         self.create_addr = partial(urljoin, self.base_addr)
#         self.model_base_addr = f"http://{self.client.gateway_host}:{self.client.gateway_port}/models/{self.model_name}/"
#         self.model_create_addr = partial(urljoin, self.model_base_addr)


#     def verify_request(self):
#         # Make sure the token is still valid
#         try:
#             post(self.create_addr("verify_token"), {}, self.client.auth_key)
#         except:
#             print("Your access token is invalid or has expired. Please log in again.")
#             self.client.authenticate()


#     def generate_text(self, prompt, **gen_kwargs):
#         """Generates a string of text based on a prompt
        
#         :param prompt: (str) The prompt to use for generation
#         :param gen_kwargs: (dict) Keyword arguments to pass to the model's generate function
#         """


#         self.verify_request()

#         """TODO: should support batching"""
#         model_generate_addr = urljoin(self.model_base_addr, "generate_text")
#         generate_configs = {}
#         generate_configs['prompt']= prompt
#         generate_configs.update(gen_kwargs)
#         generate_configs['use_grad'] = torch.is_grad_enabled()

#         parameters= gen_kwargs.keys()

#         generate_configs['max-tokens'] = generate_configs.pop('max_tokens') if 'max_tokens' in parameters else None
#         generate_configs['top-k'] = generate_configs.pop('top_k') if 'top_k' in parameters else None
#         generate_configs['top-p'] = generate_configs.pop('top_p') if 'top_p' in parameters else None
#         generate_configs['num_return_sequences'] = generate_configs.pop('num_sequences') if 'num_sequences' in parameters else None
#         generate_configs['repetition_penalty'] = generate_configs.pop('rep_penalty') if 'rep_penalty' in parameters else None

#         print(f"Submission: {generate_configs}")
#         generation = post(model_generate_addr, generate_configs, self.client.auth_key)
#         GenerationObj = namedtuple('GenObj', generation.keys())
#         results = GenerationObj(**generation)
#         print(f"Success:\n{prompt} {results.text}")
#         return results


    # @cached_property
    # def module_names(self):
    #     """Returns a list of all module names available to this model"""
    #     self.verify_request()
    #     return get(self.model_create_addr("module_names"))


    # @cached_property
    # def parameter_names(self):
    #     """Returns a list of all parameter names available to this model"""
    #     self.verify_request()
    #     return get(self.model_create_addr("parameter_names"))


    # @cached_property
    # def probe_points(self):
    #     """(not implemented) Returns a list of all probe points available to this model"""
    #     self.verify_request()
    #     return get(self.model_create_addr("probe_points"))


    # def get_parameters(self, *names):
    #     """(not implemented) Returns a list of all parameters available to this model"""
    #     self.verify_request()
    #     return post(self.model_create_addr("get_parameters"), names)


    # def encode(self, prompts, /, return_tensors="pt", **tokenizer_kwargs):
    #     tokenizer_kwargs.setdefault("return_tensors", return_tensors)
    #     tokenizer_kwargs.setdefault("padding", True)

    #     return post(
    #         self.model_create_addr("encode"),
    #         {"prompts": prompts, "tokenizer_kwargs": tokenizer_kwargs,},
    #     )
