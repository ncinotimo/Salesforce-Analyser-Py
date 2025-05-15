"""
Bypass Pattern Analyzer

This module provides functionality for detecting bypass patterns in
Salesforce/nCino validation rules and Apex triggers.
"""

import re
from typing import Dict, List, Any, Union, Tuple

class BypassPatternAnalyzer:
    """
    Class for analyzing Salesforce/nCino validation rules and Apex triggers for bypass patterns.
    """
    
    def __init__(self):
        """
        Initialize the analyzer with defined bypass patterns.
        """
        self.validation_rule_patterns = [
            {
                "name": "Profile-based bypass",
                "regex": re.compile(r"\$Profile\.Name\s*=[=!]=|\$Profile\.Name.*CONTAINS"),
                "severity": "Medium",
                "description": "Using Profile.Name to bypass validation rules creates maintenance challenges when profiles change and makes rules difficult to manage at scale.",
                "recommended_approach": "Use custom permissions instead, which are more maintainable and explicit."
            },
            {
                "name": "Custom permission bypass",
                "regex": re.compile(r"NOT\(\$Permission\.[^)]+\)"),
                "severity": "Low",
                "description": "Using NOT with permissions is generally acceptable but should be documented and consistently implemented.",
                "recommended_approach": "Ensure permission names are consistently structured with prefixes like 'Bypass_' for clarity."
            },
            {
                "name": "User ID bypass",
                "regex": re.compile(r"\$User\.Id\s*=[=!]=|\$User\.Id.*CONTAINS"),
                "severity": "High",
                "description": "Hardcoding specific User IDs creates significant maintenance issues and security risks.",
                "recommended_approach": "Use permission sets, custom permissions, or roles instead of specific User IDs."
            },
            {
                "name": "Record Type bypass",
                "regex": re.compile(r"RecordType\.Name\s*!=|RecordType\.Name\s*<>"),
                "severity": "Medium",
                "description": "Explicitly excluding certain record types can create maintenance challenges.",
                "recommended_approach": "Use explicit inclusion rather than exclusion when possible."
            },
            {
                "name": "Owner ID bypass",
                "regex": re.compile(r"OwnerId\s*=[=!]=\s*\$User\.Id"),
                "severity": "Medium",
                "description": "Bypassing validation for record owners may create inconsistent data validation.",
                "recommended_approach": "Consider permission-based approaches that don't depend on record ownership."
            }
        ]

        self.apex_trigger_patterns = [
            {
                "name": "Feature management permission check",
                "regex": re.compile(r"FeatureManagement\.checkPermission\s*\(\s*['\"]([\w_]+)['\"]"),
                "severity": "Low",
                "description": "Using FeatureManagement to check permissions is recommended, but should be implemented consistently.",
                "recommended_approach": "Use a consistent pattern like return !FeatureManagement.checkPermission('Bypass_Trigger');"
            },
            {
                "name": "Custom setting bypass",
                "regex": re.compile(r"([\w_]+__c)\.([\w_]+__c)"),
                "severity": "Medium",
                "description": "Using custom settings to control trigger execution can create maintenance challenges.",
                "recommended_approach": "Document the custom setting usage and ensure consistent implementation."
            },
            {
                "name": "Hardcoded User ID check",
                "regex": re.compile(r"Id\s*==\s*['\"]005[A-Za-z0-9]{12,15}['\"]"),
                "severity": "High",
                "description": "Hardcoding User IDs creates significant maintenance issues and security risks.",
                "recommended_approach": "Use permission sets, custom permissions, or roles instead of specific User IDs."
            },
            {
                "name": "Profile name check",
                "regex": re.compile(r"profile\.name\s*==\s*['\"]|userinfo\.getprofileid\(\)\s*==\s*['\"]", re.IGNORECASE),
                "severity": "Medium",
                "description": "Using profile names or IDs to bypass logic creates maintenance challenges.",
                "recommended_approach": "Use custom permissions instead of relying on profiles."
            }
        ]

        self.flow_patterns = [
            {
                "name": "Permission-based bypass",
                "location_pattern": re.compile(r"Start|Decision"),
                "condition_pattern": re.compile(r"\$Permission\."),
                "severity": "Low",
                "description": "Using permissions to control flow execution is a recommended pattern when implemented consistently.",
                "recommended_approach": "Use a consistent naming convention for bypass permissions."
            },
            {
                "name": "Profile-based bypass",
                "location_pattern": re.compile(r"Start|Decision"),
                "condition_pattern": re.compile(r"\$Profile\."),
                "severity": "Medium",
                "description": "Using profiles to control flow execution creates maintenance challenges.",
                "recommended_approach": "Use custom permissions instead of relying on profiles."
            },
            {
                "name": "User ID bypass",
                "location_pattern": re.compile(r"Start|Decision"),
                "condition_pattern": re.compile(r"\$User\.Id"),
                "severity": "High",
                "description": "Hardcoding User IDs creates significant maintenance issues and security risks.",
                "recommended_approach": "Use permission sets, custom permissions, or roles instead of specific User IDs."
            }
        ]

    def analyze_validation_rules(self, validation_rules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze validation rules for bypass patterns.
        
        Args:
            validation_rules: List of validation rule metadata objects
            
        Returns:
            Dictionary containing analysis results
        """
        if not validation_rules or not isinstance(validation_rules, list):
            raise ValueError("Validation rule data must be provided as a list")

        results = {
            "bypass_patterns": [],
            "rules_by_pattern": {},
            "rules_by_severity": {
                "High": [],
                "Medium": [],
                "Low": []
            },
            "total_rules": len(validation_rules),
            "rules_with_bypass": 0
        }

        # Initialize pattern tracking
        for pattern in self.validation_rule_patterns:
            results["rules_by_pattern"][pattern["name"]] = []

        # Analyze each validation rule
        for rule in validation_rules:
            api_name = rule.get("apiName") or rule.get("fullName") or ""
            formula = rule.get("errorConditionFormula") or rule.get("formula") or ""
            found_patterns = []

            # Check for each bypass pattern
            for pattern in self.validation_rule_patterns:
                if pattern["regex"].search(formula):
                    found_patterns.append({
                        "name": pattern["name"],
                        "severity": pattern["severity"],
                        "description": pattern["description"],
                        "recommended_approach": pattern["recommended_approach"]
                    })
                    results["rules_by_pattern"][pattern["name"]].append(api_name)

            # If patterns were found, add to results
            if found_patterns:
                highest_severity = self.determine_highest_severity(found_patterns)
                rule_with_patterns = {
                    "apiName": api_name,
                    "active": rule.get("active", False),
                    "description": rule.get("description", ""),
                    "patterns": found_patterns,
                    "highest_severity": highest_severity
                }

                results["bypass_patterns"].append(rule_with_patterns)
                results["rules_by_severity"][highest_severity].append(api_name)
                results["rules_with_bypass"] += 1

        # Calculate percentage of rules with bypass patterns
        results["bypass_percentage"] = round((results["rules_with_bypass"] / results["total_rules"]) * 100) if results["total_rules"] > 0 else 0
        
        # Calculate security score (0-100)
        results["security_score"] = self.calculate_security_score(results)

        return results

    def analyze_apex_triggers(self, triggers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze Apex triggers for bypass patterns.
        
        Args:
            triggers: List of Apex trigger metadata objects
            
        Returns:
            Dictionary containing analysis results
        """
        if not triggers or not isinstance(triggers, list):
            raise ValueError("Trigger data must be provided as a list")

        results = {
            "bypass_patterns": [],
            "triggers_by_pattern": {},
            "triggers_by_severity": {
                "High": [],
                "Medium": [],
                "Low": []
            },
            "total_triggers": len(triggers),
            "triggers_with_bypass": 0
        }

        # Initialize pattern tracking
        for pattern in self.apex_trigger_patterns:
            results["triggers_by_pattern"][pattern["name"]] = []

        # Analyze each trigger
        for trigger in triggers:
            name = trigger.get("name") or ""
            content = trigger.get("content") or trigger.get("code") or ""
            found_patterns = []

            # Check for each bypass pattern
            for pattern in self.apex_trigger_patterns:
                if pattern["regex"].search(content):
                    found_patterns.append({
                        "name": pattern["name"],
                        "severity": pattern["severity"],
                        "description": pattern["description"],
                        "recommended_approach": pattern["recommended_approach"]
                    })
                    results["triggers_by_pattern"][pattern["name"]].append(name)

            # If patterns were found, add to results
            if found_patterns:
                highest_severity = self.determine_highest_severity(found_patterns)
                trigger_with_patterns = {
                    "name": name,
                    "active": trigger.get("active", False),
                    "patterns": found_patterns,
                    "highest_severity": highest_severity
                }

                results["bypass_patterns"].append(trigger_with_patterns)
                results["triggers_by_severity"][highest_severity].append(name)
                results["triggers_with_bypass"] += 1

        # Calculate percentage of triggers with bypass patterns
        results["bypass_percentage"] = round((results["triggers_with_bypass"] / results["total_triggers"]) * 100) if results["total_triggers"] > 0 else 0
        
        # Calculate security score (0-100)
        results["security_score"] = self.calculate_security_score(results, 'trigger')

        return results

    def determine_highest_severity(self, patterns: List[Dict[str, Any]]) -> str:
        """
        Determine the highest severity from a list of patterns.
        
        Args:
            patterns: Found patterns with severity levels
            
        Returns:
            Highest severity: 'High', 'Medium', or 'Low'
        """
        if any(p["severity"] == "High" for p in patterns):
            return "High"
        if any(p["severity"] == "Medium" for p in patterns):
            return "Medium"
        return "Low"

    def calculate_security_score(self, results: Dict[str, Any], component_type: str = 'validation') -> int:
        """
        Calculate a security score based on the analysis results.
        
        Args:
            results: Analysis results
            component_type: Type of component ('validation' or 'trigger')
            
        Returns:
            Security score (0-100)
        """
        # Start with a perfect score
        score = 100
        
        # Determine which results to use based on type
        if component_type == 'trigger':
            components_with_bypass = results["triggers_with_bypass"]
            total_components = results["total_triggers"]
            high_severity_components = len(results["triggers_by_severity"]["High"])
            medium_severity_components = len(results["triggers_by_severity"]["Medium"])
        else:  # validation
            components_with_bypass = results["rules_with_bypass"]
            total_components = results["total_rules"]
            high_severity_components = len(results["rules_by_severity"]["High"])
            medium_severity_components = len(results["rules_by_severity"]["Medium"])
        
        # Deduct for percentage of components with bypass
        if total_components > 0:
            bypass_percentage = (components_with_bypass / total_components) * 100
            score -= bypass_percentage * 0.3  # Deduct up to 30 points for 100% bypass
        
        # Deduct for high severity issues
        score -= high_severity_components * 5  # Deduct 5 points per high severity issue
        
        # Deduct for medium severity issues
        score -= medium_severity_components * 2  # Deduct 2 points per medium severity issue
        
        # Ensure score stays within 0-100 range
        return max(0, min(100, round(score)))

    def generate_refactoring_priorities(self, results: Dict[str, Any], component_type: str = 'validation') -> List[Dict[str, Any]]:
        """
        Generate a prioritized list of components to refactor.
        
        Args:
            results: Analysis results
            component_type: Type of component ('validation' or 'trigger')
            
        Returns:
            Prioritized list of components to refactor
        """
        components = results["bypass_patterns"]
        
        # Define a helper function for sorting
        def severity_order(item):
            severity_values = {"High": 0, "Medium": 1, "Low": 2}
            return (
                severity_values.get(item["highest_severity"], 3),
                item.get("apiName", "") if "apiName" in item else item.get("name", "")
            )
        
        # Sort by severity (High, Medium, Low) and then by name
        return sorted(components, key=severity_order)

    def generate_general_recommendations(self, results: Dict[str, Any], component_type: str = 'validation') -> List[str]:
        """
        Generate general recommendations based on analysis results.
        
        Args:
            results: Analysis results
            component_type: Type of component ('validation' or 'trigger')
            
        Returns:
            List of general recommendations
        """
        recommendations = []
        
        # Common recommendations
        recommendations.append(
            "Implement a consistent approach to bypass logic across all components"
        )
        
        recommendations.append(
            "Use custom permissions instead of profiles or user IDs for bypass logic"
        )
        
        recommendations.append(
            "Document all bypass mechanisms in a central location for security review"
        )
        
        # Type-specific recommendations
        if component_type == 'validation':
            if len(results["rules_by_severity"]["High"]) > 0:
                recommendations.append(
                    "Immediately refactor validation rules with hardcoded User IDs"
                )
            
            if results.get("bypass_percentage", 0) > 50:
                recommendations.append(
                    "Review overall validation strategy to reduce reliance on bypass patterns"
                )
        elif component_type == 'trigger':
            if len(results["triggers_by_severity"]["High"]) > 0:
                recommendations.append(
                    "Immediately refactor triggers with hardcoded User IDs or Profile checks"
                )
            
            recommendations.append(
                "Implement a centralized trigger handler framework with consistent bypass logic"
            )
        
        return recommendations
