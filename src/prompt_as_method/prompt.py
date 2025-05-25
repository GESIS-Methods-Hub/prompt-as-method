from typing import Annotated, Any, List, Literal, Union
from pydantic import BaseModel, Field


class BaseMessage(BaseModel):
    content: str


class AssistantMessage(BaseMessage):
    role: Literal["assistant"] = "assistant"


class SystemMessage(BaseMessage):
    role: Literal["system"] = "system"


class UserMessage(BaseMessage):
    role: Literal["user"] = "user"


Message = Annotated[Union[AssistantMessage, SystemMessage, UserMessage], Field(discriminator="role")]

Messages = Annotated[List[Message], Field(min_length=1)]


class ResponseFormat(BaseModel):
    type: Literal["json_schema"]
    json_schema: dict[str, Any]


temperature_min = 0
temperature_max = 2
temperature_default = 1
top_p_min = 0
top_p_max = 2
top_p_default = 1


class PromptParameters(BaseModel):
    model: str
    max_completion_tokens: int | None = None
    temperature: Annotated[float, Field(ge=temperature_min, le=temperature_max)] = temperature_default
    top_p: Annotated[float, Field(ge=top_p_min, le=top_p_max)] = top_p_default


class Prompt(PromptParameters):
    messages: Messages
    response_format: ResponseFormat | None = None
