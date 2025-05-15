# Salesforce-Analyser-Py

A Python-based Salesforce/nCino analyzer using Model Context Protocol (MCP) for integration with Claude Desktop and other LLMs.

## Overview

This project implements an MCP server that provides specialized tools for analyzing Salesforce/nCino configurations, with a focus on the Loan object. The analyzer can detect naming convention violations, security bypass patterns, and provide comprehensive reports and recommendations.

## Features

- **Claude Desktop Integration**: Seamlessly connect to Claude Desktop using the included configuration file
- **MCP Integration**: Connect to Claude and other LLMs using the Model Context Protocol
- **Metadata Analysis**: Analyze field naming conventions, validation rules, and Apex triggers
- **Security Assessment**: Detect bypass patterns and security vulnerabilities
- **Comprehensive Reporting**: Generate detailed reports with actionable recommendations
- **Salesforce Integration**: Extract metadata directly from Salesforce orgs

## Quick Start with Claude Desktop

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Claude Desktop**:
   - Edit the `claude_desktop_config.json` file with your desired settings
   - Add it to your Claude Desktop configuration directory, or
   - Add the `salesforce-analyzer` section to your existing configuration

   ```json
   {
       "mcpServers": {
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

3. **Start Claude Desktop**:
   - Launch the Claude Desktop application
   - It will automatically start the Salesforce Analyzer MCP server when needed

4. **Start analyzing**:
   - Upload your Salesforce metadata files to Claude
   - Ask Claude to analyze your configuration
   - Review the results and recommendations

For detailed instructions, see the [Claude Desktop Integration Guide](./docs/claude_desktop.md).

## Architecture

This project follows the Model Context Protocol specification, providing:

1. **Resources**: Salesforce metadata objects (fields, validation rules, triggers)
2. **Tools**: Specialized analysis functions for naming conventions and security patterns
3. **Prompts**: Pre-defined templates for common analysis scenarios

## Installation

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

## Usage

### Starting the MCP Server Manually

If you want to start the server manually instead of through Claude Desktop:

```bash
# Set environment variables (optional)
export MCP_API_KEY=your_api_key
export PORT=3000

# Start the server
python mcp_server.py
```

### Using the Client Example

```bash
# Run the client example
python mcp_client.py
```

## Documentation

See the [docs](./docs) directory for detailed documentation on:
- [Claude Desktop Integration](./docs/claude_desktop.md)
- [MCP Integration](./docs/mcp_integration.md)
- [Analysis Features](./docs/analysis_features.md)
- [Tool Reference](./docs/tool_reference.md)
- [Salesforce Integration](./docs/salesforce_integration.md)

## License

MIT

## Acknowledgements

This project is based on the concepts and patterns described in the [Model Context Protocol](https://modelcontextprotocol.io/) specification.
