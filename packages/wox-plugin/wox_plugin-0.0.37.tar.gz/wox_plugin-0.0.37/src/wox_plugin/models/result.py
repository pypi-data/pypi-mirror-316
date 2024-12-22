from typing import List, Callable, Awaitable, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum
import orjson
from .image import WoxImage
from .preview import WoxPreview


class ResultTailType(str, Enum):
    """Result tail type enum for Wox"""

    TEXT = "text"  # string type
    IMAGE = "image"  # WoxImage type


@dataclass
class ResultTail:
    """Tail model for Wox results"""

    type: ResultTailType = field(default=ResultTailType.TEXT)
    text: str = field(default="")
    image: WoxImage = field(default=WoxImage())

    def to_json(self) -> str:
        """Convert to JSON string with camelCase naming"""
        return orjson.dumps(
            {
                "Type": self.type,
                "Text": self.text,
                "Image": orjson.loads(self.image.to_json()),
            }
        ).decode("utf-8")

    @classmethod
    def from_json(cls, json_str: str) -> "ResultTail":
        """Create from JSON string with camelCase naming"""
        data = orjson.loads(json_str)
        image = WoxImage()
        if "Image" in data:
            image = WoxImage.from_json(orjson.dumps(data["Image"]).decode("utf-8"))
        return cls(
            type=ResultTailType(data["Type"]),
            text=data.get("Text", ""),
            image=image,
        )


@dataclass
class ActionContext:
    """Context for result actions"""

    context_data: str

    def to_json(self) -> str:
        """Convert to JSON string with camelCase naming"""
        return orjson.dumps(
            {
                "ContextData": self.context_data,
            }
        ).decode("utf-8")

    @classmethod
    def from_json(cls, json_str: str) -> "ActionContext":
        """Create from JSON string with camelCase naming"""
        data = orjson.loads(json_str)
        return cls(
            context_data=data["ContextData"],
        )


@dataclass
class ResultAction:
    """Action model for Wox results"""

    name: str
    action: Optional[Callable[[ActionContext], Awaitable[None]]] = None
    id: str = field(default="")
    icon: WoxImage = field(default=WoxImage())
    is_default: bool = field(default=False)
    prevent_hide_after_action: bool = field(default=False)
    hotkey: str = field(default="")

    def to_json(self) -> str:
        """Convert to JSON string with camelCase naming"""
        return orjson.dumps(
            {
                "Name": self.name,
                "Id": self.id,
                "IsDefault": self.is_default,
                "PreventHideAfterAction": self.prevent_hide_after_action,
                "Hotkey": self.hotkey,
                "Icon": orjson.loads(self.icon.to_json()),
            }
        ).decode("utf-8")

    @classmethod
    def from_json(cls, json_str: str) -> "ResultAction":
        """Create from JSON string with camelCase naming"""
        data = orjson.loads(json_str)
        return cls(
            name=data["Name"],
            id=data.get("Id", ""),
            icon=WoxImage.from_json(orjson.dumps(data["Icon"]).decode("utf-8")) if "Icon" in data else WoxImage(),
            is_default=data.get("IsDefault", False),
            prevent_hide_after_action=data.get("PreventHideAfterAction", False),
            hotkey=data.get("Hotkey", ""),
        )


