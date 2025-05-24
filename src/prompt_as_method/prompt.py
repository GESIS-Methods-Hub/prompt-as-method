from typing import Annotated, Any, List, Literal, Union
from pydantic import BaseModel, Field, TypeAdapter

class BaseMessage(BaseModel):
    content: str

class AssistantMessage(BaseMessage):
    role: Literal["assistant"] = "assistant"

class SystemMessage(BaseMessage):
    role: Literal["system"] = "system"

class UserMessage(BaseMessage):
    role: Literal["user"] = "user"

Message = Annotated[Union[AssistantMessage, SystemMessage, UserMessage], Field(discriminator="role")]

Messages = List[Message]

class ResponseFormat(BaseModel):
    type: Literal["json_schema"]
    json_schema: dict[str, Any]

class PromptParameters(BaseModel):
    model: str
    max_completion_tokens: int | None = None
    temperature: Annotated[float, Field(ge=0, le=2)] = 1
    top_p: Annotated[float, Field(ge=0, le=1)] = 1

class Prompt(PromptParameters):
    messages: Messages
    response_format: ResponseFormat | None = None
