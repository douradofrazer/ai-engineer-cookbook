# Weather MCP

This is a demo MCP (Model Context Protocol) server that you will build during the course to help you solidify your fundamentals learned in Chapter 2.

## Overview

The Weather MCP provides weather-related tools, resources, and prompts that can be integrated with MCP-compatible clients like Claude Desktop. It demonstrates the core concepts of building an MCP server including:

- **Tools**: Weather data retrieval and processing
- **Resources**: Weather information and forecasts
- **Prompts**: Context-aware weather assistance

## Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager

## Setup

After cloning the repository, follow these steps to set up the Weather MCP:

### 1. Navigate to the project directory
```bash
cd mcp/crash-course/weather-mcp
```

### 2. Create a virtual environment
```bash
uv venv
```

### 3. Install dependencies
```bash
uv sync
```

## Usage

### Running & Installing the MCP Server

Start the Weather MCP server:

```bash
uv run mcp install server.py --name "Weather MCP"
```
