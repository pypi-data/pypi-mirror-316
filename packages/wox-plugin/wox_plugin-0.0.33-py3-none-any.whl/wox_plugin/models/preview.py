from typing import Dict
from enum import StrEnum
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


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


@dataclass_json
@dataclass
class WoxPreview:
    """Preview model for Wox results"""

    PreviewType: WoxPreviewType
    PreviewData: str
    PreviewProperties: Dict[str, str] = field(default_factory=dict)
    ScrollPosition: WoxPreviewScrollPosition = WoxPreviewScrollPosition.BOTTOM
