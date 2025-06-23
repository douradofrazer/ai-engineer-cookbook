# Setting Up Your First MCP

In this guide, I'll help you build a Weather MCP (Model Control Protocol). A simple program that can tell you about the weather. We'll use fake weather data so you can focus on learning how MCPs work.

## 🚀 Getting Started

### How to Set Up

Let's begin by cloning the repository [here](../weather-mcp/).

Once in the directory, run the following commands in order:
```shell
uv venv  # Sets up a virtual environment
uv sync  # Synchronizes dependencies
```

Ensure you have `uv` installed before proceeding. And with that, you're all set to get started.

Now, before running the server, let's inspect the code. Starting with `server.py`, which is the main entry point.

[server.py](../weather-mcp/server.py)
```python
...
mcp = FastMCP("Weather MCP Server") # Creates the MCP server

register_weather_tools(mcp) # registers the tools
...
```

The python SDK uses FastMCP 1.0 which is a framework for building MCP servers and clients. </br>
It's as easy as that to setup a MCP server. Now you need some primitives, which are setup in `register_weather_tools(...)`

We the have 3 tools setup in [weather_tools.py](../weather-mcp/tools/weather_tools.py)

```python

...

    @mcp.tool()
    def get_current_weather(location: str) -> str:
        ...

    @mcp.tool()
    def get_weather_forecast(location: str, days: int = 5) -> str:
        ...

    @mcp.tool()
    def compare_weather(location1: str, location2: str) -> str:
        ...
...

```

`@mcp.tool()` helps convert a python function into a MCP tool.

With that you're now ready to run the inspector and test the MCP out.

```bash
# Test with MCP Inscpector
uv run mcp dev server.py
```

you should see these logs on running the `dev` command:
```
Starting MCP inspector...
⚙️ Proxy server listening on port 6277
🔍 MCP Inspector is up and running at http://127.0.0.1:6274 🚀
```

Watch this quick demo of the MCP Inspector in action to see how to test your weather tools.

<video width="80%" controls>
  <source src="mcp-inspector-tools-demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

### Installing the Server

Running the command below setups your server with Claude desktop.

> Note: Ensure to exit and reload claude desktop after installation of the server.

```bash
# Install the server into claude
uv run mcp install server.py --name "Weather MCP"
```

After installing the server, you should see the Weather MCP tools available in Claude Desktop:

<video width="50%" controls>
  <source src="claude-mcp-tools-demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

</br>

After completing this module, you should have:
- ✅ A working MCP server
- ✅ Basic weather fetching functionality
- ✅ Development environment set up

## 📝 What's Next?

Let's expand on this example and add more privitives supported by clients like Claude Desktop.

</br>

[Next Chapter ➡](../4-advanced-setup/README.md)