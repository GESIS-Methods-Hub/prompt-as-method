import abc
from enum import Enum
import json
from typing import Iterator
import requests

from pydantic import HttpUrl
from .prompt import Prompt


class LLM(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def generate(self, prompt: Prompt) -> dict:
        pass

    def generate_all(self, prompts: Iterator[Prompt]) -> Iterator[dict]:
        for prompt in prompts:
            yield self.generate(prompt)


class LLMType(Enum):
    openai = "OpenAI"

    def __str__(self):
        return self.value


class HttpLLM(LLM):

    def __init__(self, url: str):
        self._url = HttpUrl(url)

    @abc.abstractmethod
    def _prompt_to_request_data(self, prompt: Prompt) -> dict:
        return {}

    def generate(self, prompt: Prompt) -> dict:
        request_data = json.dumps(self._prompt_to_request_data(prompt))
        response = requests.post(
            url=self._url.__str__(),
            headers={
                "Content-Type": "application/json"
            },
            data=request_data)
        if response.status_code != 200:
            raise ValueError(f"Error returned from {self._url}: {response.text}")
        return response.json()

    @staticmethod
    def init(llm_type: LLMType, url: str) -> "HttpLLM":
        match llm_type:
            case LLMType.openai:
                return OpenAI(url)
            case _:
                raise ValueError(f"Invalid LLMType: {type(llm_type)}")


class ChatCompletion(Prompt):
    stream: bool = False


class OpenAI(HttpLLM):

    def __init__(self, url: str):
        super().__init__(url)

    def _prompt_to_request_data(self, prompt: Prompt) -> dict:
        chat_completion = ChatCompletion.model_validate(prompt.model_dump())
        return chat_completion.model_dump(exclude_none=True)
