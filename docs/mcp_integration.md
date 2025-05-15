# MCP Integration Guide

This guide explains how to integrate the Salesforce/nCino Analyzer with Claude using the Model Context Protocol (MCP).

## Understanding Model Context Protocol (MCP)

The Model Context Protocol (MCP) is an open standard for connecting AI models to external tools, data, and capabilities. It allows Claude to directly leverage the specialized analysis capabilities of the Salesforce/nCino Analyzer without having to implement them in prompts.

## Setting Up the MCP Server

### Prerequisites

- Python 3.9 or later
- Salesforce CLI (optional, for direct metadata extraction)
- Claude API key (for using Claude)
- Basic understanding of Salesforce/nCino metadata

### Installation

```bash
# Clone the repository
git clone https://github.com/ncinotimo/Salesforce-Analyser-Py.git
cd Salesforce-Analyser-Py

# Set up a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file with the following settings:

```
MCP_API_KEY=your_mcp_api_key
CLAUDE_API_KEY=your_claude_api_key
PORT=3000
```

### Starting the Server

```bash
python mcp_server.py
```

## Connecting to Claude

There are two main ways to connect the MCP server to Claude:

### Option 1: Using the MCP Inspector

1. Navigate to [https://inspector.modelcontextprotocol.io/](https://inspector.modelcontextprotocol.io/)
2. Enter your MCP server URL (e.g., `http://localhost:3000`)
3. Enter your MCP API key
4. Enter your Claude API key
5. Test the connection and explore available resources and tools

### Option 2: Connecting Directly to Claude

1. Navigate to Claude's desktop app
2. Select the "Connect to MCP" option from the settings menu
3. Enter your MCP server URL and API key
4. Start a new conversation to use the Salesforce/nCino Analyzer capabilities

## Available Resources

The MCP server exposes the following resources:

| Resource ID | Description |
|-------------|-------------|
| `salesforce.fields` | Field definitions from Salesforce/nCino objects |
| `salesforce.validationRules` | Validation rule definitions |
| `salesforce.triggers` | Apex trigger definitions |

## Available Tools

The MCP server provides the following tools:

| Tool ID | Description |
|---------|-------------|
| `salesforce.extractMetadata` | Extract metadata from a Salesforce org |
| `salesforce.analyzeNamingConventions` | Analyze field naming conventions |
| `salesforce.analyzeValidationRules` | Analyze validation rule bypass patterns |
| `salesforce.analyzeApexTriggers` | Analyze Apex trigger bypass patterns |
| `salesforce.generateReport` | Generate a comprehensive report |

## Available Prompt Templates

The MCP server includes these prompt templates:

| Template ID | Description |
|-------------|-------------|
| `salesforce.basicAnalysis` | Basic analysis of Salesforce/nCino configuration |
| `salesforce.securityAnalysis` | Security-focused analysis |

## Using the MCP Server with Claude

Once connected, you can ask Claude to analyze your Salesforce/nCino configurations using natural language. For example:

```
Can you analyze the naming conventions in my Salesforce fields? I've uploaded them to the MCP server.
```

```
Please check my validation rules for security bypass patterns using the MCP tools.
```

```
Can you generate a comprehensive report on my Salesforce/nCino configuration using the MCP tools? Please focus on security issues.
```

## Example Workflow

1. Start the MCP server: `python mcp_server.py`
2. Connect to Claude via the MCP Inspector or directly
3. Upload your Salesforce metadata to the MCP server
4. Ask Claude to analyze your configuration
5. Review the results and ask follow-up questions

## Advanced Usage: Using the MCP Client

For programmatic access to the MCP server, you can use the MCP client:

```python
from mcp import MCPClient

async def analyze_salesforce():
    client = MCPClient(
        api_key="your_mcp_api_key",
        server_url="http://localhost:3000",
        claude_api_key="your_claude_api_key"
    )
    
    await client.connect()
    
    results = await client.call_tool("salesforce.analyzeNamingConventions", {
        "fields": your_fields_data
    })
    
    print(results)
    
    await client.disconnect()
```

See the `mcp_client.py` file for a complete example.

## Troubleshooting

### Server Won't Start

- Check if the port is already in use
- Verify Python version compatibility
- Ensure all dependencies are installed

### Connection Issues

- Verify MCP API key is correct
- Check network connectivity to the server
- Ensure the server is running

### Analysis Errors

- Check that metadata is correctly formatted
- Verify permissions for Salesforce API access
- Look at server logs for detailed error information

## Best Practices

1. **Data Security**: Always use API keys to secure your MCP server
2. **Error Handling**: Implement robust error handling for Salesforce API calls
3. **Metadata Quality**: Ensure metadata is properly extracted and formatted
4. **Prompt Design**: Use clear, specific prompts when interacting with Claude
5. **Resource Management**: Monitor server performance when analyzing large metadata sets