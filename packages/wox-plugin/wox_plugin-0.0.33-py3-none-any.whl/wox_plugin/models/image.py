from enum import StrEnum
from dataclasses import dataclass
from dataclasses_json import dataclass_json


class WoxImageType(StrEnum):
    """Image type enum for Wox"""

    ABSOLUTE = "absolute"
    RELATIVE = "relative"
    BASE64 = "base64"
    SVG = "svg"
    LOTTIE = "lottie"  # only support lottie json data
    EMOJI = "emoji"
    URL = "url"
    THEME = "theme"


@dataclass_json
@dataclass
class WoxImage:
    """Image model for Wox"""

    ImageType: WoxImageType
    ImageData: str

    @staticmethod
    def new_base64(data: str) -> "WoxImage":
        """Create a new base64 image"""
        return WoxImage(ImageType=WoxImageType.BASE64, ImageData=data)

    @staticmethod
    def new_svg(data: str) -> "WoxImage":
        """Create a new svg image"""
        return WoxImage(ImageType=WoxImageType.SVG, ImageData=data)

    @staticmethod
    def new_lottie(data: str) -> "WoxImage":
        """Create a new lottie image"""
        return WoxImage(ImageType=WoxImageType.LOTTIE, ImageData=data)

    @staticmethod
    def new_emoji(data: str) -> "WoxImage":
        """Create a new emoji image"""
        return WoxImage(ImageType=WoxImageType.EMOJI, ImageData=data)

    @staticmethod
    def new_url(data: str) -> "WoxImage":
        """Create a new url image"""
        return WoxImage(ImageType=WoxImageType.URL, ImageData=data)

    @staticmethod
    def new_absolute(data: str) -> "WoxImage":
        """Create a new absolute image"""
        return WoxImage(ImageType=WoxImageType.ABSOLUTE, ImageData=data)

    @staticmethod
    def new_relative(data: str) -> "WoxImage":
        """Create a new relative image"""
        return WoxImage(ImageType=WoxImageType.RELATIVE, ImageData=data)

    @staticmethod
    def new_theme(data: str) -> "WoxImage":
        """Create a new theme image"""
        return WoxImage(ImageType=WoxImageType.THEME, ImageData=data)

    def __str__(self) -> str:
        """Convert image to string"""
        return f"{self.ImageType}:{self.ImageData}"
