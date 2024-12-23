# Python Wikimedia Enterprise Model Context Protocol Implementation

This is not the official MCP implementation for the Wikimedia Enterprise API.

##

To run make a .env file in this directory with `WME_USERNAME` and `WME_PASSWORD` (you can get free credentials at https://enterprise.wikimedia.com/).

Currently to use this you need to install Anthropic Desktop and then add it to your `claude_desktop_config.json`.

A sample json would look like:

```json
{
  "mcpServers": {
    "wikimedia-enterprise": {
      "command": "/path/to/wikimedia-enterprise-mcp/start.sh"
    }
  }
}
```

### Installation
Git clone the repo. You need to have `poetry` installed to manage the dependencies (and a modern version of python). 

## Testing

For testing make a `.env` file with `WME_USERNAME` and `WME_PASSWORD`.

Install the pre-commit hooks with `poetry run pre-commit install` or just run them manually e.g. `poetry run ruff check`
