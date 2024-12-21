from enum import StrEnum
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase


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


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class WoxImage:
    """Image model for Wox"""

    image_type: WoxImageType
    image_data: str

    @staticmethod
    def new_base64(data: str) -> "WoxImage":
        """Create a new base64 image"""
        return WoxImage(image_type=WoxImageType.BASE64, image_data=data)

    @staticmethod
    def new_svg(data: str) -> "WoxImage":
        """Create a new svg image"""
        return WoxImage(image_type=WoxImageType.SVG, image_data=data)

    @staticmethod
    def new_lottie(data: str) -> "WoxImage":
        """Create a new lottie image"""
        return WoxImage(image_type=WoxImageType.LOTTIE, image_data=data)

    @staticmethod
    def new_emoji(data: str) -> "WoxImage":
        """Create a new emoji image"""
        return WoxImage(image_type=WoxImageType.EMOJI, image_data=data)

    @staticmethod
    def new_url(data: str) -> "WoxImage":
        """Create a new url image"""
        return WoxImage(image_type=WoxImageType.URL, image_data=data)

    @staticmethod
    def new_absolute(data: str) -> "WoxImage":
        """Create a new absolute image"""
        return WoxImage(image_type=WoxImageType.ABSOLUTE, image_data=data)

    @staticmethod
    def new_relative(data: str) -> "WoxImage":
        """Create a new relative image"""
        return WoxImage(image_type=WoxImageType.RELATIVE, image_data=data)

    @staticmethod
    def new_theme(data: str) -> "WoxImage":
        """Create a new theme image"""
        return WoxImage(image_type=WoxImageType.THEME, image_data=data)

    def __str__(self) -> str:
        """Convert image to string"""
        return f"{self.image_type}:{self.image_data}"
