import csv
import json
from typing import Iterator
import chevron
from pydantic import FilePath, ValidationError

from .prompt import Prompt

class PromptTemplate:

    def __init__(
            self,
            template_file_name: FilePath | None = None,
            template_string: str | None = None):
        if template_string != None:
            if template_file_name == None:
                self._template_string = template_string
            else:
                raise ValueError("Both file_name and template_string were provided")
        elif template_file_name != None:
            with open(template_file_name) as template_file:
                self._template_string = template_file.read()
        else:
            raise ValueError("Neither file_name nor template_string were provided")

    def render(
            self,
            data: dict | str = {},
            data_file_name: FilePath | None = None) -> Prompt:
        if data_file_name != None:
            with open(data_file_name) as data_file:
                return self.render(data_file.read())

        if type(data) == str:
            return self.render(json.loads(data))
        elif type(data) == dict:
            rendered: str = chevron.render(self._template_string, data)
            return Prompt.model_validate_json(rendered)
        else:
            raise ValueError("invalid data type")
    
    def render_from_dicts(self, data_stream : Iterator[dict]) -> Iterator[Prompt]:
        for data in data_stream:
            yield self.render(data)

    def render_from_csv(self, file_name: FilePath, **kwargs) -> Iterator[Prompt]:
        with open(file_name, newline="") as csv_file:
            return self.render_from_dicts(csv.DictReader(csv_file, **kwargs))

    def render_from_tsv(self, file_name: FilePath, **kwargs) -> Iterator[Prompt]:
        return self.render_from_csv(file_name, delimiter="\t", **kwargs)

    def render_from_ndjson(self, file_name: FilePath) -> Iterator[Prompt]:
        with open(file_name) as ndjson_file:
            for line in ndjson_file:
                trimmed_line = line.strip()
                if trimmed_line != "":
                    yield self.render(json.loads(trimmed_line))
