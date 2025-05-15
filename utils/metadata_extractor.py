"""
Metadata Extractor

This module provides functionality for extracting metadata from Salesforce orgs
and converting between different formats.
"""

import os
import json
import csv
import xml.etree.ElementTree as ET
import tempfile
import subprocess
import logging
from typing import Dict, List, Any, Optional, Union

import aiofiles
import aiohttp
import xmltodict
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MetadataExtractor:
    """
    Class for extracting metadata from Salesforce orgs and converting formats.
    """
    
    def __init__(self, temp_dir: str = None):
        """
        Initialize the extractor.
        
        Args:
            temp_dir: Directory for temporary files (default: system temp dir)
        """
        self.temp_dir = temp_dir or tempfile.gettempdir()
        
        # Create temp directory if it doesn't exist
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir, exist_ok=True)

    async def extract_metadata(self, credentials: Dict[str, str], object_name: str = "LLC_BI__Loan__c") -> Dict[str, Any]:
        """
        Extract metadata from a Salesforce org.
        
        Args:
            credentials: Dictionary with instance_url and access_token
            object_name: Name of the Salesforce object to extract
            
        Returns:
            Dictionary containing extracted metadata
        """
        instance_url = credentials.get("instance_url")
        access_token = credentials.get("access_token")
        
        if not instance_url or not access_token:
            raise ValueError("Both instance_url and access_token are required")
        
        # Set up a unique extraction directory
        extraction_id = f"extraction_{object_name}_{id(self)}"
        extraction_dir = os.path.join(self.temp_dir, extraction_id)
        os.makedirs(extraction_dir, exist_ok=True)
        
        try:
            # Authenticate with Salesforce
            await self._authenticate_with_salesforce(credentials, extraction_dir)
            
            # Extract the metadata
            await self._extract_object_metadata(extraction_dir, object_name)
            
            # Process the extracted metadata
            metadata = await self._process_extracted_metadata(extraction_dir, object_name)
            
            return metadata
        except Exception as e:
            logger.error(f"Error extracting metadata: {str(e)}")
            raise
        finally:
            # Clean up temporary files
            self._cleanup_temp_files(extraction_dir)

    async def _authenticate_with_salesforce(self, credentials: Dict[str, str], working_dir: str) -> None:
        """
        Authenticate with Salesforce using provided credentials.
        
        Args:
            credentials: Dictionary with Salesforce credentials
            working_dir: Working directory for the operation
        """
        instance_url = credentials.get("instance_url")
        access_token = credentials.get("access_token")
        
        # Create a session file
        session_file = os.path.join(working_dir, "sfdx_session.json")
        session_data = {
            "accessToken": access_token,
            "instanceUrl": instance_url,
            "refreshToken": None,
            "clientId": "MCP-Salesforce-Analyzer",
            "clientSecret": None,
            "refreshTokenExpiry": None
        }
        
        async with aiofiles.open(session_file, 'w') as f:
            await f.write(json.dumps(session_data))
        
        # Authenticate using SFDX or directly via API
        # For simplicity, we'll use the REST API directly
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Test the connection
        async with aiohttp.ClientSession() as session:
            url = f"{instance_url}/services/data/v56.0/sobjects"
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise ValueError(f"Salesforce authentication failed: {error_text}")
                
                logger.info("Salesforce authentication successful")

    async def _extract_object_metadata(self, working_dir: str, object_name: str) -> None:
        """
        Extract Salesforce object metadata.
        
        Args:
            working_dir: Working directory for the operation
            object_name: Name of the Salesforce object to extract
        """
        # Create a package.xml file for extraction
        package_dir = os.path.join(working_dir, "package")
        os.makedirs(package_dir, exist_ok=True)
        
        package_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>{object_name}</members>
        <n>CustomObject</n>
    </types>
    <types>
        <members>{object_name}.*</members>
        <n>CustomField</n>
    </types>
    <types>
        <members>{object_name}.*</members>
        <n>ValidationRule</n>
    </types>
    <version>56.0</version>
