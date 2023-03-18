from typing import Optional
from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class HistoryEntry:
    timestamp: int


@dataclass
class CompletionHistoryEntry(HistoryEntry):
    message: str
    response: str

    @classmethod
    def from_message(cls, message: str, timestamp: int, response: str):
        return cls(message=message, response=response, timestamp=timestamp)


@dataclass
class ChatHistoryEntry(HistoryEntry):
    message: str
    message_role: str  # "user" or "system"
    response: str

    @classmethod
    def from_message(cls, message: str, timestamp: int, response: str):
        role = "user"
        if message.lower().startswith("you are"):
            role = "system"
        return cls(
            message=message, message_role=role, response=response, timestamp=timestamp
        )


@dataclass
class EntitiesRequest:
    text: str


@dataclass
class EntitiesResponse:
    text: str


class Network(BaseModel):
    name: str
    command: str
    version: str


class OpenAiNetwork(Network):
    ...


class OpenAIIntegration(BaseModel):
    api_key: str
    networks: list[OpenAiNetwork]


class ReplicateNetwork(Network):
    type: str


class ReplicateIntegration(BaseModel):
    api_key: str
    networks: list[ReplicateNetwork]


class Integrations(BaseModel):
    openai: Optional[OpenAIIntegration]
    replicate: Optional[ReplicateIntegration]


class TelegramSettings(BaseModel):
    bot_token: str
    admin_id: Optional[int]
    allowed_users: list[int] = []
    allowed_chats: list[int] = []


class GeneralSettings(BaseModel):
    text_history_size: int = 10
    text_history_ttl: int = 300


class ConfigException(Exception):
    pass


class IntegrationException(Exception):
    pass
