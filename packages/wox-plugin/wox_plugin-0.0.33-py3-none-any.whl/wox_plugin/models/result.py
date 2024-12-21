from typing import Optional, List, Callable, Awaitable
from enum import StrEnum
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from .image import WoxImage
from .preview import WoxPreview


class ResultTailType(StrEnum):
    """Result tail type enum for Wox"""

    TEXT = "text"  # string type
    IMAGE = "image"  # WoxImage type


@dataclass_json
@dataclass
class ResultTail:
    """Tail model for Wox results"""

    Type: ResultTailType
    Text: Optional[str] = None
    Image: Optional[WoxImage] = None


@dataclass_json
@dataclass
class ActionContext:
    """Context for result actions"""

    ContextData: str


@dataclass_json
@dataclass
class ResultAction:
    """Action model for Wox results"""

    Name: str
    Action: Callable[[ActionContext], Awaitable[None]] = field(metadata=config(exclude=True))
    Id: Optional[str] = None
    Icon: Optional[WoxImage] = None
    IsDefault: Optional[bool] = None
    PreventHideAfterAction: Optional[bool] = None
    Hotkey: Optional[str] = None


@dataclass_json
@dataclass
class Result:
    """Result model for Wox"""

    Title: str
    Icon: WoxImage
    Id: Optional[str] = None
    SubTitle: Optional[str] = None
    Preview: Optional[WoxPreview] = None
    Score: Optional[float] = None
    Group: Optional[str] = None
    GroupScore: Optional[float] = None
    Tails: Optional[List[ResultTail]] = None
    ContextData: Optional[str] = None
    Actions: Optional[List[ResultAction]] = None
    RefreshInterval: Optional[int] = None
    OnRefresh: Optional[Callable[["RefreshableResult"], Awaitable["RefreshableResult"]]] = field(
        default=None, metadata=config(exclude=True)
    )


@dataclass_json
@dataclass
class RefreshableResult:
    """Result that can be refreshed periodically"""

    Title: str
    SubTitle: str
    Icon: WoxImage
    Preview: WoxPreview
    Tails: List[ResultTail]
    ContextData: str
    RefreshInterval: int
    Actions: List[ResultAction]

    def __await__(self):
        # Make RefreshableResult awaitable by returning itself
        async def _awaitable():
            return self

        return _awaitable().__await__()