</Package>"""
        
        package_path = os.path.join(package_dir, "package.xml")
        async with aiofiles.open(package_path, 'w') as f:
            await f.write(package_xml)
        
        # In a real implementation, we would use SFDX or the Metadata API
        # For this example, we'll generate sample metadata for demonstration
        await self._generate_sample_metadata(working_dir, object_name)

    async def _generate_sample_metadata(self, working_dir: str, object_name: str) -> None:
        """
        Generate sample metadata for demonstration purposes.
        
        Args:
            working_dir: Working directory for the operation
            object_name: Name of the Salesforce object
        """
        # Create directories for the metadata
        object_dir = os.path.join(working_dir, "objects", object_name)
        fields_dir = os.path.join(object_dir, "fields")
        validation_dir = os.path.join(object_dir, "validationRules")
        triggers_dir = os.path.join(working_dir, "triggers")
        
        os.makedirs(fields_dir, exist_ok=True)
        os.makedirs(validation_dir, exist_ok=True)
        os.makedirs(triggers_dir, exist_ok=True)
        
        # Generate sample fields
        sample_fields = [
            {"apiName": "LLC_BI__Amount__c", "label": "Loan Amount", "type": "Currency"},
            {"apiName": "LLC_BI__Status__c", "label": "Status", "type": "Picklist"},
            {"apiName": "nc_Loan_Score__c", "label": "Loan Score", "type": "Number"},
            {"apiName": "customField__c", "label": "Custom Field", "type": "Text"},
        ]
        
        for field in sample_fields:
            field_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>{field["apiName"]}</fullName>
    <label>{field["label"]}</label>
    <type>{field["type"]}</type>
</CustomField>"""
            
            field_path = os.path.join(fields_dir, f"{field['apiName']}.field-meta.xml")
            async with aiofiles.open(field_path, 'w') as f:
                await f.write(field_xml)
        
        # Generate sample validation rules
        sample_rules = [
            {
                "apiName": "LLC_BI__Loan_Amount_Validation",
                "description": "Ensures loan amount is positive",
                "formula": "LLC_BI__Amount__c <= 0",
                "errorMessage": "Loan amount must be greater than zero."
            },
            {
                "apiName": "LLC_BI__Status_Complete_Check",
                "description": "Validates required fields when status is Complete",
                "formula": "AND(ISPICKVAL(LLC_BI__Status__c, 'Complete'), ISBLANK(LLC_BI__CloseDate__c))",
                "errorMessage": "Close Date is required when Status is Complete."
            },
            {
                "apiName": "nc_Loan_Admin_Bypass",
                "description": "Validation rule with admin bypass",
                "formula": "AND(ISPICKVAL(LLC_BI__Status__c, 'Pending'), $Profile.Name != 'System Administrator')",
                "errorMessage": "Only administrators can save loans in Pending status."
            }
        ]
        
        for rule in sample_rules:
            rule_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<ValidationRule xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>{rule["apiName"]}</fullName>
    <active>true</active>
    <description>{rule["description"]}</description>
    <errorConditionFormula>{rule["formula"]}</errorConditionFormula>
    <errorMessage>{rule["errorMessage"]}</errorMessage>
