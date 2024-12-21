from typing import Optional, List, Dict
from enum import StrEnum
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


class PluginSettingDefinitionType(StrEnum):
    """Plugin setting definition type enum"""

    HEAD = "head"
    TEXTBOX = "textbox"
    CHECKBOX = "checkbox"
    SELECT = "select"
    SELECT_AI_MODEL = "selectAIModel"
    LABEL = "label"
    NEWLINE = "newline"
    TABLE = "table"
    DYNAMIC = "dynamic"  # dynamic setting will be replaced by the actual setting when retrieved


@dataclass_json
@dataclass
class PluginSettingValueStyle:
    """Plugin setting value style"""

    PaddingLeft: int = 0
    PaddingTop: int = 0
    PaddingRight: int = 0
    PaddingBottom: int = 0
    Width: int = 0
    LabelWidth: int = 0  # if has label, E.g. select, checkbox, textbox


@dataclass_json
@dataclass
class PluginSettingValueBase:
    """Base class for all plugin setting values"""

    Key: str
    DefaultValue: str = ""

    def get_key(self) -> str:
        """Get the key of the setting"""
        return self.Key

    def get_default_value(self) -> str:
        """Get the default value of the setting"""
        return self.DefaultValue


@dataclass_json
@dataclass
class PluginSettingValueHead(PluginSettingValueBase):
    """Head setting value"""

    Title: str
    Description: Optional[str] = None
    Style: Optional[PluginSettingValueStyle] = None


@dataclass_json
@dataclass
class PluginSettingValueTextBox(PluginSettingValueBase):
    """TextBox setting value"""

    Label: str
    Description: Optional[str] = None
    Style: Optional[PluginSettingValueStyle] = None


@dataclass_json
@dataclass
class PluginSettingValueCheckBox(PluginSettingValueBase):
    """CheckBox setting value"""

    Label: str
    Description: Optional[str] = None
    Style: Optional[PluginSettingValueStyle] = None


@dataclass_json
@dataclass
class PluginSettingValueSelect(PluginSettingValueBase):
    """Select setting value"""

    Label: str
    Description: Optional[str] = None
    Options: List[str] = field(default_factory=list)
    Style: Optional[PluginSettingValueStyle] = None


@dataclass_json
@dataclass
class PluginSettingValueLabel(PluginSettingValueBase):
    """Label setting value"""

    Label: str
    Description: Optional[str] = None
    Style: Optional[PluginSettingValueStyle] = None


@dataclass_json
@dataclass
class PluginSettingValueNewLine(PluginSettingValueBase):
    """NewLine setting value"""

    pass


@dataclass_json
@dataclass
class PluginSettingValueTable(PluginSettingValueBase):
    """Table setting value"""

    Label: str
    Description: Optional[str] = None
    Columns: List[str] = field(default_factory=list)
    Style: Optional[PluginSettingValueStyle] = None


@dataclass_json
@dataclass
class PluginSettingDefinitionItem:
    """Plugin setting definition item"""

    Type: PluginSettingDefinitionType
    Value: PluginSettingValueBase
    DisabledInPlatforms: Optional[List[str]] = None
    IsPlatformSpecific: bool = False  # if true, this setting may be different in different platforms


@dataclass_json
@dataclass
class PluginSettingDefinitions:
    """Plugin setting definitions"""

    Definitions: List[PluginSettingDefinitionItem] = field(default_factory=list)

    def get_default_value(self, key: str) -> Optional[str]:
        """Get default value for a key"""
        for item in self.Definitions:
            if item.Value.get_key() == key:
                return item.Value.get_default_value()
        return None

    def get_all_defaults(self) -> Dict[str, str]:
        """Get all default values"""
        settings = {}
        for item in self.Definitions:
            if item.Value:
                settings[item.Value.get_key()] = item.Value.get_default_value()
        return settings


@dataclass_json
@dataclass
class MetadataCommand:
    """Metadata for plugin commands"""

    Command: str
    Description: str
