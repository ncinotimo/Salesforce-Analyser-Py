"""
MCP Client Example

This module demonstrates how to use the MCP server with Claude from Python.
"""

import os
import asyncio
import json
import logging
from typing import Dict, List, Any

from mcp import MCPClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
MCP_API_KEY = os.getenv("MCP_API_KEY", "default_key")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:3000")
MODEL = os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229")

async def main():
    """
    Main function to demonstrate MCP client usage.
    """
    try:
        # Initialize MCP client
        client = MCPClient(
            api_key=MCP_API_KEY,
            model=MODEL,
            server_url=SERVER_URL,
            claude_api_key=CLAUDE_API_KEY
        )
        
        logger.info("Connecting to MCP server...")
        await client.connect()
        
        logger.info("Connected to MCP server successfully!")
        
        # Get available resources and tools
        resources = await client.list_resources()
        tools = await client.list_tools()
        prompts = await client.list_prompt_templates()
        
        logger.info(f"Available resources: {', '.join(r['id'] for r in resources)}")
        logger.info(f"Available tools: {', '.join(t['id'] for t in tools)}")
        logger.info(f"Available prompts: {', '.join(p['id'] for p in prompts)}")
        
        # Example: Load sample data
        sample_data = load_sample_data()
        
        # Example: Analyze naming conventions
        logger.info("--- Analyzing naming conventions ---")
        naming_results = await client.call_tool("salesforce.analyzeNamingConventions", {
            "fields": sample_data["fields"]
        })
        
        logger.info(f"Analysis complete. Compliance: {naming_results['results']['compliance_percentage']}%")
        logger.info(f"Found {len(naming_results['results']['violations'])} naming convention violations")
        
        # Example: Analyze validation rules
        logger.info("--- Analyzing validation rules ---")
        validation_results = await client.call_tool("salesforce.analyzeValidationRules", {
            "validation_rules": sample_data["validation_rules"]
        })
        
        logger.info(f"Analysis complete. Security score: {validation_results['results']['security_score']}/100")
        logger.info(f"Found {len(validation_results['results']['bypass_patterns'])} validation rules with bypass patterns")
        
        # Example: Generate comprehensive report
        logger.info("--- Generating comprehensive report ---")
        report_results = await client.call_tool("salesforce.generateReport", {
            "naming_results": naming_results,
            "validation_results": validation_results
        })
        
        logger.info("Report generated successfully!")
        logger.info(f"Overall score: {report_results['report']['overall_score']['score']}/100 ({report_results['report']['overall_score']['rating']})")
        
        # Example: Use a prompt template
        logger.info("--- Using prompt template ---")
        prompt_params = {
            "resource_ids": [
                "salesforce.fields",
                "salesforce.validationRules"
            ],
            "focus": "Naming convention compliance and security bypass patterns"
        }
        
        filled_prompt = await client.fill_prompt_template("salesforce.basicAnalysis", prompt_params)
        
        logger.info("Prompt template filled successfully!")
        logger.info("System prompt:", filled_prompt["system_prompt"][:100] + "...")
        logger.info("User prompt:", filled_prompt["user_prompt"][:100] + "...")
        
        # Example: Generate a response from Claude using the MCP server
        logger.info("--- Generating Claude response ---")
        
        # Create a chat completion
        completion = await client.create_chat_completion({
            "messages": [
                {
                    "role": "system",
                    "content": filled_prompt["system_prompt"]
                },
                {
                    "role": "user",
                    "content": filled_prompt["user_prompt"]
                }
            ]
        })
        
        logger.info("Claude response:", completion["choices"][0]["message"]["content"][:500] + "...")
        
        logger.info("MCP client example completed successfully!")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        # Disconnect from the MCP server
        await client.disconnect()
        logger.info("Disconnected from MCP server")

def load_sample_data() -> Dict[str, List[Dict[str, Any]]]:
    """
    Load sample data for demonstration.
    
    Returns:
        Dictionary containing sample Salesforce metadata
    """
    return {
        "fields": [
            {
                "apiName": "LLC_BI__Amount__c",
                "label": "Loan Amount",
                "type": "Currency",
                "description": "The total amount of the loan."
            },
            {
                "apiName": "LLC_BI__Status__c",
                "label": "Status",
                "type": "Picklist",
                "description": "The current status of the loan."
            },
            {
                "apiName": "nc_Loan_Score__c",
                "label": "Loan Score",
                "type": "Number",
                "description": "Custom scoring field for loan risk assessment."
            },
            {
                "apiName": "customField__c",
                "label": "Custom Field",
                "type": "Text",
                "description": "A custom field with non-compliant naming."
            }
        ],
        "validation_rules": [
            {
                "apiName": "LLC_BI__Loan_Amount_Validation",
                "active": True,
                "description": "Ensures loan amount is positive",
                "errorConditionFormula": "LLC_BI__Amount__c <= 0",
                "errorMessage": "Loan amount must be greater than zero.",
                "errorDisplayField": "LLC_BI__Amount__c"
            },
            {
                "apiName": "LLC_BI__Status_Complete_Check",
                "active": True,
                "description": "Validates required fields when status is Complete",
                "errorConditionFormula": "AND(ISPICKVAL(LLC_BI__Status__c, 'Complete'), ISBLANK(LLC_BI__CloseDate__c))",
                "errorMessage": "Close Date is required when Status is Complete.",
                "errorDisplayField": "LLC_BI__CloseDate__c"
            },
            {
                "apiName": "nc_Loan_Admin_Bypass",
                "active": True,
                "description": "Validation rule with admin bypass",
                "errorConditionFormula": "AND(ISPICKVAL(LLC_BI__Status__c, 'Pending'), $Profile.Name != 'System Administrator')",
                "errorMessage": "Only administrators can save loans in Pending status.",
                "errorDisplayField": "LLC_BI__Status__c"
            }
        ],
        "triggers": [
            {
                "name": "LLC_BI__LoanTrigger",
                "active": True,
                "content": """trigger LLC_BI__LoanTrigger on LLC_BI__Loan__c (before insert, before update) {
  // Skip processing if user has bypass permission
  if (FeatureManagement.checkPermission('Bypass_Loan_Trigger')) {
    return;
  }
  
  // Main trigger logic
  if (Trigger.isBefore && Trigger.isInsert) {
    LoanTriggerHandler.handleBeforeInsert(Trigger.new);
  } else if (Trigger.isBefore && Trigger.isUpdate) {
    LoanTriggerHandler.handleBeforeUpdate(Trigger.new, Trigger.oldMap);
  }
}"""
            }
        ]
    }

if __name__ == "__main__":
    asyncio.run(main())
