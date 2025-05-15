# Using with Claude Desktop

This guide explains how to use the Salesforce/nCino Analyzer with Claude Desktop.

## Claude Desktop Integration

Claude Desktop is an application that allows you to use Claude locally with access to tools and resources through the Model Context Protocol (MCP). The Salesforce/nCino Analyzer is designed to integrate seamlessly with Claude Desktop.

## Setup Instructions

### Prerequisites

- Claude Desktop application installed
- Python 3.9 or later
- Salesforce CLI (optional, for direct metadata extraction)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ncinotimo/Salesforce-Analyser-Py.git
   cd Salesforce-Analyser-Py
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure Claude Desktop to run the MCP server.

## Configuring Claude Desktop

Claude Desktop uses a configuration file to manage MCP servers. You have two options for configuration:

### Option 1: Use the Provided Configuration File

1. Locate the Claude Desktop configuration directory (typically in your user profile)
2. Copy the `claude_desktop_config.json` file from this repository to that location
3. Edit the file to update paths and environment variables as needed

### Option 2: Add to Existing Configuration

If you already have a Claude Desktop configuration file, add the Salesforce Analyzer to it:

```json
{
    "mcpServers": {
        "existing-server": { ... },
        
        "salesforce-analyzer": {
            "command": "python",
            "args": [
                "-m",
                "mcp_server.py"
            ],
            "env": {
                "MCP_API_KEY": "your_mcp_api_key_here",
                "PORT": "3000"
            }
        }
    }
}
```

### Important Configuration Settings

- **command**: Specifies the command to run the server (usually `python`)
- **args**: The arguments to pass to the command (the path to `mcp_server.py`)
- **env**: Environment variables needed by the server:
  - **MCP_API_KEY**: Your custom API key for security
  - **PORT**: The port to run the server on (default: 3000)

## Using the Salesforce Analyzer in Claude Desktop

Once configured, Claude Desktop will automatically start the Salesforce Analyzer MCP server when needed.

### Example Prompts

1. **Basic Analysis**:
   ```
   Can you analyze my Salesforce field naming conventions? I'll upload the metadata file now.
   ```

2. **Security Analysis**:
   ```
   I want to check my validation rules for security bypass patterns. Please use the Salesforce/nCino Analyzer to help me.
   ```

3. **Extract and Analyze**:
   ```
   I'd like to extract metadata from my Salesforce org and analyze it. Here's my access token: [token]. The instance URL is: [url].
   ```

4. **Comprehensive Report**:
   ```
   Please generate a comprehensive report on all aspects of my Salesforce/nCino configuration. I've already uploaded the metadata files.
   ```

### Uploading Files

When you need to provide metadata files to Claude:

1. Click the upload button in the Claude Desktop interface
2. Select your Salesforce metadata files (JSON, XML, or CSV)
3. Ask Claude to analyze the uploaded files

### Viewing Results

Claude will display the analysis results directly in the chat. The results may include:

- Executive summaries
- Detailed findings
- Recommendations
- Visualizations (if supported by Claude Desktop)

## Troubleshooting

### MCP Server Not Starting

If the MCP server doesn't start:

1. Make sure the path to `mcp_server.py` is correct in your configuration
2. Check that all dependencies are installed
3. Verify Python is in your PATH
4. Look at the Claude Desktop logs for error messages

### Connection Issues

If Claude can't connect to the MCP server:

1. Check that the port specified in the configuration is available
2. Ensure the API keys match between Claude Desktop and the server
3. Check for any firewall issues

### File Format Issues

If Claude has trouble processing your metadata files:

1. Make sure the files are in supported formats (JSON, XML, CSV)
2. Check that the file structure matches the expected format
3. Try using a smaller subset of data first

## Best Practices

1. **Start Simple**: Begin with simple analyses and then move to more complex ones
2. **Organize Files**: Keep your metadata files well-organized by type
3. **Be Specific**: Ask Claude specific questions about the analysis results
4. **Follow Up**: Use follow-up questions to dig deeper into findings
5. **Save Reports**: Save important analysis results from Claude for later reference

## Limitations

- Claude Desktop must be able to start Python processes
- Large metadata files may take longer to process
- Some visualization capabilities depend on Claude Desktop's rendering abilities

## Getting Help

If you encounter issues:

1. Check the [GitHub repository](https://github.com/ncinotimo/Salesforce-Analyser-Py) for updates
2. Review the documentation in the `docs` directory
3. Submit an issue on GitHub if you find a bug
