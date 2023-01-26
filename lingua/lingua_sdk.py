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

from .hooks import TestForwardHook
from .utils import get, post

sys.path.append("..")

JWT_TOKEN_FILE = Path(Path.home() / '.lingua.jwt')

class Client:

    def __init__(self, gateway_host: str, gateway_port: int, auth_key: str = None):
        """ Initializes the Lingua client

        :param gateway_host: The host of the gateway service
        :param gateway_port: The port of the gateway service
        :param auth_key:  The authentication key for the gateway service
        """

        self.gateway_host = gateway_host
        self.gateway_port = gateway_port
        self.base_addr = f"http://{self.gateway_host}:{self.gateway_port}/"
        self.create_addr = partial(urljoin, self.base_addr)

        if auth_key:
            self.auth_key = auth_key
        elif JWT_TOKEN_FILE.exists():
            with open(JWT_TOKEN_FILE, "r") as f:
                self.auth_key = f.read()
        else:
            try:
                print("You must authenticate with your LDAP credentials to use the Lingua service")
                self.authenticate()
            except Exception as err:
                print(err)
                sys.exit(1)

        self.all_model_names = get(self.create_addr("models"))
        model_instances = self.get_models()
        active_model_instances = [models for models in model_instances if model_instances[models]=="Active"]
        print(f"Available models: {self.all_model_names} \nActive models instances: {active_model_instances}")


    def authenticate(self):
        """Authenticates this user with the gateway service via LDAP"""
        num_tries = 0
        while num_tries < 3:
            username = input("Username: ")
            password = getpass()
            result = requests.post(self.create_addr("authenticate"), auth=(username, password))
            if result.status_code == 200:
                print("Login successful.")
                self.auth_key = json.loads(result.text)['token']
                with open(JWT_TOKEN_FILE, "w") as f:
                    f.write(self.auth_key)
                return
            else:
                print("Authentication failed.")
                num_tries += 1

        raise Exception("Too many failed login attempts.")


    def get_models(self):
        """
        Returns a list of all models available to this client, 
        along with their active/inactive status
        """
        model_instances = get(self.create_addr("models/instances"))
        return model_instances


    def load_model(self, model_name: str):
        """Loads a model from the gateway service
        
        :param model_name: (str) The name of the model to load
        """

        if model_name not in self.all_model_names:
            raise ValueError(
                "asked for model {} but server only supports model "
                "names {}".format(model_name, self.all_model_names)
            )
        # If the model is inactive, send a request to launch it, then wait for it to start
        if self.get_models()[model_name] == "Inactive":
            print(f"Launching a model instance for {model_name}, this may take a few minutes...")
            result = post(
                self.create_addr(f"models/{model_name}/launch"), 
                {},
                auth_key=self.auth_key
            )
            while self.get_models()[model_name] == "Inactive":
                time.sleep(1)

        return Model(self, model_name)


@dataclass
class Model():

    def __init__(self, client: Client, model_name: str):
        """ Initializes a model instance

        :param client: (Client) Lingua client that this model belongs to
        :param model_name: (str): The name of the model
        """

        self.client = client
        self.model_name = model_name
        self.base_addr = f"http://{self.client.gateway_host}:{self.client.gateway_port}/"
        self.create_addr = partial(urljoin, self.base_addr)
        self.model_base_addr = f"http://{self.client.gateway_host}:{self.client.gateway_port}/models/{self.model_name}/"
        self.model_create_addr = partial(urljoin, self.model_base_addr)


    def verify_request(self):
        # Make sure the token is still valid
        try:
            post(self.create_addr("verify_token"), {}, self.client.auth_key)
        except:
            print("Your access token is invalid or has expired. Please log in again.")
            self.client.authenticate()


    def generate_text(self, prompt, **gen_kwargs):
        """Generates a string of text based on a prompt
        
        :param prompt: (str) The prompt to use for generation
        :param gen_kwargs: (dict) Keyword arguments to pass to the model's generate function
        """


        self.verify_request()

        """TODO: should support batching"""
        model_generate_addr = urljoin(self.model_base_addr, "generate_text")
        generate_configs = {}
        generate_configs['prompt']= prompt
        generate_configs.update(gen_kwargs)
        generate_configs['use_grad'] = torch.is_grad_enabled()

        parameters= gen_kwargs.keys()

        generate_configs['max-tokens'] = generate_configs.pop('max_tokens') if 'max_tokens' in parameters else None
        generate_configs['top-k'] = generate_configs.pop('top_k') if 'top_k' in parameters else None
        generate_configs['top-p'] = generate_configs.pop('top_p') if 'top_p' in parameters else None
        generate_configs['num_return_sequences'] = generate_configs.pop('num_sequences') if 'num_sequences' in parameters else None
        generate_configs['repetition_penalty'] = generate_configs.pop('rep_penalty') if 'rep_penalty' in parameters else None

        print(f"Submission: {generate_configs}")
        generation = post(model_generate_addr, generate_configs, self.client.auth_key)
        GenerationObj = namedtuple('GenObj', generation.keys())
        results = GenerationObj(**generation)
        print(f"Success:\n{prompt} {results.text}")
        return results


    @cached_property
    def module_names(self):
        """Returns a list of all module names available to this model"""
        self.verify_request()
        return get(self.model_create_addr("module_names"))


    @cached_property
    def parameter_names(self):
        """Returns a list of all parameter names available to this model"""
        self.verify_request()
        return get(self.model_create_addr("parameter_names"))


    @cached_property
    def probe_points(self):
        """(not implemented) Returns a list of all probe points available to this model"""
        self.verify_request()
        return get(self.model_create_addr("probe_points"))


    def get_parameters(self, *names):
        """(not implemented) Returns a list of all parameters available to this model"""
        self.verify_request()
        return post(self.model_create_addr("get_parameters"), names)


    def encode(self, prompts, /, return_tensors="pt", **tokenizer_kwargs):
        tokenizer_kwargs.setdefault("return_tensors", return_tensors)
        tokenizer_kwargs.setdefault("padding", True)

        return post(
            self.model_create_addr("encode"),
            {"prompts": prompts, "tokenizer_kwargs": tokenizer_kwargs,},
        )
