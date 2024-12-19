# MCP-timeserver

A simple MCP server that exposes datetime information to agentic systems and chat REPLs

## Components

### Resources

The server implements a simple datetime:// URI scheme for accessing the current date/time in a given timezone, for example:
```
datetime://Africa/Freetown/now
datetime://Europe/London/now
datetime://America/New_York/now
```

### Tools

The server exposes a tool to get the current local time in the system timezone:
```python
>>> get_current_time()
"The current time is 2024-12-18 19:59:36"
```

## Quickstart

### Install

use the following json

```json
{
  "mcpServers": {
    "MCP-timeserver": {
      "command": "uvx",
      "args": ["MCP-timeserver"]
    }
  }
}
```
