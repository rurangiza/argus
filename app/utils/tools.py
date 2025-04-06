"""Tools registry and utility functions for tool descriptions."""

from collections import defaultdict

import httpx
from app.models import ToolDescription


class ToolsRegistry():
    tools: dict = defaultdict()

    @classmethod
    def get_descriptions(cls):
        return [v["description"] for _, v in cls.tools.items()]

    @classmethod
    def get_all(cls):
        return cls.tools


def generate_openai_tool_description(func_name, descriptions: ToolDescription):
  """Generate OpenAI tool description format from function name and description."""
  full_description = {
    "type": "function",
    "function": {
        "name": func_name,
        "description": descriptions['short'],
        "parameters": {
          "type": "object",
          "properties": {},
          "required": [],
          "additionalProperties": False
        }
    }
  }
  
  if descriptions["params"]:
    full_description["function"]["parameters"]["properties"] = descriptions["params"]
    full_description["function"]["parameters"]["required"] = list(descriptions["params"].keys())
    
  return full_description

def register_tool(d: ToolDescription):
    """Register a tool with its description in the tools registry."""
    def decorator(func):
        ToolsRegistry.tools[func.__name__] = {
            "function": func,
            "description": generate_openai_tool_description(func.__name__, d)
        }
        return func
    return decorator


"""
TOOLS DEFINItION
"""

@register_tool({
    "short": "Get current temperature for a given location.",
    "params": {
      "latitude": {
        "description": "Latitude coordinate (e.g. 4.6097 for Bogotá)",
        "type": "string",
      },
      "longitude": {
        "description": "Longitude coordinate (e.g. -74.0817 for Bogotá)",
        "type": "string",
      },
    }
})
def get_weather(latitude, longitude):
    """Get current temperature for a given location using latitude and longitude coordinates."""
    response = httpx.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']