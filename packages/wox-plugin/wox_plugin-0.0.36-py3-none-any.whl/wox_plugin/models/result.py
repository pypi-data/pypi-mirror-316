from typing import Optional, List, Callable, Awaitable
from enum import StrEnum
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase
from .image import WoxImage
from .preview import WoxPreview


class ResultTailType(StrEnum):
    """Result tail type enum for Wox"""

    TEXT = "text"  # string type
    IMAGE = "image"  # WoxImage type


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ResultTail:
    """Tail model for Wox results"""

    type: ResultTailType
    text: Optional[str] = None
    image: Optional[WoxImage] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ActionContext:
    """Context for result actions"""

    context_data: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ResultAction:
    """Action model for Wox results"""

    name: str
    action: Callable[[ActionContext], Awaitable[None]] = field(metadata={"exclude": True})
    id: Optional[str] = None
    icon: Optional[WoxImage] = None
    is_default: Optional[bool] = None
    prevent_hide_after_action: Optional[bool] = None
    hotkey: Optional[str] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Result:
    """Result model for Wox"""

    title: str
    icon: WoxImage
    id: Optional[str] = None
    sub_title: Optional[str] = None
    preview: Optional[WoxPreview] = None
    score: Optional[float] = None
    group: Optional[str] = None
    group_score: Optional[float] = None
    tails: Optional[List[ResultTail]] = None
    context_data: Optional[str] = None
    actions: Optional[List[ResultAction]] = None
    refresh_interval: Optional[int] = None
    on_refresh: Optional[Callable[["RefreshableResult"], Awaitable["RefreshableResult"]]] = field(default=None, metadata={"exclude": True})


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RefreshableResult:
    """Result that can be refreshed periodically"""

    title: str
    sub_title: str
    icon: WoxImage
    preview: WoxPreview
    tails: List[ResultTail]
    context_data: str
    refresh_interval: int
    actions: List[ResultAction]

    def __await__(self):
        # Make RefreshableResult awaitable by returning itself
        async def _awaitable():
            return self

        return _awaitable().__await__()
