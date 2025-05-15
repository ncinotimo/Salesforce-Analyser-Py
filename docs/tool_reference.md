# Tool Reference

This reference guide provides detailed information on each tool available in the Salesforce/nCino Analyzer MCP server.

## Table of Contents

1. [Extract Metadata](#extract-metadata)
2. [Analyze Naming Conventions](#analyze-naming-conventions)
3. [Analyze Validation Rules](#analyze-validation-rules)
4. [Analyze Apex Triggers](#analyze-apex-triggers)
5. [Generate Report](#generate-report)

## Extract Metadata

Extracts metadata from a Salesforce org.

### Tool ID
`salesforce.extractMetadata`

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| instance_url | string | Salesforce instance URL (e.g., https://mycompany.my.salesforce.com) | Yes |
| access_token | string | Salesforce access token | Yes |
| object_name | string | Object name to extract (default: LLC_BI__Loan__c) | No |

### Returns

```json
{
  "success": true,
  "data": {
    "fields": [
      {
        "apiName": "LLC_BI__Amount__c",
        "label": "Loan Amount",
        "type": "Currency",
        "description": "The total amount of the loan."
      },
      ...
    ],
    "validation_rules": [
      {
        "apiName": "LLC_BI__Loan_Amount_Validation",
        "active": true,
        "description": "Ensures loan amount is positive",
        "errorConditionFormula": "LLC_BI__Amount__c <= 0",
        "errorMessage": "Loan amount must be greater than zero."
      },
      ...
    ],
    "triggers": [
      {
        "name": "LLC_BI__LoanTrigger",
        "content": "...",
        "active": true
      },
      ...
    ]
  },
  "message": "Successfully extracted metadata for LLC_BI__Loan__c"
}
```

### Example Usage

```python
# Extract metadata from Salesforce
result = await client.call_tool("salesforce.extractMetadata", {
    "instance_url": "https://mycompany.my.salesforce.com",
    "access_token": "00D...",
    "object_name": "LLC_BI__Loan__c"
})
```

## Analyze Naming Conventions

Analyzes field naming conventions against nCino standards.

### Tool ID
`salesforce.analyzeNamingConventions`

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| fields | array | Array of field metadata objects | Yes* |
| resource_id | string | Optional resource ID to analyze instead of providing fields directly | Yes* |

\* Either `fields` or `resource_id` must be provided.

### Returns

```json
{
  "success": true,
  "results": {
    "violations": [
      {
        "apiName": "customField__c",
        "label": "Custom Field",
        "type": "Text",
        "violations": [
          {
            "rule": "Custom project-specific fields",
            "pattern": "^nc_",
            "expected": true
          }
        ],
        "recommended_fix": "Add 'nc_' prefix: 'nc_customField__c'"
      },
      ...
    ],
    "compliant_field_count": 3,
    "total_field_count": 4,
    "compliance_percentage": 75,
    "by_severity": {
      "critical": [...],
      "medium": [...],
      "low": [...]
    }
  },
  "summary": {
    "total_fields": 4,
    "compliant_fields": 3,
    "compliance_percentage": 75,
    "violation_count": 1,
    "critical_violations": 0,
    "medium_violations": 1,
    "low_violations": 0,
    "top_issues": [...],
    "recommendations": [...]
  },
  "message": "Analyzed 4 fields. Compliance: 75%"
}
```

### Example Usage

```python
# Analyze field naming conventions
result = await client.call_tool("salesforce.analyzeNamingConventions", {
    "fields": fields_data
})

# Or using a resource
result = await client.call_tool("salesforce.analyzeNamingConventions", {
    "resource_id": "salesforce.fields"
})
```

## Analyze Validation Rules

Detects bypass patterns in validation rules.

### Tool ID
`salesforce.analyzeValidationRules`

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| validation_rules | array | Array of validation rule metadata objects | Yes* |
| resource_id | string | Optional resource ID to analyze instead of providing validation rules directly | Yes* |

\* Either `validation_rules` or `resource_id` must be provided.

### Returns

```json
{
  "success": true,
  "results": {
    "bypass_patterns": [
      {
        "apiName": "nc_Loan_Admin_Bypass",
        "active": true,
        "description": "Validation rule with admin bypass",
        "patterns": [
          {
            "name": "Profile-based bypass",
            "severity": "Medium",
            "description": "Using Profile.Name to bypass validation rules creates maintenance challenges when profiles change.",
            "recommended_approach": "Use custom permissions instead, which are more maintainable and explicit."
          }
        ],
        "highest_severity": "Medium"
      },
      ...
    ],
    "rules_by_pattern": {
      "Profile-based bypass": ["nc_Loan_Admin_Bypass"],
      "Custom permission bypass": [],
      "User ID bypass": [],
      "Record Type bypass": [],
      "Owner ID bypass": []
    },
    "rules_by_severity": {
      "High": [],
      "Medium": ["nc_Loan_Admin_Bypass"],
      "Low": []
    },
    "total_rules": 3,
    "rules_with_bypass": 1,
    "bypass_percentage": 33,
    "security_score": 90
  },
  "refactoring_priorities": [...],
  "recommendations": [...],
  "message": "Analyzed 3 validation rules. Security score: 90/100"
}
```

### Example Usage

```python
# Analyze validation rules
result = await client.call_tool("salesforce.analyzeValidationRules", {
    "validation_rules": validation_rules_data
})

# Or using a resource
result = await client.call_tool("salesforce.analyzeValidationRules", {
    "resource_id": "salesforce.validationRules"
})
```

## Analyze Apex Triggers

Detects bypass patterns in Apex triggers.

### Tool ID
`salesforce.analyzeApexTriggers`

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| triggers | array | Array of trigger metadata objects | Yes* |
| resource_id | string | Optional resource ID to analyze instead of providing triggers directly | Yes* |

\* Either `triggers` or `resource_id` must be provided.

### Returns

```json
{
  "success": true,
  "results": {
    "bypass_patterns": [
      {
        "name": "LLC_BI__LoanTrigger",
        "active": true,
        "patterns": [
          {
            "name": "Feature management permission check",
            "severity": "Low",
            "description": "Using FeatureManagement to check permissions is recommended, but should be implemented consistently.",
            "recommended_approach": "Use a consistent pattern like return !FeatureManagement.checkPermission('Bypass_Trigger');"
          }
        ],
        "highest_severity": "Low"
      },
      ...
    ],
    "triggers_by_pattern": {
      "Feature management permission check": ["LLC_BI__LoanTrigger"],
      "Custom setting bypass": [],
      "Hardcoded User ID check": [],
      "Profile name check": []
    },
    "triggers_by_severity": {
      "High": [],
      "Medium": [],
      "Low": ["LLC_BI__LoanTrigger"]
    },
    "total_triggers": 1,
    "triggers_with_bypass": 1,
    "bypass_percentage": 100,
    "security_score": 95
  },
  "refactoring_priorities": [...],
  "recommendations": [...],
  "message": "Analyzed 1 triggers. Security score: 95/100"
}
```

### Example Usage

```python
# Analyze Apex triggers
result = await client.call_tool("salesforce.analyzeApexTriggers", {
    "triggers": triggers_data
})

# Or using a resource
result = await client.call_tool("salesforce.analyzeApexTriggers", {
    "resource_id": "salesforce.triggers"
})
```

## Generate Report

Generates a comprehensive report combining all analyses.

### Tool ID
`salesforce.generateReport`

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| naming_results | object | Results from naming convention analysis | No |
| validation_results | object | Results from validation rule analysis | No |
| trigger_results | object | Results from trigger analysis | No |

### Returns

```json
{
  "success": true,
  "report": {
    "executive_summary": {
      "overall_assessment": "Low risk identified. The configuration is generally sound with minor improvements recommended.",
      "key_findings": [
        "75% of fields comply with naming conventions.",
        "33% of validation rules contain bypass patterns.",
        "100% of Apex triggers contain bypass patterns."
      ],
      "risks_identified": {
        "critical": 0,
        "medium": 1,
        "low": 1
      }
    },
    "detailed_findings": {
      "naming_conventions": {...},
      "validation_rules": {...},
      "triggers": {...}
    },
    "recommendations": [...],
    "overall_score": {
      "score": 85,
      "rating": "Good",
      "component_scores": {
        "naming_conventions": 75,
        "validation_rules": 90,
        "triggers": 95
      }
    }
  },
  "message": "Successfully generated comprehensive report"
}
```

### Example Usage

```python
# Generate comprehensive report
result = await client.call_tool("salesforce.generateReport", {
    "naming_results": naming_results,
    "validation_results": validation_results,
    "trigger_results": trigger_results
})
```

## Using Resources with Tools

Many tools accept a `resource_id` parameter instead of direct data input. This allows for easy chaining of tool calls:

```python
# Get resource content
fields_resource = await client.get_resource("salesforce.fields")

# Analyze the resource
naming_results = await client.call_tool("salesforce.analyzeNamingConventions", {
    "resource_id": "salesforce.fields"
})

# Generate a report using the results
report = await client.call_tool("salesforce.generateReport", {
    "naming_results": naming_results
})
```

## Error Handling

All tools return a `success` flag and, in case of errors, an `error` field with the error message:

```json
{
  "success": false,
  "error": "No valid fields provided for analysis",
  "message": "Failed to analyze naming conventions: No valid fields provided for analysis"
}
```

## Best Practices

1. **Resource Reuse**: Use resources when analyzing the same data multiple times
2. **Error Handling**: Always check the `success` flag before processing results
3. **Result Caching**: Cache analysis results when generating multiple reports
4. **Tool Chaining**: Use the output of one tool as input for another
5. **Parameter Validation**: Validate parameters before calling tools to avoid errors