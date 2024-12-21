"""
Wox Plugin SDK for Python

This package provides the SDK for developing Wox plugins in Python.
"""

from typing import List

from .plugin import Plugin, BasePlugin, PluginInitParams
from .api import PublicAPI, ChatStreamCallback
from .models.context import Context
from .models.query import (
    Query,
    QueryEnv,
    Selection,
    ChangeQueryParam,
    QueryType,
    SelectionType,
    MetadataCommand,
)
from .models.result import (
    Result,
    ResultTail,
    ResultAction,
    ActionContext,
    RefreshableResult,
    ResultTailType,
)
from .models.settings import (
    PluginSettingDefinitionType,
    PluginSettingValueStyle,
    PluginSettingValueHead,
    PluginSettingValueTextBox,
    PluginSettingValueCheckBox,
    PluginSettingValueSelect,
    PluginSettingValueLabel,
    PluginSettingValueNewLine,
    PluginSettingValueTable,
    PluginSettingDefinitionItem,
    PluginSettingDefinitions,
    PluginSettingValidator,
    PluginSettingValidatorType,
    PluginSettingValidatorIsNumber,
    PluginSettingValueSelectOption,
    PluginSettingValueTableColumn,
    PluginSettingValueSelectAiModel,
)
from .models.ai import (
    AIModel,
    Conversation,
    ConversationRole,
    ChatStreamDataType,
    user_message,
    ai_message,
)
from .models.image import WoxImage, WoxImageType
from .models.preview import WoxPreview, WoxPreviewType, WoxPreviewScrollPosition


__all__: List[str] = [
    # Plugin
    "Plugin",
    "BasePlugin",
    "PluginInitParams",
    # API
    "PublicAPI",
    "ChatStreamCallback",
    # Models
    "Context",
    "Query",
    "QueryEnv",
    "Selection",
    "Result",
    "WoxImage",
    "WoxPreview",
    "ResultTail",
    "ResultAction",
    "ActionContext",
    "RefreshableResult",
    "MetadataCommand",
    "PluginSettingDefinitionItem",
    "PluginSettingValueStyle",
    # AI
    "AIModel",
    "Conversation",
    "ConversationRole",
    "ChatStreamDataType",
    "user_message",
    "ai_message",
    # Query
    "ChangeQueryParam",
    "QueryType",
    "Selection",
    "SelectionType",
    # Exceptions
    "WoxPluginError",
    "InvalidQueryError",
    "PluginInitError",
    "APIError",
    # Image
    "WoxImage",
    "WoxImageType",
    # Preview
    "WoxPreview",
    "WoxPreviewType",
    "WoxPreviewScrollPosition",
    # Settings
    "PluginSettingDefinitionType",
    "PluginSettingValueHead",
    "PluginSettingValueTextBox",
    "PluginSettingValueCheckBox",
    "PluginSettingValueSelect",
    "PluginSettingValueLabel",
    "PluginSettingValueNewLine",
    "PluginSettingValueTable",
    "PluginSettingDefinitions",
    "PluginSettingValidator",
    "PluginSettingValidatorType",
    "PluginSettingValidatorIsNumber",
    "PluginSettingValueSelectOption",
    "PluginSettingValueTableColumn",
    "PluginSettingValueSelectAiModel",
    # Result
    "ResultTailType",
]
