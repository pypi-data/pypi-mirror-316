"""
Wox Plugin SDK for Python

This package provides the SDK for developing Wox plugins in Python.
"""

from typing import List

from .plugin import Plugin, BasePlugin, PluginInitParams
from .api import PublicAPI, ChatStreamCallback
from .models.common import Context, MetadataCommand, PluginSettingDefinitionItem
from .models.query import (
    Query,
    QueryEnv,
    Selection,
    ChangeQueryParam,
    QueryType,
    SelectionType,
)
from .models.result import (
    Result,
    WoxImage,
    WoxPreview,
    ResultTail,
    ResultAction,
    ActionContext,
    RefreshableResult,
)
from .models.settings import (
    PluginSettingDefinitionValue,
    PluginSettingValueStyle,
)
from .models.ai import (
    AIModel,
    Conversation,
    ConversationRole,
    ChatStreamDataType,
    user_message,
    ai_message,
)
from .utils.helpers import new_base64_wox_image
from .exceptions import WoxPluginError, InvalidQueryError, PluginInitError, APIError


__version__: str = "0.1.0"
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
    "PluginSettingDefinitionValue",
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
    # Utils
    "new_base64_wox_image",
    # Exceptions
    "WoxPluginError",
    "InvalidQueryError",
    "PluginInitError",
    "APIError",
]
