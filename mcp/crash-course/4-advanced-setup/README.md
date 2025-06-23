# Enhancing Your MCP with Advanced Features

Now that you have a working MCP server with basic weather functionality, let's explore the additional capabilities that make MCP powerful for production use. We'll add prompts, resources, and improved tooling to create a more robust and feature-rich implementation.

Here's the complete project structure we'll be working with:
```
weather-mcp/
├── server.py                  # Main MCP server implementation
├── pyproject.toml             # Project dependencies and configuration
├── README.md                  # Project documentation
├── uv.lock                    # Dependency lock file
├── prompts/                   # MCP prompt definitions
│   ├── weather_prompts.py     # Weather-specific prompts
│   └── __init__.py
├── tools/                     # MCP tools implementation
│   ├── weather_tools.py       # Weather-specific tools
│   └── __init__.py
├── data/                      # Data directory
│   ├── mock_data.py           # Mock weather data
│   └── __init__.py
├── resources/                 # Resource files
│   ├── weather_resources.py   # Weather-specific resources
│   └── __init__.py
```

## Enabling Resources

Resources in MCP provide static information and context that can be accessed by tools and prompts. 
Let's enable them by uncommenting `register_weather_resources(...)` in `server.py`.

This registers three key resources that enhance our weather MCP:

```python
...
    @mcp.resource("weather://locations")
    def available_locations() -> str:
        ...
    @mcp.resource("weather://location/{location}")
    def location_summary(location: str) -> str:
        ...
    @mcp.resource("weather://alerts/general")
    def weather_alerts() -> str:
        ...
...
```

## Enabling Prompts

Prompts in MCP provide templates for structured interactions with the AI. Let's enable them by uncommenting `register_weather_prompts(...)` in `server.py`.

This registers two key prompts that enhance our weather MCP:

```python
...
    @mcp.prompt()
    def weather_report_prompt(location: str, include_forecast: bool = True) -> str:
        ...
    @mcp.prompt()
    def travel_weather_prompt(departure_location: str, destination_location: str, travel_date: str = "today") -> str:
        ...
    @mcp.prompt()
    def weather_activity_prompt(location: str, activity_type: str) -> str:
        ...
...
```

## Inspect your resources & prompts

```bash
# Test with MCP Inscpector
uv run mcp dev server.py
```

<video width="80%" controls>
  <source src="mcp-inspector-resources-prompts-demo.mp4" type="video/mp4">
</video>

### Install the MCP server

```bash
# Install the server into claude
uv run mcp install server.py --name "Weather MCP"
```

> Note: Ensure to exit and reload claude desktop after installation of the server.

After installing the server, you should see the Weather MCP tools, resources and prompts available in Claude Desktop:

<video width="80%" controls>
  <source src="claude-mcp-prompts-resources-demo.mp4" type="video/mp4">
</video>

</br>

After completing this module, you should have:
- ✅ A working MCP server with tools, resouces and prompts
- ✅ Fully integrated with Claude desktop
- ✅ Have a complete understanding of how to build an MCP from scratch and use it's primitives.

## 📝 Course Completion

Congratulations! You've now completed the MCP Crash Course. You've learned:

1. How to set up an MCP
2. How to create and use MCP tools
3. How to add resources to your MCP
4. How to create prompts for structured interactions
5. How to test and deploy your MCP with Claude Desktop

### Next Steps

Here are some suggestions for what to do next:

1. **Explore More Examples**: Check out [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers) for more complex MCP implementations
2. **Build Your Own MCP**: Start building your own MCP for a specific use case

Happy building! 🚀 Star the repository and stay tuned for more content!