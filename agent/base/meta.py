import json
import os
from abc import ABC, abstractclassmethod

import openai
from openai import OpenAI

class agent(ABC):
    r"""
    """

    def __init__(self, system_prompt: str, timeout: float, max_retries: int) -> None:
        r"""
        """
        self.client = self._create_client(timeout, max_retries)
        self.system_prompt = system_prompt
        self.few_shot_prompt = None
        self.wrap_content = None

    def _create_client(self, timeout: float, max_retries: int):
        r"""
        """

        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            timeout=timeout,
            max_retries=max_retries
        )

        return client
    
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
        
    
    @abstractclassmethod
    def wrap_input_content(self) -> None:
        r"""
        """
        pass
    
    def set_few_shot_prompt(self, json_file_path: str) -> None:
        r"""
        """
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        assert isinstance(data, list), f"The json file in {json_file_path} must be a list"

        self.few_shot_prompt = data

    def get_respoense(self, model: str='gpt-3.5-turbo'):
        r"""
        """
        hook_prompt = self.few_shot_prompt if isinstance(self.few_shot_prompt, list) else []
        assert isinstance(self.wrap_content, str), " the wrap_input_content function must be called before calling the get_respoense function"
        
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': self.system_prompt},
                *hook_prompt,
                {'role': 'user', 'content': self.wrap_content},
            ]
        )

        return response, response.choices[0].message.content, response.choices[0].finish_reason