from typing import Optional, List
from enum import StrEnum
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase


class SelectionType(StrEnum):
    """Selection type enum"""

    TEXT = "text"
    FILE = "file"


class QueryType(StrEnum):
    """Query type enum"""

    INPUT = "input"
    SELECTION = "selection"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class MetadataCommand:
    """Metadata command"""

    command: str
    description: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Selection:
    """Selection model representing text or file selection"""

    type: SelectionType
    text: Optional[str] = None
    file_paths: Optional[List[str]] = None

    def __str__(self) -> str:
        """Convert selection to string"""
        if self.type == SelectionType.TEXT and self.text:
            return self.text
        elif self.type == SelectionType.FILE and self.file_paths:
            return " ".join(self.file_paths)
        return ""


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class QueryEnv:
    """
    Query environment information
    """

    active_window_title: str = ""
    """Active window title when user query"""

    active_window_pid: int = 0
    """Active window pid when user query, 0 if not available"""

    active_browser_url: str = ""
    """
    Active browser url when user query
    Only available when active window is browser and https://github.com/Wox-launcher/Wox.Chrome.Extension is installed
    """


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Query:
    """
    Query model representing a user query
    """

    type: QueryType
    raw_query: str
    selection: Selection
    env: QueryEnv
    trigger_keyword: Optional[str] = None
    command: Optional[str] = None
    search: str = field(default="")

    def is_global_query(self) -> bool:
        """Check if this is a global query without trigger keyword"""
        return self.type == QueryType.INPUT and not self.trigger_keyword

    def __str__(self) -> str:
        """Convert query to string"""
        if self.type == QueryType.INPUT:
            return self.raw_query
        elif self.type == QueryType.SELECTION:
            return str(self.selection)
        return ""


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ChangeQueryParam:
    """Change query parameter"""

    query_type: QueryType
    query_text: Optional[str] = None
    query_selection: Optional[Selection] = None
