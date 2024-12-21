from typing import Dict
from enum import StrEnum
from pydantic import BaseModel


class WoxPreviewType(StrEnum):
    """Preview type enum for Wox"""

    MARKDOWN = "markdown"
    TEXT = "text"
    IMAGE = "image"  # when type is image, data should be WoxImage.String()
    URL = "url"
    FILE = "file"  # when type is file(can be *.md, *.jpg, *.pdf and so on), data should be url/filepath
    REMOTE = "remote"  # when type is remote, data should be url to load WoxPreview


class WoxPreviewScrollPosition(StrEnum):
    """Preview scroll position enum for Wox"""

    BOTTOM = "bottom"  # scroll to bottom after preview first show


class WoxPreview(BaseModel):
    """Preview model for Wox results"""

    PreviewType: WoxPreviewType
    PreviewData: str
    PreviewProperties: Dict[str, str]
    ScrollPosition: WoxPreviewScrollPosition = WoxPreviewScrollPosition.BOTTOM
