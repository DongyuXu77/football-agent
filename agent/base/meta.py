import json
import os
from abc import ABC, abstractclassmethod

import openai

from agent.utils import call_client

class agent(ABC):
    r"""
    """

    def __init__(self, system_prompt: str) -> None:
        r"""
        """
        self.system_prompt = system_prompt
        self.few_shot_prompt = None

    def _change_system_prompt(self, system_prompt: str) -> None:
        r"""
        """
        self.system_prompt = system_prompt
    
    def _finetune_model(self, origin_model: str, train_file: str):
        try:
            self.client.fine_tuning.jobs.create(
                model=origin_model,
                training_file=train_file,
            )
        except openai.APIError:
            raise "OPENAI API ERROR OCCURS"
        
    
    def wrap_input_content(self, input_content: str) -> None:
        r"""
        """
        self.wrap_input_content = input_content
        return input_content
    
    def set_few_shot_prompt(self, json_file_path: str) -> None:
        r"""
        """
        if not os.path.exists(json_file_path):
            raise FileNotFoundError(f" the set_few_shot_prompt file in path :{json_file_path} doesn't exist")
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        assert isinstance(data, list), f"The json file in {json_file_path} must be a list"

        self.few_shot_prompt = data

    def get_response(self, model: str='gpt-3.5-turbo-16k'):
        r"""
        """
        hook_prompt = self.few_shot_prompt if isinstance(self.few_shot_prompt, list) else []
        assert isinstance(self.wrap_content, str), " the wrap_input_content function must be called before calling the get_respoense function"
        
        response = call_client().chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': self.system_prompt},
                *hook_prompt,
                {'role': 'user', 'content': self.wrap_content},
            ]
        )

        return response, response.choices[0].message.content, response.choices[0].finish_reason