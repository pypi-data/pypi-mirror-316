from typing import Dict
from enum import StrEnum
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase


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


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class WoxPreview:
    """Preview model for Wox results"""

    preview_type: WoxPreviewType
    preview_data: str
    preview_properties: Dict[str, str] = field(default_factory=dict)
    scroll_position: WoxPreviewScrollPosition = WoxPreviewScrollPosition.BOTTOM
