"""
MCP Server for Salesforce/nCino Analysis

This module implements a Model Context Protocol (MCP) server that provides
specialized tools for analyzing Salesforce/nCino configurations.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional

from mcp import MCPServer, Resource, Tool, PromptTemplate

from models.naming_convention_analyzer import NamingConventionAnalyzer
from models.bypass_pattern_analyzer import BypassPatternAnalyzer
from utils.metadata_extractor import MetadataExtractor
from utils.report_generator import generate_comprehensive_report

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get environment variables
MCP_API_KEY = os.getenv("MCP_API_KEY", "default_key")
PORT = int(os.getenv("PORT", "3000"))

# Initialize the MCP server
server = MCPServer(
    api_key=MCP_API_KEY,
    name="Salesforce/nCino Analyzer",
    description="Specialized analyzer for Salesforce/nCino configurations",
    version="1.0.0",
    vendor="nCino",
    contact_info="https://github.com/ncinotimo/Salesforce-Analyser-Py"
)

# Initialize analyzers and utilities
naming_analyzer = NamingConventionAnalyzer()
bypass_analyzer = BypassPatternAnalyzer()
metadata_extractor = MetadataExtractor()

# ====================================================================
# RESOURCES
# ====================================================================

@server.resource(
    id="salesforce.fields",
    name="Salesforce Field Definitions",
    description="Field definitions from Salesforce/nCino objects",
    content_type="application/json"
)
async def get_fields(source: str = None, object_name: str = "LLC_BI__Loan__c") -> Dict[str, Any]:
    """
    Retrieve field definitions from Salesforce/nCino objects
    
    Args:
        source: Source of the field definitions (file path or JSON)
        object_name: Name of the Salesforce object
        
    Returns:
        Dictionary containing field definitions and metadata
    """
    try:
        field_data = await load_resource_data(source)
        return {
            "content": field_data,
            "metadata": {
                "count": len(field_data),
                "objectName": object_name
            }
        }
    except Exception as e:
        logger.error(f"Error retrieving field definitions: {str(e)}")
        raise ValueError(f"Failed to load field definitions: {str(e)}")

@server.resource(
    id="salesforce.validationRules",
    name="Salesforce Validation Rules",
    description="Validation rule definitions from Salesforce/nCino objects",
    content_type="application/json"
)
async def get_validation_rules(source: str = None, object_name: str = "LLC_BI__Loan__c") -> Dict[str, Any]:
    """
    Retrieve validation rule definitions from Salesforce/nCino objects
    
    Args:
        source: Source of the validation rule definitions (file path or JSON)
        object_name: Name of the Salesforce object
        
    Returns:
        Dictionary containing validation rule definitions and metadata
    """
    try:
        rule_data = await load_resource_data(source)
        return {
            "content": rule_data,
            "metadata": {
                "count": len(rule_data),
                "objectName": object_name
            }
        }
    except Exception as e:
        logger.error(f"Error retrieving validation rules: {str(e)}")
        raise ValueError(f"Failed to load validation rules: {str(e)}")

@server.resource(
    id="salesforce.triggers",
    name="Salesforce Apex Triggers",
    description="Apex trigger definitions from Salesforce/nCino objects",
    content_type="application/json"
)
async def get_triggers(source: str = None, object_name: str = "LLC_BI__Loan__c") -> Dict[str, Any]:
    """
    Retrieve Apex trigger definitions from Salesforce/nCino objects
    
    Args:
        source: Source of the trigger definitions (file path or JSON)
        object_name: Name of the Salesforce object
        
    Returns:
        Dictionary containing trigger definitions and metadata
    """
    try:
        trigger_data = await load_resource_data(source)
        return {
            "content": trigger_data,
            "metadata": {
                "count": len(trigger_data),
                "objectName": object_name
            }
        }
    except Exception as e:
        logger.error(f"Error retrieving triggers: {str(e)}")
        raise ValueError(f"Failed to load triggers: {str(e)}")

# ====================================================================
# TOOLS
# ====================================================================

@server.tool(
    id="salesforce.extractMetadata",
    name="Extract Salesforce Metadata",
    description="Extract metadata from a Salesforce org",
    parameters={
        "type": "object",
        "properties": {
            "instance_url": {
                "type": "string",
                "description": "Salesforce instance URL (e.g., https://mycompany.my.salesforce.com)"
            },
            "access_token": {
                "type": "string",
                "description": "Salesforce access token"
            },
            "object_name": {
                "type": "string",
                "description": "Object name to extract (default: LLC_BI__Loan__c)",
                "default": "LLC_BI__Loan__c"
            }
        },
        "required": ["instance_url", "access_token"]
    }
)
async def extract_metadata(instance_url: str, access_token: str, object_name: str = "LLC_BI__Loan__c") -> Dict[str, Any]:
    """
    Extract metadata from a Salesforce org
    
    Args:
        instance_url: Salesforce instance URL
        access_token: Salesforce access token
        object_name: Name of the Salesforce object to extract
        
    Returns:
        Dictionary containing extracted metadata
    """
    try:
        credentials = {
            "instance_url": instance_url,
            "access_token": access_token
        }
        
        metadata = await metadata_extractor.extract_metadata(credentials, object_name)
        
        return {
            "success": True,
            "data": {
                "fields": metadata.get("fields", []),
                "validation_rules": metadata.get("validation_rules", []),
                "triggers": metadata.get("triggers", [])
            },
            "message": f"Successfully extracted metadata for {object_name}"
        }
    except Exception as e:
        logger.error(f"Error extracting metadata: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to extract metadata: {str(e)}"
        }

@server.tool(
    id="salesforce.analyzeNamingConventions",
    name="Analyze Naming Conventions",
    description="Analyze field naming conventions against nCino standards",
    parameters={
        "type": "object",
        "properties": {
            "fields": {
                "type": "array",
                "description": "Array of field metadata objects",
                "items": {
                    "type": "object"
                }
            },
            "resource_id": {
                "type": "string",
                "description": "Optional resource ID to analyze instead of providing fields directly"
            }
        },
        "anyOf": [
            {"required": ["fields"]},
            {"required": ["resource_id"]}
        ]
    }
)
async def analyze_naming_conventions(fields: List[Dict[str, Any]] = None, resource_id: str = None) -> Dict[str, Any]:
    """
    Analyze field naming conventions against nCino standards
    
    Args:
        fields: List of field metadata objects
        resource_id: Optional resource ID to analyze instead of providing fields directly
        
    Returns:
        Dictionary containing analysis results
    """
    try:
        fields_to_analyze = fields
        
        # If resource_id is provided, get the fields from that resource
        if resource_id and not fields:
            resource = await server.get_resource(resource_id)
            fields_to_analyze = resource.get("content")
        
        if not fields_to_analyze or not isinstance(fields_to_analyze, list):
            raise ValueError("No valid fields provided for analysis")
        
        results = naming_analyzer.analyze_fields(fields_to_analyze)
        summary = naming_analyzer.generate_summary_report(results)
        
        return {
            "success": True,
            "results": results,
            "summary": summary,
            "message": f"Analyzed {len(fields_to_analyze)} fields. Compliance: {results['compliance_percentage']}%"
        }
    except Exception as e:
        logger.error(f"Error analyzing naming conventions: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to analyze naming conventions: {str(e)}"
        }

@server.tool(
    id="salesforce.analyzeValidationRules",
    name="Analyze Validation Rule Bypass Patterns",
    description="Detect bypass patterns in validation rules",
    parameters={
        "type": "object",
        "properties": {
            "validation_rules": {
                "type": "array",
                "description": "Array of validation rule metadata objects",
                "items": {
                    "type": "object"
                }
            },
            "resource_id": {
                "type": "string",
                "description": "Optional resource ID to analyze instead of providing validation rules directly"
            }
        },
        "anyOf": [
            {"required": ["validation_rules"]},
            {"required": ["resource_id"]}
        ]
    }
)
async def analyze_validation_rules(validation_rules: List[Dict[str, Any]] = None, resource_id: str = None) -> Dict[str, Any]:
    """
    Detect bypass patterns in validation rules
    
    Args:
        validation_rules: List of validation rule metadata objects
        resource_id: Optional resource ID to analyze instead of providing validation rules directly
        
    Returns:
        Dictionary containing analysis results
    """
    try:
        rules_to_analyze = validation_rules
        
        # If resource_id is provided, get the validation rules from that resource
        if resource_id and not validation_rules:
            resource = await server.get_resource(resource_id)
            rules_to_analyze = resource.get("content")
        
        if not rules_to_analyze or not isinstance(rules_to_analyze, list):
            raise ValueError("No valid validation rules provided for analysis")
        
        results = bypass_analyzer.analyze_validation_rules(rules_to_analyze)
        priorities = bypass_analyzer.generate_refactoring_priorities(results, 'validation')
        recommendations = bypass_analyzer.generate_general_recommendations(results, 'validation')
        
        return {
            "success": True,
            "results": results,
            "refactoring_priorities": priorities,
            "recommendations": recommendations,
            "message": f"Analyzed {len(rules_to_analyze)} validation rules. Security score: {results['security_score']}/100"
        }
    except Exception as e:
        logger.error(f"Error analyzing validation rules: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to analyze validation rules: {str(e)}"
        }

@server.tool(
    id="salesforce.analyzeApexTriggers",
    name="Analyze Apex Trigger Bypass Patterns",
    description="Detect bypass patterns in Apex triggers",
    parameters={
        "type": "object",
        "properties": {
            "triggers": {
                "type": "array",
                "description": "Array of trigger metadata objects",
                "items": {
                    "type": "object"
                }
            },
            "resource_id": {
                "type": "string",
                "description": "Optional resource ID to analyze instead of providing triggers directly"
            }
        },
        "anyOf": [
            {"required": ["triggers"]},
            {"required": ["resource_id"]}
        ]
    }
)
async def analyze_apex_triggers(triggers: List[Dict[str, Any]] = None, resource_id: str = None) -> Dict[str, Any]:
    """
    Detect bypass patterns in Apex triggers
    
    Args:
        triggers: List of trigger metadata objects
        resource_id: Optional resource ID to analyze instead of providing triggers directly
        
    Returns:
        Dictionary containing analysis results
    """
    try:
        triggers_to_analyze = triggers
        
        # If resource_id is provided, get the triggers from that resource
        if resource_id and not triggers:
            resource = await server.get_resource(resource_id)
            triggers_to_analyze = resource.get("content")
        
        if not triggers_to_analyze or not isinstance(triggers_to_analyze, list):
            raise ValueError("No valid triggers provided for analysis")
        
        results = bypass_analyzer.analyze_apex_triggers(triggers_to_analyze)
        priorities = bypass_analyzer.generate_refactoring_priorities(results, 'trigger')
        recommendations = bypass_analyzer.generate_general_recommendations(results, 'trigger')
        
        return {
            "success": True,
            "results": results,
            "refactoring_priorities": priorities,
            "recommendations": recommendations,
            "message": f"Analyzed {len(triggers_to_analyze)} triggers. Security score: {results['security_score']}/100"
        }
    except Exception as e:
        logger.error(f"Error analyzing triggers: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to analyze triggers: {str(e)}"
        }

@server.tool(
    id="salesforce.generateReport",
    name="Generate Comprehensive Report",
    description="Generate a comprehensive report combining all analyses",
    parameters={
        "type": "object",
        "properties": {
            "naming_results": {
                "type": "object",
                "description": "Results from naming convention analysis"
            },
            "validation_results": {
                "type": "object",
                "description": "Results from validation rule analysis"
            },
            "trigger_results": {
                "type": "object",
                "description": "Results from trigger analysis"
            }
        },
        "required": []
    }
)
async def generate_report(naming_results: Dict[str, Any] = None, validation_results: Dict[str, Any] = None, 
                         trigger_results: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generate a comprehensive report combining all analyses
    
    Args:
        naming_results: Results from naming convention analysis
        validation_results: Results from validation rule analysis
        trigger_results: Results from trigger analysis
        
    Returns:
        Dictionary containing the comprehensive report
    """
    try:
        # Build analyses object
        analyses = {}
        
        if naming_results:
            analyses["naming_conventions"] = naming_results.get("results")
            analyses["naming_conventions_summary"] = naming_results.get("summary")
        
        if validation_results:
            analyses["validation_rules"] = validation_results.get("results")
            analyses["validation_rules_refactoring_priorities"] = validation_results.get("refactoring_priorities")
            analyses["validation_rules_recommendations"] = validation_results.get("recommendations")
        
        if trigger_results:
            analyses["triggers"] = trigger_results.get("results")
            analyses["triggers_refactoring_priorities"] = trigger_results.get("refactoring_priorities")
            analyses["triggers_recommendations"] = trigger_results.get("recommendations")
        
        # Generate report structure
        report = generate_comprehensive_report(analyses)
        
        return {
            "success": True,
            "report": report,
            "message": "Successfully generated comprehensive report"
        }
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to generate report: {str(e)}"
        }

