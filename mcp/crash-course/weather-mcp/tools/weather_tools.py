"""MCP tools for weather data."""

from datetime import datetime
from typing import Optional
from data.mock_data import MOCK_WEATHER_DATA

from mcp.server.fastmcp import FastMCP

# ============================================================================= #
# TOOLS - Interactive functions for getting weather data                        #
# ============================================================================= #

def register_weather_tools(mcp: FastMCP):
    """Register all weather tools with the MCP server."""

    @mcp.tool()
    def get_current_weather(location: str) -> str:
        """Get current weather conditions for a specific location.
        
        Args:
            location: The city name (e.g., 'new_york', 'london', 'tokyo')
        
        Returns:
            Current weather information as a formatted string
        """
        location_key = location.lower().replace(" ", "_").replace(",", "")
        
        if location_key not in MOCK_WEATHER_DATA:
            return f"Weather data not available for {location}. Available locations: {', '.join(MOCK_WEATHER_DATA.keys())}"
        
        current = MOCK_WEATHER_DATA[location_key]["current"]
        
        return f"""Current Weather in {location.title()}:
    🌡️  Temperature: {current['temperature']}°F
    💧 Humidity: {current['humidity']}%
    🌤️  Conditions: {current['conditions']}
    💨 Wind: {current['wind_speed']} mph {current['wind_direction']}
    📊 Pressure: {current['pressure']} mb
    👁️  Visibility: {current['visibility']} miles
    ☀️ UV Index: {current['uv_index']}

    Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""


    @mcp.tool()
    def get_weather_forecast(location: str, days: int = 5) -> str:
        """Get weather forecast for a specific location.
        
        Args:
            location: The city name (e.g., 'new_york', 'london', 'tokyo')
            days: Number of days to forecast (1-5, default: 5)
        
        Returns:
            Weather forecast as a formatted string
        """
        location_key = location.lower().replace(" ", "_").replace(",", "")
        
        if location_key not in MOCK_WEATHER_DATA:
            return f"Weather data not available for {location}. Available locations: {', '.join(MOCK_WEATHER_DATA.keys())}"
        
        if days < 1 or days > 5:
            return "Forecast days must be between 1 and 5"
        
        forecast = MOCK_WEATHER_DATA[location_key]["forecast"][:days]
        
        result = f"📅 {days}-Day Weather Forecast for {location.title()}:\n\n"
        
        for day_data in forecast:
            result += f"**{day_data['day']}**\n"
            result += f"🌡️ High: {day_data['high']}°F | Low: {day_data['low']}°F\n"
            result += f"🌤️ Conditions: {day_data['conditions']}\n"
            result += f"🌧️ Precipitation: {day_data['precipitation']}%\n\n"
        
        return result


    @mcp.tool()
    def compare_weather(location1: str, location2: str) -> str:
        """Compare current weather between two locations.
        
        Args:
            location1: First city name
            location2: Second city name
        
        Returns:
            Weather comparison as a formatted string
        """
        loc1_key = location1.lower().replace(" ", "_").replace(",", "")
        loc2_key = location2.lower().replace(" ", "_").replace(",", "")
        
        if loc1_key not in MOCK_WEATHER_DATA:
            return f"Weather data not available for {location1}"
        
        if loc2_key not in MOCK_WEATHER_DATA:
            return f"Weather data not available for {location2}"
        
        weather1 = MOCK_WEATHER_DATA[loc1_key]["current"]
        weather2 = MOCK_WEATHER_DATA[loc2_key]["current"]
        
        temp_diff = weather1["temperature"] - weather2["temperature"]
        humidity_diff = weather1["humidity"] - weather2["humidity"]
        
        result = f"🌍 Weather Comparison\n\n"
        result += f"**{location1.title()}** vs **{location2.title()}**\n\n"
        result += f"🌡️ Temperature: {weather1['temperature']}°F vs {weather2['temperature']}°F "
        result += f"({'+' if temp_diff > 0 else ''}{temp_diff}°F difference)\n"
        result += f"💧 Humidity: {weather1['humidity']}% vs {weather2['humidity']}% "
        result += f"({'+' if humidity_diff > 0 else ''}{humidity_diff}% difference)\n"
        result += f"🌤️ Conditions: {weather1['conditions']} vs {weather2['conditions']}\n"
        result += f"💨 Wind: {weather1['wind_speed']} mph vs {weather2['wind_speed']} mph\n"
        
        return result