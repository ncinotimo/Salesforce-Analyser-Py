"""
Naming Convention Analyzer

This module provides functionality for analyzing Salesforce/nCino field
naming conventions and detecting violations.
"""

import re
from typing import Dict, List, Any, Tuple, Set

class NamingConventionAnalyzer:
    """
    Class for analyzing Salesforce/nCino field naming conventions.
    """
    
    def __init__(self):
        """
        Initialize the analyzer with defined convention rules.
        """
        self.convention_rules = [
            {
                "pattern": re.compile(r"^LLC_BI__"),
                "description": "Managed package fields from nCino",
                "expected": True
            },
            {
                "pattern": re.compile(r"^nc_"),
                "description": "Custom project-specific fields",
                "expected": True
            },
            {
                "pattern": re.compile(r"^[a-z]"),
                "description": "Fields should not start with lowercase letters",
                "expected": False
            }
        ]

        self.loan_object_conventions = {
            "standard_patterns": [
                re.compile(r"^LLC_BI__Loan__c$"),
                re.compile(r"^LLC_BI__.*__c$")
            ],
            "custom_patterns": [
                re.compile(r"^nc_Loan_.*__c$"),
                re.compile(r"^nc_.*__c$")
            ],
            "invalid_patterns": [
                re.compile(r"^Loan_"),
                re.compile(r"^loan_"),
                re.compile(r"__X$")
            ]
        }

    def analyze_fields(self, fields: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze field metadata for naming convention compliance.
        
        Args:
            fields: List of field metadata objects
            
        Returns:
            Dictionary containing analysis results
        """
        if not fields or not isinstance(fields, list):
            raise ValueError("Field data must be provided as a list")

        results = {
            "violations": [],
            "compliant_field_count": 0,
            "total_field_count": len(fields),
            "by_severity": {
                "critical": [],
                "medium": [],
                "low": []
            }
        }

        # Analyze each field
        for field in fields:
            api_name = field.get("apiName") or field.get("fullName") or ""
            violations = []

            # Check against convention rules
            for rule in self.convention_rules:
                matches = rule["pattern"].search(api_name) is not None
                if (rule["expected"] and not matches) or (not rule["expected"] and matches):
                    violations.append({
                        "rule": rule["description"],
                        "pattern": rule["pattern"].pattern,
                        "expected": rule["expected"]
                    })

            # Check against Loan object specific patterns
            if "Loan" in api_name or "loan" in api_name:
                # Check if it's not following standard patterns
                is_standard = any(pattern.search(api_name) is not None for pattern in self.loan_object_conventions["standard_patterns"])
                is_custom = any(pattern.search(api_name) is not None for pattern in self.loan_object_conventions["custom_patterns"])
                has_invalid_pattern = any(pattern.search(api_name) is not None for pattern in self.loan_object_conventions["invalid_patterns"])

                if not is_standard and not is_custom and "Loan" in api_name:
                    violations.append({
                        "rule": "Loan-related fields must follow standard or custom patterns",
                        "severity": "critical"
                    })

                if has_invalid_pattern:
                    violations.append({
                        "rule": "Field uses an invalid naming pattern",
                        "severity": "critical"
                    })

            # If violations were found, add to results
            if violations:
                field_violation = {
                    "apiName": api_name,
                    "label": field.get("label", ""),
                    "type": field.get("type", ""),
                    "violations": violations,
                    "recommended_fix": self.generate_recommendation(api_name, violations)
                }

                # Assign severity
                severity = self.determine_severity(violations)
                results["by_severity"][severity].append(field_violation)
                results["violations"].append(field_violation)
            else:
                results["compliant_field_count"] += 1

        # Calculate compliance percentage
        results["compliance_percentage"] = round((results["compliant_field_count"] / results["total_field_count"]) * 100)

        return results

    def determine_severity(self, violations: List[Dict[str, Any]]) -> str:
        """
        Determine the overall severity of violations.
        
        Args:
            violations: List of violations found for a field
            
        Returns:
            Severity level: 'critical', 'medium', or 'low'
        """
        if any(v.get("severity") == "critical" for v in violations):
            return "critical"
        if any("Loan" in v.get("rule", "") or "standard patterns" in v.get("rule", "") for v in violations):
            return "critical"
        if any("custom project-specific" in v.get("rule", "") for v in violations):
            return "medium"
        return "low"

    def generate_recommendation(self, api_name: str, violations: List[Dict[str, Any]]) -> str:
        """
        Generate a recommended fix for naming convention violations.
        
        Args:
            api_name: Current API name
            violations: List of violations found
            
        Returns:
            Recommended fix as a string
        """
        recommendation = ""
        
        # Check for lowercase starting violations
        if any("lowercase" in v.get("rule", "") for v in violations):
            first_char = api_name[0]
            recommendation = f"Change first character '{first_char}' to uppercase: '{first_char.upper() + api_name[1:]}'"
        # Check for missing prefixes
        elif any("Managed package" in v.get("rule", "") or "Custom project-specific" in v.get("rule", "") for v in violations):
            if "Loan" in api_name and not api_name.startswith("LLC_BI__") and not api_name.startswith("nc_"):
                recommendation = f"Add 'nc_' prefix: 'nc_{api_name}'"
            else:
                recommendation = "Add appropriate prefix ('LLC_BI__' for managed package fields or 'nc_' for custom fields)"
        # Check for invalid patterns
        elif any("invalid" in v.get("rule", "") for v in violations):
            if api_name.endswith("__X"):
                recommendation = f"Remove '__X' suffix: '{api_name.replace('__X', '__c')}'"
            elif api_name.startswith("loan_"):
                recommendation = f"Change to 'nc_Loan_{api_name[5:]}'"
            else:
                recommendation = "Rename to follow standard pattern (LLC_BI__*__c) or custom pattern (nc_*__c)"
        
        return recommendation or "Review field naming and apply appropriate convention"

    def generate_summary_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a summary report of naming convention compliance.
        
        Args:
            results: Analysis results
            
        Returns:
            Summary report
        """
        return {
            "total_fields": results["total_field_count"],
            "compliant_fields": results["compliant_field_count"],
            "compliance_percentage": results["compliance_percentage"],
            "violation_count": len(results["violations"]),
            "critical_violations": len(results["by_severity"]["critical"]),
            "medium_violations": len(results["by_severity"]["medium"]),
            "low_violations": len(results["by_severity"]["low"]),
            "top_issues": self.identify_top_issues(results["violations"]),
            "recommendations": self.generate_general_recommendations(results)
        }

    def identify_top_issues(self, violations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Identify the most common violation types.
        
        Args:
            violations: All violations found
            
        Returns:
            List of top issues
        """
        issue_types = {}
        
        for v in violations:
            for issue in v["violations"]:
                rule_desc = issue.get("rule", "")
                if rule_desc not in issue_types:
                    issue_types[rule_desc] = 0
                issue_types[rule_desc] += 1
        
        return [
            {"rule": rule, "count": count}
            for rule, count in sorted(issue_types.items(), key=lambda x: x[1], reverse=True)[:5]
        ]

    def generate_general_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """
        Generate general recommendations based on analysis results.
        
        Args:
            results: Analysis results
            
        Returns:
            List of general recommendations
        """
        recommendations = []
        
        if len(results["by_severity"]["critical"]) > 0:
            recommendations.append(
                "Immediately address critical naming violations to prevent potential conflicts and maintenance issues"
            )
        
        if results["compliance_percentage"] < 70:
            recommendations.append(
                "Create and document clear naming conventions and socialize with team"
            )
            recommendations.append(
                "Consider implementing automated validation for field naming during development"
            )
        
        if len(results["by_severity"]["critical"]) == 0 and len(results["by_severity"]["medium"]) > 0:
            recommendations.append(
                "Address medium-severity naming issues in next planned refactoring cycle"
            )
        
        recommendations.append(
            "Regularly review and audit field naming as part of maintenance practices"
        )
        
        return recommendations
