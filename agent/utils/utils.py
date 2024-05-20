import os

import openai
from openai import OpenAI

class Registry(object):
    r""" helper function to registe sub model 
    """

    def __init__(self, name) -> None:
        self._name = name
        self._module_dict = dict()
    
    @property
    def name(self):
        return self._name
    
    @property
    def module_dict(self):
        return self._module_dict
    
    @property
    def module_name(self):
        return list(self._module_dict.keys())
    
    def register(self, cls):
        module_name = cls.__name__
        if module_name in self._module_dict:
            raise KeyError(f'{module_name} is already registered in {self._name}')
        self._module_dict[module_name] = cls
        
        return cls
    
    def get(self, name):
        if name in self._module_dict:
            return self._module_dict[name]
        else:
            raise KeyError(f'{name} is not registered in {self.name}')


def call_client(timeout: float=30.0, max_retries: int=3):
    client = OpenAI(
        base_url="https://api.gptsapi.net/v1",
        api_key=os.environ.get("OPENAI_API_KEY"),
        timeout=timeout,
        max_retries=max_retries
    )
    return client