# ====================================================================
# PROMPT TEMPLATES
# ====================================================================

@server.prompt_template(
    id="salesforce.basicAnalysis",
    name="Basic Salesforce/nCino Analysis",
    description="Analyze Salesforce/nCino configuration for basic issues"
)
async def basic_analysis_template(resource_ids: List[str] = None, focus: str = None) -> Dict[str, str]:
    """
    Basic Salesforce/nCino analysis prompt template
    
    Args:
        resource_ids: List of resource IDs to analyze
        focus: Specific focus areas for the analysis
        
    Returns:
        Dictionary containing system and user prompts
    """
    system_prompt = """You are a Salesforce/nCino configuration expert who specializes in analyzing metadata for naming convention violations and security issues. 
  
You will be analyzing:
- Field naming conventions against nCino standards
- Validation rule bypass patterns
- Apex trigger security issues

Provide a clear, concise analysis with:
1. Executive summary with key findings
2. Detailed list of issues found, grouped by type
3. Prioritized recommendations for improvement
4. Overall configuration health score"""

    # Build the user prompt
    user_prompt = """Analyze the provided Salesforce/nCino configuration and identify any issues with naming conventions or security patterns. 

"""
    if resource_ids:
        user_prompt += "I've provided the following resources to analyze:\n"
        for resource_id in resource_ids:
            user_prompt += f"- {resource_id}\n"
        user_prompt += "\n"

    user_prompt += "Please focus on:\n"
    if focus:
        user_prompt += focus + "\n"
    else:
        user_prompt += """- Naming convention compliance
- Security bypass patterns
- Overall configuration health"""

    return {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt
    }

