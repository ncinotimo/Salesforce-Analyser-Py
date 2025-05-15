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

3. Set up environment variables (or use Claude Desktop's environment variable UI):
   ```bash
   # Create a .env file
   echo "MCP_API_KEY=your_custom_api_key" > .env
   echo "PORT=3000" >> .env
   ```

## Connecting to Claude Desktop

### Method 1: Using the Configuration File

1. Open Claude Desktop
2. Go to Settings > Integrations > Add Integration
3. Select "From Configuration File"
4. Browse to and select the `claude_desktop_config.json` file from this repository
5. Follow the setup instructions in the UI

### Method 2: Manual Configuration

1. Open Claude Desktop
2. Go to Settings > Integrations > Add Integration
3. Select "MCP Server"
4. Enter the following details:
   - Name: Salesforce/nCino Analyzer
   - Description: Analyze Salesforce/nCino configurations for naming conventions and security patterns
   - URL: http://localhost:3000 (or your custom port)
   - API Key: Your MCP API key from the .env file
5. Save the configuration

## Starting the Server

Before you can use the analyzer in Claude Desktop, you need to start the MCP server:

```bash
# Start the MCP server
python mcp_server.py
```

You should see output indicating that the server is running on the specified port.

## Using the Integration in Claude Desktop

Once the integration is set up and the server is running, you can use the Salesforce/nCino Analyzer in your conversations with Claude.

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

### Server Connection Issues

If Claude can't connect to the MCP server:

1. Verify the server is running (`python mcp_server.py`)
2. Check that the port matches in both the server and Claude Desktop configuration
3. Ensure the API keys match
4. Check for any firewall issues

### File Format Issues

If Claude has trouble processing your metadata files:

1. Make sure the files are in supported formats (JSON, XML, CSV)
2. Check that the file structure matches the expected format
3. Try using a smaller subset of data first

### Integration Not Appearing

If the Salesforce/nCino Analyzer integration doesn't appear in Claude Desktop:

1. Verify the `claude_desktop_config.json` file is properly formatted
2. Restart Claude Desktop
3. Check the Claude Desktop logs for any errors

## Best Practices

1. **Start Simple**: Begin with simple analyses and then move to more complex ones
2. **Organize Files**: Keep your metadata files well-organized by type
3. **Be Specific**: Ask Claude specific questions about the analysis results
4. **Follow Up**: Use follow-up questions to dig deeper into findings
5. **Save Reports**: Save important analysis results from Claude for later reference

## Limitations

- Claude Desktop must be able to access localhost (or wherever the MCP server is running)
- Large metadata files may take longer to process
- Some visualization capabilities depend on Claude Desktop's rendering abilities

## Getting Help

If you encounter issues:

1. Check the [GitHub repository](https://github.com/ncinotimo/Salesforce-Analyser-Py) for updates
2. Review the documentation in the `docs` directory
3. Submit an issue on GitHub if you find a bug
