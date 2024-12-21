from typing import Optional, List
from enum import StrEnum
from pydantic import BaseModel


class SelectionType(StrEnum):
    """Selection type enum"""

    TEXT = "text"
    FILE = "file"


class QueryType(StrEnum):
    """Query type enum"""

    INPUT = "input"
    SELECTION = "selection"


class MetadataCommand(BaseModel):
    """Metadata command"""

    Command: str
    Description: str


class Selection(BaseModel):
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


class QueryEnv(BaseModel):
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


class Query(BaseModel):
    """
    Query model representing a user query
    """

    Type: QueryType
    RawQuery: str
    TriggerKeyword: Optional[str] = None
    Command: Optional[str] = None
    Search: str
    Selection: Selection
    Env: QueryEnv

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


class ChangeQueryParam(BaseModel):
    """Change query parameter"""

    QueryType: QueryType
    QueryText: Optional[str] = None
    QuerySelection: Optional[Selection] = None
