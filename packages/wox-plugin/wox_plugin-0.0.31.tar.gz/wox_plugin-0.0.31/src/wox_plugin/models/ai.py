from enum import Enum
from typing import List, Optional, Callable
import time
from pydantic import BaseModel


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


class AIModel(BaseModel):
    """AI model definition"""

    name: str
    provider: str


class Conversation(BaseModel):
    """Conversation content"""

    role: ConversationRole
    text: str
    images: List[bytes] = []  # PNG format image data
    timestamp: int = None

    def model_post_init(self, __context) -> None:
        if self.timestamp is None:
            self.timestamp = int(time.time() * 1000)

    def to_dict(self) -> dict:
        """Convert to dictionary format"""
        return {
            "Role": self.role,
            "Text": self.text,
            "Images": self.images,
            "Timestamp": self.timestamp,
        }


def user_message(text: str, images: List[bytes] = None) -> Conversation:
    """Create a user message"""
    return Conversation(role=ConversationRole.USER, text=text, images=images or [])


def ai_message(text: str) -> Conversation:
    """Create an AI message"""
    return Conversation(role=ConversationRole.AI, text=text)
