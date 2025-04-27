from typing import Mapping

from src.argus.exception import ToolNotFound
from src.argus.tools.registry import ToolsRegistry
from src.argus.tools.tool import Tool

from ._get_datetime import GetDatetime
from ._get_weather import GetWeather


class BaseRegistry(ToolsRegistry):
    """
    The base registry for managing general purpose tools
    """

    _tool_classes: list[type[Tool]] = [GetWeather, GetDatetime]

    def __init__(self) -> None:
        self._tools = {
            tool.__name__: tool for tool in BaseRegistry._tool_classes
        }

    @property
    def tools(self) -> Mapping[str, type[Tool]]:
        """Get all tools"""
        return self._tools

    def get_tool_by_name(self, tool_name: str) -> type[Tool]:
        """Get a specific tool class"""
        if tool_name in self._tools:
            return self._tools[tool_name]
        raise ToolNotFound(tool_name)