@dataclass
class Result:
    """Result model for Wox"""

    title: str
    icon: WoxImage
    id: str = field(default="")
    sub_title: str = field(default="")
    preview: WoxPreview = field(default=WoxPreview())
    score: float = field(default=0.0)
    group: str = field(default="")
    group_score: float = field(default=0.0)
    tails: List[ResultTail] = field(default_factory=list)
    context_data: str = field(default="")
    actions: List[ResultAction] = field(default_factory=list)
    refresh_interval: int = field(default=0)
    on_refresh: Optional[Callable[["RefreshableResult"], Awaitable["RefreshableResult"]]] = None

    def to_json(self) -> str:
        """Convert to JSON string with camelCase naming"""
        data = {
            "Title": self.title,
            "Icon": orjson.loads(self.icon.to_json()),
            "Id": self.id,
            "SubTitle": self.sub_title,
            "Score": self.score,
            "Group": self.group,
            "GroupScore": self.group_score,
            "ContextData": self.context_data,
            "RefreshInterval": self.refresh_interval,
        }
        if self.preview:
            data["Preview"] = orjson.loads(self.preview.to_json())
        if self.tails:
            data["Tails"] = [orjson.loads(tail.to_json()) for tail in self.tails]
        if self.actions:
            data["Actions"] = [orjson.loads(action.to_json()) for action in self.actions]
        return orjson.dumps(data).decode("utf-8")

    @classmethod
    def from_json(cls, json_str: str) -> "Result":
        """Create from JSON string with camelCase naming"""
        data = orjson.loads(json_str)
        preview = WoxPreview()
        if "Preview" in data:
            preview = WoxPreview.from_json(orjson.dumps(data["Preview"]).decode("utf-8"))

        tails = []
        if "Tails" in data:
            tails = [ResultTail.from_json(orjson.dumps(tail).decode("utf-8")) for tail in data["Tails"]]

        actions = []
        if "Actions" in data:
            actions = [ResultAction.from_json(orjson.dumps(action).decode("utf-8")) for action in data["Actions"]]

        return cls(
            title=data["Title"],
            icon=WoxImage.from_json(orjson.dumps(data["Icon"]).decode("utf-8")),
            id=data.get("Id", ""),
            sub_title=data.get("SubTitle", ""),
            preview=preview,
            score=data.get("Score", 0.0),
            group=data.get("Group", ""),
            group_score=data.get("GroupScore", 0.0),
            tails=tails,
            context_data=data.get("ContextData", ""),
            actions=actions,
            refresh_interval=data.get("RefreshInterval", 0),
        )


@dataclass
class RefreshableResult:
    """Result that can be refreshed periodically"""

    title: str
    sub_title: str
    icon: WoxImage
    preview: WoxPreview
    tails: List[ResultTail] = field(default_factory=list)
    context_data: str = field(default="")
    refresh_interval: int = field(default=0)
    actions: List[ResultAction] = field(default_factory=list)

    def to_json(self) -> str:
        """Convert to JSON string with camelCase naming"""
        return orjson.dumps(
            {
                "Title": self.title,
                "SubTitle": self.sub_title,
                "Icon": orjson.loads(self.icon.to_json()),
                "Preview": orjson.loads(self.preview.to_json()),
                "Tails": [orjson.loads(tail.to_json()) for tail in self.tails],
                "ContextData": self.context_data,
                "RefreshInterval": self.refresh_interval,
                "Actions": [orjson.loads(action.to_json()) for action in self.actions],
            }
        ).decode("utf-8")

    @classmethod
    def from_json(cls, json_str: str, actions_map: Dict[str, Callable[[ActionContext], Awaitable[None]]]) -> "RefreshableResult":
        """Create from JSON string with camelCase naming"""
        data = orjson.loads(json_str)
        actions = []
        for action_data in data["Actions"]:
            action_name = action_data["Name"]
            if action_name in actions_map:
                action = ResultAction.from_json(orjson.dumps(action_data).decode("utf-8"))
                actions.append(action)

        return cls(
            title=data["Title"],
            sub_title=data["SubTitle"],
            icon=WoxImage.from_json(orjson.dumps(data["Icon"]).decode("utf-8")),
            preview=WoxPreview.from_json(orjson.dumps(data["Preview"]).decode("utf-8")),
            tails=[ResultTail.from_json(orjson.dumps(tail).decode("utf-8")) for tail in data["Tails"]],
            context_data=data["ContextData"],
            refresh_interval=data["RefreshInterval"],
            actions=actions,
        )

    def __await__(self):
        # Make RefreshableResult awaitable by returning itself
        async def _awaitable():
            return self

        return _awaitable().__await__()
