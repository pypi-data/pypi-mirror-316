from enum import Enum
from typing import List, Optional, Callable
import time
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase


class ConversationRole(str, Enum):
    """Role in the conversation"""

    USER = "user"
    AI = "ai"


class ChatStreamDataType(str, Enum):
    """Type of chat stream data"""

    STREAMING = "streaming"  # Currently streaming
    FINISHED = "finished"  # Stream completed
    ERROR = "error"  # Error occurred


ChatStreamCallback = Callable[[ChatStreamDataType, str], None]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AIModel:
    """AI model definition"""

    name: str
    provider: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Conversation:
    """Conversation content"""

    role: ConversationRole
    text: str
    images: List[bytes] = field(default_factory=list)  # PNG format image data
    timestamp: Optional[int] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = int(time.time() * 1000)

    def to_dict(self) -> dict:
        """Convert to dictionary format"""
        return {
            "role": self.role,
            "text": self.text,
            "images": self.images,
            "timestamp": self.timestamp,
        }


def user_message(text: str, images: List[bytes] = None) -> Conversation:
    """Create a user message"""
    return Conversation(role=ConversationRole.USER, text=text, images=images or [])


def ai_message(text: str) -> Conversation:
    """Create an AI message"""
    return Conversation(role=ConversationRole.AI, text=text)
