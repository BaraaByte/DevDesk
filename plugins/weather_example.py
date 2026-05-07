"""
Example: Weather Widget Plugin
Fetches weather data and displays it in a widget
"""

from plugins.base import DevDeskPlugin
from typing import Dict, Any
import httpx


class WeatherPlugin(DevDeskPlugin):
    """Display current weather information"""
    
    name = "Weather"
    version = "1.0.0"
    author = "DevDesk Community"
    description = "Display current weather information"
    
    def __init__(self, city: str = "New York", units: str = "celsius"):
        super().__init__()
        self.city = city
        self.units = units
        self.api_url = "https://api.open-meteo.com/v1/forecast"
    
    async def get_data(self) -> Dict[str, Any]:
        """Fetch weather data from Open-Meteo API (free, no key required)"""
        try:
            # Get coordinates for city (simplified - use proper geocoding in production)
            # For demo: New York (40.7128, -74.0060)
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.api_url,
                    params={
                        "latitude": 40.7128,
                        "longitude": -74.0060,
                        "current": "temperature_2m,weather_code,wind_speed_10m",
                        "temperature_unit": self.units.capitalize()
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    current = data.get("current", {})
                    
                    return {
                        "temperature": current.get("temperature_2m"),
                        "condition": self._decode_weather(current.get("weather_code")),
                        "wind_speed": current.get("wind_speed_10m"),
                        "city": self.city,
                        "units": self.units
                    }
        except Exception as e:
            print(f"Weather API error: {e}")
        
        return {"error": "Failed to fetch weather data"}
    
    def get_component_name(self) -> str:
        return "WeatherWidget"
    
    def _decode_weather(self, code: int) -> str:
        """Decode WMO weather code"""
        codes = {
            0: "Clear",
            1: "Mostly Clear",
            2: "Partly Cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy",
            51: "Light Drizzle",
            53: "Moderate Drizzle",
            55: "Heavy Drizzle",
            61: "Slight Rain",
            63: "Moderate Rain",
            65: "Heavy Rain",
            71: "Slight Snow",
            73: "Moderate Snow",
            75: "Heavy Snow",
            80: "Slight Rain Showers",
            81: "Moderate Rain Showers",
            82: "Violent Rain Showers",
            85: "Slight Snow Showers",
            86: "Heavy Snow Showers",
            95: "Thunderstorm",
            96: "Thunderstorm with Hail",
            99: "Thunderstorm with Hail"
        }
        return codes.get(code, "Unknown")
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate weather plugin configuration"""
        required_fields = ["city"]
        return all(field in config for field in required_fields)


# Example usage
if __name__ == "__main__":
    import asyncio
    
    plugin = WeatherPlugin(city="San Francisco")
    data = asyncio.run(plugin.get_data())
    print(f"Weather data: {data}")
