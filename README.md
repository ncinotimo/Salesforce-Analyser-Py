# Salesforce-Analyser-Py

A Python-based Salesforce/nCino analyzer using Model Context Protocol (MCP) for integration with Claude and other LLMs.

## Overview

This project implements an MCP server that provides specialized tools for analyzing Salesforce/nCino configurations, with a focus on the Loan object. The analyzer can detect naming convention violations, security bypass patterns, and provide comprehensive reports and recommendations.

## Features

- **MCP Integration**: Seamlessly connect to Claude and other LLMs using the Model Context Protocol
- **Metadata Analysis**: Analyze field naming conventions, validation rules, and Apex triggers
- **Security Assessment**: Detect bypass patterns and security vulnerabilities
- **Comprehensive Reporting**: Generate detailed reports with actionable recommendations
- **Salesforce Integration**: Extract metadata directly from Salesforce orgs

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

### Connecting to Claude

1. Start the MCP server
2. Connect to Claude through the MCP Inspector or directly through Claude's MCP integration
3. Use the provided tools and resources to analyze Salesforce/nCino configurations

## Documentation

See the [docs](./docs) directory for detailed documentation on:
- [MCP Integration](./docs/mcp_integration.md)
- [Analysis Features](./docs/analysis_features.md)
- [Tool Reference](./docs/tool_reference.md)
- [Salesforce Integration](./docs/salesforce_integration.md)

## License

MIT

## Acknowledgements

This project is based on the concepts and patterns described in the [Model Context Protocol](https://modelcontextprotocol.io/) specification.
