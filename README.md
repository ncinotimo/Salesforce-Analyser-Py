# Salesforce-Analyser-Py

A Python-based Salesforce/nCino analyzer using Model Context Protocol (MCP) for integration with Claude Desktop and other LLMs.

## Overview

This project implements an MCP server that provides specialized tools for analyzing Salesforce/nCino configurations, with a focus on the Loan object. The analyzer can detect naming convention violations, security bypass patterns, and provide comprehensive reports and recommendations.

## Features

- **Claude Desktop Integration**: Seamlessly connect to Claude Desktop using the included configuration
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

2. **Start the MCP server**:
   ```bash
   python mcp_server.py
   ```

3. **Connect to Claude Desktop**:
   - Open Claude Desktop
   - Go to Settings > Integrations > Add Integration
   - Select "From Configuration File"
   - Browse to and select `claude_desktop_config.json` from this repository
   - Follow the setup instructions in the UI

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

### Starting the MCP Server

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
