"""Tools registry and utility functions for tool descriptions."""

from abc import ABC, abstractmethod

from pydantic import BaseModel


class Tool(BaseModel, ABC):
    @classmethod
    def description(cls) -> str | None:
        """Get the description of the tool"""
        return cls.__doc__

    @abstractmethod
    def resolve(self) -> str:
        """Resolve the tool"""
        pass
