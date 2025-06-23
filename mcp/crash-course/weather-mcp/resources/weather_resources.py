"""MCP weather resources."""

from datetime import datetime
from data.mock_data import MOCK_WEATHER_DATA
from mcp.server.fastmcp import FastMCP

# ============================================================================= #
# RESOURCES - Static weather information and context                            #
# ============================================================================= #

def register_weather_resources(mcp: FastMCP):
    """Register all weather resources with the MCP server."""

    @mcp.resource("weather://locations")
    def available_locations() -> str:
        """List all available weather locations with basic info."""
        result = "📍 Available Weather Locations:\n\n"
        
        for location, data in MOCK_WEATHER_DATA.items():
            current = data["current"]
            result += f"**{location.replace('_', ' ').title()}**\n"
            result += f"Current: {current['temperature']}°F, {current['conditions']}\n"
            result += f"Humidity: {current['humidity']}%, Wind: {current['wind_speed']} mph\n\n"
        
        return result


    @mcp.resource("weather://location/{location}")
    def location_summary(location: str) -> str:
        """Get detailed weather summary for a specific location."""
        location_key = location.lower().replace(" ", "_")
        
        if location_key not in MOCK_WEATHER_DATA:
            return f"Location '{location}' not found. Available: {', '.join(MOCK_WEATHER_DATA.keys())}"
        
        data = MOCK_WEATHER_DATA[location_key]
        current = data["current"]
        
        result = f"📊 Weather Summary for {location.replace('_', ' ').title()}\n\n"
        result += f"**Current Conditions** (as of {datetime.now().strftime('%H:%M')})\n"
        result += f"Temperature: {current['temperature']}°F\n"
        result += f"Conditions: {current['conditions']}\n"
        result += f"Humidity: {current['humidity']}%\n"
        result += f"Wind: {current['wind_speed']} mph {current['wind_direction']}\n"
        result += f"Pressure: {current['pressure']} mb\n"
        result += f"Visibility: {current['visibility']} miles\n"
        result += f"UV Index: {current['uv_index']}\n\n"
        
        result += "**5-Day Outlook**\n"
        for day in data["forecast"]:
            result += f"{day['day']}: {day['high']}°/{day['low']}° - {day['conditions']} ({day['precipitation']}% rain)\n"
        
        return result


    @mcp.resource("weather://alerts/general")
    def weather_alerts() -> str:
        """General weather alerts and advisories."""
        return """🚨 Weather Alerts & Advisories

    ⚠️ **General Weather Safety Tips:**
    - Always check local weather before outdoor activities
    - Monitor UV index for sun exposure guidance
    - Stay hydrated in high temperatures
    - Be cautious of sudden weather changes

    🌩️ **Severe Weather Guidelines:**
    - Seek shelter during thunderstorms
    - Avoid outdoor activities during heavy rain
    - Monitor wind speeds for travel safety
    - Check visibility conditions before driving

    📱 **Stay Informed:**
    - Weather conditions can change rapidly
    - Always verify with local meteorological services
    - Consider multiple weather sources for important decisions

    Last updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S')