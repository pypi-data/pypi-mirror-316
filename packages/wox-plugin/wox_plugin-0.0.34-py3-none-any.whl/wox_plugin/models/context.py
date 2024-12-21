import uuid
from dataclasses import dataclass, field
from typing import Dict
from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Context:
    """
    Context object that carries request-scoped values across the plugin execution
    """

    values: Dict[str, str] = field(default_factory=dict)

    def get_trace_id(self) -> str:
        """Get the trace ID from context"""
        return self.values["traceId"]

    @staticmethod
    def new() -> "Context":
        """Create a new context with a random trace ID"""
        return Context(values={"traceId": str(uuid.uuid4())})

    @staticmethod
    def new_with_value(key: str, value: str) -> "Context":
        """Create a new context with a specific key-value pair"""
        ctx = Context.new()
        ctx.values[key] = value
        return ctx
