"""MCP weather prompts."""

from mcp.server.fastmcp import FastMCP

# ============================================================================= # 
# PROMPTS - Templates for weather-related interactions                          #
# ============================================================================= #
    
def register_weather_prompts(mcp: FastMCP):
    """Register all weather prompts with the MCP server."""

    @mcp.prompt()
    def weather_report_prompt(location: str, include_forecast: bool = True) -> str:
        """Generate a comprehensive weather report prompt.
        
        Args:
            location: The location for the weather report
            include_forecast: Whether to include forecast information
        """
        prompt = f"""Please provide a comprehensive weather report for {location}. 

    Include the following information:
    1. Current weather conditions with detailed observations
    2. Temperature analysis and comfort level assessment
    3. Wind and atmospheric pressure conditions
    4. Visibility and UV index implications
    """
        
        if include_forecast:
            prompt += """5. 5-day forecast with trend analysis
    6. Recommendations for outdoor activities
    7. Any weather-related advisories or precautions"""
        
        prompt += f"""

    Use the weather tools available to gather current data for {location} and present it in a clear, informative manner suitable for planning daily activities."""
        
        return prompt


    @mcp.prompt()
    def travel_weather_prompt(departure_location: str, destination_location: str, travel_date: str = "today") -> str:
        """Generate a travel weather planning prompt.
        
        Args:
            departure_location: Starting location
            destination_location: Destination location  
            travel_date: Date of travel (default: today)
        """
        return f"""Please help me plan for weather conditions during my travel from {departure_location} to {destination_location} on {travel_date}.

    Provide a detailed travel weather analysis including:

    1. **Departure Weather**: Current conditions in {departure_location}
    - Temperature and comfort level for departure
    - Any weather conditions that might affect travel departure

    2. **Destination Weather**: Current conditions in {destination_location}  
    - Expected weather upon arrival
    - Temperature differences to prepare for
    - Any significant weather differences from departure location

    3. **Travel Recommendations**:
    - Appropriate clothing suggestions based on both locations
    - Weather-related travel considerations
    - Any weather precautions for the journey

    4. **Packing Suggestions**: Based on weather differences between locations

    Use the available weather comparison tools to analyze both locations and provide practical travel advice."""


    @mcp.prompt()
    def weather_activity_prompt(location: str, activity_type: str) -> str:
        """Generate a weather-appropriate activity planning prompt.
        
        Args:
            location: Location for the activity
            activity_type: Type of activity (outdoor, sports, event, etc.)
        """
        return f"""Help me plan {activity_type} activities in {location} based on current and forecasted weather conditions.

    Please analyze:

    1. **Current Weather Suitability**
    - Is the current weather appropriate for {activity_type}?
    - What are the comfort levels and safety considerations?
    - Any immediate weather concerns?

    2. **Forecast Analysis** 
    - Best days/times for {activity_type} in the coming forecast
    - Weather trends that might affect activity planning
    - Any days to avoid for {activity_type}

    3. **Specific Recommendations**
    - Optimal timing for {activity_type} based on weather
    - Suggested preparations or equipment needed
    - Alternative indoor options if weather is unsuitable

    4. **Safety Considerations**
    - UV exposure concerns for outdoor activities
    - Wind, temperature, or precipitation warnings
    - Visibility or atmospheric conditions to monitor

    Use current weather data and forecasts to provide practical, safety-conscious activity planning advice."""