@server.prompt_template(
    id="salesforce.securityAnalysis",
    name="Salesforce/nCino Security Analysis",
    description="Analyze Salesforce/nCino configuration for security issues"
)
async def security_analysis_template(resource_ids: List[str] = None) -> Dict[str, str]:
    """
    Salesforce/nCino security analysis prompt template
    
    Args:
        resource_ids: List of resource IDs to analyze
        
    Returns:
        Dictionary containing system and user prompts
    """
    system_prompt = """You are a Salesforce/nCino security expert specializing in detecting bypass patterns and security vulnerabilities in configurations.

Focus primarily on:
- Validation rule bypass patterns (profile-based, user-based, etc.)
- Apex trigger security concerns
- Permission-based security issues
- Hardcoded IDs and other security risks

Provide a thorough security analysis with:
1. Executive summary with critical security findings
2. Detailed breakdown of all security vulnerabilities found
3. Security risk score for each component
4. Remediation plan with prioritized actions"""

    # Build the user prompt
    user_prompt = """Perform a comprehensive security analysis of the provided Salesforce/nCino configuration, focusing specifically on security bypass patterns and vulnerabilities.

"""
    if resource_ids:
        user_prompt += "I've provided the following resources to analyze:\n"
        for resource_id in resource_ids:
            user_prompt += f"- {resource_id}\n"
        user_prompt += "\n"

    user_prompt += """Please identify:
- All bypass patterns in validation rules and triggers
- Hardcoded IDs and credentials
- Profile-based or user-based security bypasses
- Other security vulnerabilities

For each issue, provide:
1. Severity level
2. Explanation of the security risk
3. Recommended fix"""

    return {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt
    }

# ====================================================================
# HELPER FUNCTIONS
# ====================================================================

async def load_resource_data(source):
    """
    Load resource data from various sources
    
    Args:
        source: Source of the data (file path, URL, or direct data)
        
    Returns:
        Loaded data
    """
    if not source:
        raise ValueError("No source provided for resource data")
    
    # If the source is a file path
    if isinstance(source, str) and (source.endswith('.json') or source.endswith('.xml') or source.endswith('.csv')):
        if not os.path.exists(source):
            raise ValueError(f"File not found: {source}")
        
        if source.endswith('.json'):
            with open(source, 'r') as file:
                return json.load(file)
        elif source.endswith('.xml'):
            return await metadata_extractor.convert_xml_to_json(source)
        elif source.endswith('.csv'):
            return await metadata_extractor.parse_csv_file(source)
    
    # If the source is already a data object
    if isinstance(source, (dict, list)):
        return source
    
    raise ValueError("Unsupported resource source format")

# ====================================================================
# MAIN
# ====================================================================

if __name__ == "__main__":
    logger.info(f"Starting MCP server on port {PORT}")
    server.start(port=PORT)
