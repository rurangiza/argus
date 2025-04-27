from abc import ABC, abstractmethod
from typing import Mapping

from .tool import Tool


class ToolsRegistry(ABC):
    """
    A registry for managing and retrieving available Tool classes

    This class maintains a mapping from tool names to their corresponding classes,
    allowing tools to be accessed by name or described using a Pydantic-compatible format.

    Attributes:
        _tool_classes (list[type[Tool]]):
            A class-level list containing all Tool subclasses to be registered.
        _tools (dict[str, type[Tool]]):
            An instance-level dictionary mapping tool names to Tool classes.

    Properties:
        tools (list):
            Returns a the full list of tool.

    Methods:
        get_tool_by_name(tool_name: str) -> type[Tool]:
            Retrieves a specific Tool class by its registered name.
            Raises ToolNotFound if the name does not exist in the registry.
    """

    _tool_classes: list[type[Tool]]

    @property
    @abstractmethod
    def tools(self) -> Mapping[str, type[Tool]]:
        """Get all tools"""
        pass

    @abstractmethod
    def get_tool_by_name(self, tool_name: str) -> type[Tool]:
        """Get a specific tool class"""
        pass
