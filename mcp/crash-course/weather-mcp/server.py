"""
Weather MCP Server
"""

from resources.weather_resources import register_weather_resources
from tools.weather_tools import register_weather_tools
from prompts.weather_prompts import register_weather_prompts
from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("Weather MCP Server")

# Register all components
register_weather_tools(mcp)
# register_weather_resources(mcp)
# register_weather_prompts(mcp)


# ============================================================================= # 
# MAIN SERVER ENTRY POINT                                                       #
# ============================================================================= #

def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()