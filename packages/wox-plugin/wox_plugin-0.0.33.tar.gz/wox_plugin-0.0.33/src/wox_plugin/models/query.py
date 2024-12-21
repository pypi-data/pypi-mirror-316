from typing import Optional, List
from enum import StrEnum
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


class SelectionType(StrEnum):
    """Selection type enum"""

    TEXT = "text"
    FILE = "file"


class QueryType(StrEnum):
    """Query type enum"""

    INPUT = "input"
    SELECTION = "selection"


@dataclass_json
@dataclass
class MetadataCommand:
    """Metadata command"""

    Command: str
    Description: str


@dataclass_json
@dataclass
class Selection:
    """Selection model representing text or file selection"""

    Type: SelectionType
    Text: Optional[str] = None
    FilePaths: Optional[List[str]] = None

    def __str__(self) -> str:
        """Convert selection to string"""
        if self.Type == SelectionType.TEXT and self.Text:
            return self.Text
        elif self.Type == SelectionType.FILE and self.FilePaths:
            return " ".join(self.FilePaths)
        return ""


@dataclass_json
@dataclass
class QueryEnv:
    """
    Query environment information
    """

    ActiveWindowTitle: str = ""
    """Active window title when user query"""

    ActiveWindowPid: int = 0
    """Active window pid when user query, 0 if not available"""

    ActiveBrowserUrl: str = ""
    """
    Active browser url when user query
    Only available when active window is browser and https://github.com/Wox-launcher/Wox.Chrome.Extension is installed
    """


@dataclass_json
@dataclass
class Query:
    """
    Query model representing a user query
    """

    Type: QueryType
    RawQuery: str
    Selection: Selection
    Env: QueryEnv
    TriggerKeyword: Optional[str] = None
    Command: Optional[str] = None
    Search: str = field(default="")

    def is_global_query(self) -> bool:
        """Check if this is a global query without trigger keyword"""
        return self.Type == QueryType.INPUT and not self.TriggerKeyword

    def __str__(self) -> str:
        """Convert query to string"""
        if self.Type == QueryType.INPUT:
            return self.RawQuery
        elif self.Type == QueryType.SELECTION:
            return str(self.Selection)
        return ""


@dataclass_json
@dataclass
class ChangeQueryParam:
    """Change query parameter"""

    QueryType: QueryType
    QueryText: Optional[str] = None
    QuerySelection: Optional[Selection] = None
