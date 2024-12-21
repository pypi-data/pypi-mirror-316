from enum import Enum
from typing import Any, Optional, Union

from pydantic import BaseModel


class PayloadType(str, Enum):
    LABELER = "labeler"
    LLM_GRAPH = "llm-graph"
    SYNTHETIC_QUESTIONS = "synthetic-questions"
    ASK = "ask"
    LLAMA_GUARD = "llama-guard"
    PROMPT_GUARD = "prompt-guard"


class Ask(BaseModel):
    text: Optional[str] = None
    json_output: Optional[dict[str, Any]] = None
    empty: bool = False


class Position(BaseModel):
    start: int
    end: int


class Entities(BaseModel):
    labels: dict[str, str]
    positions: dict[str, list[Position]]


class Relations(BaseModel):
    relations: list[tuple[str, str, str]]


class Labels(BaseModel):
    labels: dict[str, Union[str, list[str]]]


class Question(BaseModel):
    question: str
    answer: str
    block: int
    reasoning: str
    paragraph_id: str


class Payload(BaseModel):
    type: PayloadType
    kbid: str
    field: str
    errors: list[str]
    rid: Optional[str] = None
    asks: Optional[list[Ask]] = None
    relations: Optional[list[Relations]] = None
    entities: Optional[list[Entities]] = None
    labels: Optional[list[Labels]] = None
    guard_labels: Optional[list[str]] = None
    prompt_guard: Optional[list[str]] = None
    qas: Optional[list[Question]] = None
