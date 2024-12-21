from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase
from enum import StrEnum
from typing import List, Optional, Dict
from uuid import uuid4


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


class PluginSettingValidatorType(StrEnum):
    """Plugin setting validator type enum"""

    IS_NUMBER = "is_number"
    NOT_EMPTY = "not_empty"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PluginSettingValueStyle:
    """Plugin setting value style"""

    padding_left: int = 0
    padding_top: int = 0
    padding_right: int = 0
    padding_bottom: int = 0
    width: int = 0
    label_width: int = 0  # if has label, E.g. select, checkbox, textbox


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PluginSettingValidatorIsNumber:
    """Plugin setting validator for number"""

    is_integer: bool = False
    is_float: bool = False


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PluginSettingValidator:
    """Plugin setting validator"""

    type: PluginSettingValidatorType
    value: Dict  # This will be deserialized based on Type


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PluginSettingValueSelectOption:
    """Plugin setting value select option"""

    label: str
    value: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PluginSettingValueHead:
    """Head setting value"""

    content: str
    tooltip: str = ""
    style: Optional[PluginSettingValueStyle] = None

    def get_key(self) -> str:
        return str(uuid4())

    def get_default_value(self) -> str:
        return ""


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PluginSettingValueTextBox:
    """TextBox setting value"""

    key: str
    label: str
    default_value: str = ""
    suffix: str = ""
    tooltip: str = ""
    style: Optional[PluginSettingValueStyle] = None
    validators: List[PluginSettingValidator] = field(default_factory=list)

    def get_key(self) -> str:
        return self.key

    def get_default_value(self) -> str:
        return self.default_value


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PluginSettingValueCheckBox:
    """CheckBox setting value"""

    key: str
    label: str
    default_value: str = ""
    tooltip: str = ""
    style: Optional[PluginSettingValueStyle] = None

    def get_key(self) -> str:
        return self.key

    def get_default_value(self) -> str:
        return self.default_value


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PluginSettingValueSelect:
    """Select setting value"""

    key: str
    label: str
    default_value: str = ""
    suffix: str = ""
    tooltip: str = ""
    options: List[PluginSettingValueSelectOption] = field(default_factory=list)
    validators: List[PluginSettingValidator] = field(default_factory=list)
    style: Optional[PluginSettingValueStyle] = None

    def get_key(self) -> str:
        return self.key

    def get_default_value(self) -> str:
        return self.default_value


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PluginSettingValueLabel:
    """Label setting value"""

    content: str
    tooltip: str = ""
    style: Optional[PluginSettingValueStyle] = None

    def get_key(self) -> str:
        return str(uuid4())

    def get_default_value(self) -> str:
        return ""


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PluginSettingValueNewLine:
    """NewLine setting value"""

    style: Optional[PluginSettingValueStyle] = None

    def get_key(self) -> str:
        return str(uuid4())

    def get_default_value(self) -> str:
        return ""


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PluginSettingValueTableColumn:
    """Table column definition"""

    key: str
    label: str
    width: int = 0
    tooltip: str = ""
    type: str = "text"  # text, textList, checkbox, dirPath, select, selectAIModel, woxImage
    validators: List[PluginSettingValidator] = field(default_factory=list)
    select_options: List[PluginSettingValueSelectOption] = field(default_factory=list)
    text_max_lines: int = 1
    hide_in_table: bool = False
    hide_in_update: bool = False


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PluginSettingValueTable:
    """Table setting value"""

    key: str
    title: str
    default_value: str = ""
    tooltip: str = ""
    columns: List[PluginSettingValueTableColumn] = field(default_factory=list)
    sort_column_key: str = ""
    sort_order: str = "asc"  # asc or desc
    style: Optional[PluginSettingValueStyle] = None

    def get_key(self) -> str:
        return self.key

    def get_default_value(self) -> str:
        return self.default_value


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PluginSettingValueSelectAiModel:
    """Select AI model setting value"""

    key: str
    label: str
    default_value: str = ""
    suffix: str = ""
    tooltip: str = ""
    validators: List[PluginSettingValidator] = field(default_factory=list)
    style: Optional[PluginSettingValueStyle] = None

    def get_key(self) -> str:
        return self.key

    def get_default_value(self) -> str:
        return self.default_value


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PluginSettingDefinitionItem:
    """Plugin setting definition item"""

    type: PluginSettingDefinitionType
    value: object  # This will be one of the PluginSettingValue* classes
    disabled_in_platforms: Optional[List[str]] = None
    is_platform_specific: bool = False  # if true, this setting may be different in different platforms


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PluginSettingDefinitions:
    """Plugin setting definitions"""

    definitions: List[PluginSettingDefinitionItem] = field(default_factory=list)

    def get_default_value(self, key: str) -> Optional[str]:
        """Get default value for a key"""
        for item in self.definitions:
            if hasattr(item.value, "get_key") and item.value.get_key() == key:
                return item.value.get_default_value()
        return None

    def get_all_defaults(self) -> Dict[str, str]:
        """Get all default values"""
        settings = {}
        for item in self.definitions:
            if hasattr(item.value, "get_key") and hasattr(item.value, "get_default_value"):
                settings[item.value.get_key()] = item.value.get_default_value()
        return settings