</ValidationRule>"""
            
            rule_path = os.path.join(validation_dir, f"{rule['apiName']}.validationRule-meta.xml")
            async with aiofiles.open(rule_path, 'w') as f:
                await f.write(rule_xml)
        
        # Generate sample trigger
        trigger_code = """trigger LLC_BI__LoanTrigger on LLC_BI__Loan__c (before insert, before update) {
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
        
        trigger_path = os.path.join(triggers_dir, "LLC_BI__LoanTrigger.trigger")
        async with aiofiles.open(trigger_path, 'w') as f:
            await f.write(trigger_code)
        
        trigger_meta = """<?xml version="1.0" encoding="UTF-8"?>
<ApexTrigger xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>56.0</apiVersion>
    <status>Active</status>
</ApexTrigger>"""
        
        trigger_meta_path = os.path.join(triggers_dir, "LLC_BI__LoanTrigger.trigger-meta.xml")
        async with aiofiles.open(trigger_meta_path, 'w') as f:
            await f.write(trigger_meta)

    async def _process_extracted_metadata(self, working_dir: str, object_name: str) -> Dict[str, Any]:
        """
        Process the extracted metadata files.
        
        Args:
            working_dir: Working directory with extracted metadata
            object_name: Name of the Salesforce object
            
        Returns:
            Dictionary containing processed metadata
        """
        metadata = {
            "fields": [],
            "validation_rules": [],
            "triggers": []
        }
        
        # Process fields
        fields_dir = os.path.join(working_dir, "objects", object_name, "fields")
        if os.path.exists(fields_dir):
            field_files = [f for f in os.listdir(fields_dir) if f.endswith(".field-meta.xml")]
            
            for field_file in field_files:
                field_path = os.path.join(fields_dir, field_file)
                async with aiofiles.open(field_path, 'r') as f:
                    field_xml = await f.read()
                    
                field_dict = xmltodict.parse(field_xml)
                
                if field_dict and "CustomField" in field_dict:
                    custom_field = field_dict["CustomField"]
                    metadata["fields"].append({
                        "apiName": field_file.replace(".field-meta.xml", ""),
                        "label": custom_field.get("label", ""),
                        "type": custom_field.get("type", ""),
                        "description": custom_field.get("description", ""),
                        "required": custom_field.get("required") == "true",
                        "formula": custom_field.get("formula", ""),
                        "referenceTo": custom_field.get("referenceTo", ""),
                        "length": custom_field.get("length", ""),
                        "unique": custom_field.get("unique") == "true"
                    })
        
        # Process validation rules
        validation_dir = os.path.join(working_dir, "objects", object_name, "validationRules")
        if os.path.exists(validation_dir):
            validation_files = [f for f in os.listdir(validation_dir) if f.endswith(".validationRule-meta.xml")]
            
            for validation_file in validation_files:
                validation_path = os.path.join(validation_dir, validation_file)
                async with aiofiles.open(validation_path, 'r') as f:
                    validation_xml = await f.read()
                    
                validation_dict = xmltodict.parse(validation_xml)
                
                if validation_dict and "ValidationRule" in validation_dict:
                    validation_rule = validation_dict["ValidationRule"]
                    metadata["validation_rules"].append({
                        "apiName": validation_file.replace(".validationRule-meta.xml", ""),
                        "active": validation_rule.get("active") == "true",
                        "description": validation_rule.get("description", ""),
                        "errorConditionFormula": validation_rule.get("errorConditionFormula", ""),
                        "errorMessage": validation_rule.get("errorMessage", ""),
                        "errorDisplayField": validation_rule.get("errorDisplayField", "")
                    })
        
        # Process triggers
        triggers_dir = os.path.join(working_dir, "triggers")
        if os.path.exists(triggers_dir):
            trigger_files = [f for f in os.listdir(triggers_dir) if f.endswith(".trigger")]
            
            for trigger_file in trigger_files:
                trigger_path = os.path.join(triggers_dir, trigger_file)
                async with aiofiles.open(trigger_path, 'r') as f:
                    trigger_content = await f.read()
                
                meta_file = f"{trigger_file}-meta.xml"
                meta_path = os.path.join(triggers_dir, meta_file)
                is_active = True
                
                if os.path.exists(meta_path):
                    async with aiofiles.open(meta_path, 'r') as f:
                        meta_xml = await f.read()
                        meta_dict = xmltodict.parse(meta_xml)
                        
                        if meta_dict and "ApexTrigger" in meta_dict:
                            is_active = meta_dict["ApexTrigger"].get("status") != "Inactive"
                
                metadata["triggers"].append({
                    "name": trigger_file.replace(".trigger", ""),
                    "content": trigger_content,
                    "active": is_active
                })
        
        return metadata

    def _cleanup_temp_files(self, extraction_dir: str) -> None:
        """
        Clean up temporary files.
        
        Args:
            extraction_dir: Directory to clean up
        """
        try:
            # In a production environment, you might want to remove the directory
            # But for debugging, we'll keep it
            logger.info(f"Temporary files available at: {extraction_dir}")
        except Exception as e:
            logger.warning(f"Error cleaning up temporary files: {str(e)}")

    async def convert_xml_to_json(self, xml_content: str) -> Dict[str, Any]:
        """
        Convert XML content to JSON.
        
        Args:
            xml_content: XML content to convert
            
        Returns:
            JSON representation of the XML
        """
        if os.path.exists(xml_content):
            async with aiofiles.open(xml_content, 'r') as f:
                xml_str = await f.read()
        else:
            xml_str = xml_content
            
        return xmltodict.parse(xml_str)

    async def parse_csv_file(self, csv_file: str) -> List[Dict[str, Any]]:
        """
        Parse a CSV file into a list of dictionaries.
        
        Args:
            csv_file: Path to the CSV file
            
        Returns:
            List of dictionaries representing CSV rows
        """
        if not os.path.exists(csv_file):
            raise ValueError(f"CSV file not found: {csv_file}")
            
        # Use pandas for easy CSV parsing
        df = pd.read_csv(csv_file)
        return df.to_dict('records')
