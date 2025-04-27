import httpx
from pydantic import Field

from src.argus.tools.tool import Tool


class GetWeather(Tool):
    """Get current temperature for a given location using latitude and longitude coordinates."""

    latitude: str = Field(
        ..., description='Latitude coordinate (e.g. 4.6097 for Bogotá)'
    )
    longitude: str = Field(
        ..., description='Longitude coordinate (e.g. -74.0817 for Bogotá)'
    )

    def resolve(self) -> str:
        response = httpx.get(
            f'https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m'
        )
        data = response.json()
        return str(data['current']['temperature_2m'])
