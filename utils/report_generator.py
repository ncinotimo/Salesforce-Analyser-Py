"""
Report Generator

This module provides functionality for generating comprehensive reports
from analysis results.
"""

from typing import Dict, List, Any, Optional, Union

def generate_comprehensive_report(analyses: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a comprehensive report combining all analyses.
    
    Args:
        analyses: Dictionary containing various analysis results
        
    Returns:
        Dictionary containing the comprehensive report
    """
    # Create report structure
    report = {
        "executive_summary": generate_executive_summary(analyses),
        "detailed_findings": {},
        "recommendations": generate_recommendations(analyses),
        "overall_score": calculate_overall_score(analyses)
    }
    
    # Add detailed findings
    if "naming_conventions" in analyses:
        report["detailed_findings"]["naming_conventions"] = {
            "compliance_percentage": analyses["naming_conventions"].get("compliance_percentage", 0),
            "violations": [{
                "field": v.get("apiName", ""),
                "issues": [issue.get("rule", "") for issue in v.get("violations", [])],
                "recommendation": v.get("recommended_fix", "")
            } for v in analyses["naming_conventions"].get("violations", [])],
            "top_issues": analyses.get("naming_conventions_summary", {}).get("top_issues", [])
        }
    
    if "validation_rules" in analyses:
        report["detailed_findings"]["validation_rules"] = {
            "security_score": analyses["validation_rules"].get("security_score", 0),
            "bypass_percentage": analyses["validation_rules"].get("bypass_percentage", 0),
            "patterns": [{
                "rule": p.get("apiName", ""),
                "patterns": [pattern.get("name", "") for pattern in p.get("patterns", [])],
                "severity": p.get("highest_severity", "")
            } for p in analyses["validation_rules"].get("bypass_patterns", [])],
            "refactoring_priorities": analyses.get("validation_rules_refactoring_priorities", [])[:5]
        }
    
    if "triggers" in analyses:
        report["detailed_findings"]["triggers"] = {
            "security_score": analyses["triggers"].get("security_score", 0),
            "bypass_percentage": analyses["triggers"].get("bypass_percentage", 0),
            "patterns": [{
                "trigger": p.get("name", ""),
                "patterns": [pattern.get("name", "") for pattern in p.get("patterns", [])],
                "severity": p.get("highest_severity", "")
            } for p in analyses["triggers"].get("bypass_patterns", [])],
            "refactoring_priorities": analyses.get("triggers_refactoring_priorities", [])[:5]
        }
    
    return report

def generate_executive_summary(analyses: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate an executive summary from analysis results.
    
    Args:
        analyses: Dictionary containing various analysis results
        
    Returns:
        Dictionary containing the executive summary
    """
    summary = {
        "overall_assessment": "",
        "key_findings": [],
        "risks_identified": {
            "critical": 0,
            "medium": 0,
            "low": 0
        }
    }
    
    # Count risks by severity
    if "naming_conventions" in analyses:
        summary["risks_identified"]["critical"] += len(analyses["naming_conventions"].get("by_severity", {}).get("critical", []))
        summary["risks_identified"]["medium"] += len(analyses["naming_conventions"].get("by_severity", {}).get("medium", []))
        summary["risks_identified"]["low"] += len(analyses["naming_conventions"].get("by_severity", {}).get("low", []))
    
    if "validation_rules" in analyses:
        summary["risks_identified"]["critical"] += len(analyses["validation_rules"].get("rules_by_severity", {}).get("High", []))
        summary["risks_identified"]["medium"] += len(analyses["validation_rules"].get("rules_by_severity", {}).get("Medium", []))
        summary["risks_identified"]["low"] += len(analyses["validation_rules"].get("rules_by_severity", {}).get("Low", []))
    
    if "triggers" in analyses:
        summary["risks_identified"]["critical"] += len(analyses["triggers"].get("triggers_by_severity", {}).get("High", []))
        summary["risks_identified"]["medium"] += len(analyses["triggers"].get("triggers_by_severity", {}).get("Medium", []))
        summary["risks_identified"]["low"] += len(analyses["triggers"].get("triggers_by_severity", {}).get("Low", []))
    
    # Generate overall assessment
    total_issues = summary["risks_identified"]["critical"] + summary["risks_identified"]["medium"] + summary["risks_identified"]["low"]
    critical_percent = (summary["risks_identified"]["critical"] / total_issues) * 100 if total_issues > 0 else 0
    
    if summary["risks_identified"]["critical"] > 5 or critical_percent > 20:
        summary["overall_assessment"] = 'Critical attention required. The configuration contains significant risk factors that should be addressed immediately.'
    elif summary["risks_identified"]["critical"] > 0 or summary["risks_identified"]["medium"] > 10:
        summary["overall_assessment"] = 'Moderate risk identified. The configuration has several issues that should be addressed in the near term.'
    else:
        summary["overall_assessment"] = 'Low risk identified. The configuration is generally sound with minor improvements recommended.'
    
    # Add key findings
    if "naming_conventions" in analyses:
        summary["key_findings"].append(f"{analyses['naming_conventions'].get('compliance_percentage', 0)}% of fields comply with naming conventions.")
    
    if "validation_rules" in analyses:
        summary["key_findings"].append(f"{analyses['validation_rules'].get('bypass_percentage', 0)}% of validation rules contain bypass patterns.")
    
    if "triggers" in analyses:
        summary["key_findings"].append(f"{analyses['triggers'].get('bypass_percentage', 0)}% of Apex triggers contain bypass patterns.")
    
    return summary

def generate_recommendations(analyses: Dict[str, Any]) -> List[str]:
    """
    Generate recommendations from analysis results.
    
    Args:
        analyses: Dictionary containing various analysis results
        
    Returns:
        List of recommendations
    """
    recommendations = []
    
    # Add naming convention recommendations
    if "naming_conventions_summary" in analyses and "recommendations" in analyses["naming_conventions_summary"]:
        recommendations.extend(analyses["naming_conventions_summary"]["recommendations"])
    
    # Add validation rule recommendations
    if "validation_rules_recommendations" in analyses:
        recommendations.extend(analyses["validation_rules_recommendations"])
    
    # Add trigger recommendations
    if "triggers_recommendations" in analyses:
        recommendations.extend(analyses["triggers_recommendations"])
    
    # Add general recommendations
    recommendations.extend([
        "Implement a governance process to regularly review and audit configuration changes.",
        "Document all configuration standards and patterns in a central location.",
        "Provide training to developers on secure and maintainable configuration practices."
    ])
    
    # Remove any duplicates
    return list(dict.fromkeys(recommendations))

def calculate_overall_score(analyses: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate an overall score based on analysis results.
    
    Args:
        analyses: Dictionary containing various analysis results
        
    Returns:
        Dictionary containing the overall score
    """
    scores = []
    weights = []
    
    if "naming_conventions" in analyses:
        scores.append(analyses["naming_conventions"].get("compliance_percentage", 0))
        weights.append(1)
    
    if "validation_rules" in analyses:
        scores.append(analyses["validation_rules"].get("security_score", 0))
        weights.append(1.5)
    
    if "triggers" in analyses:
        scores.append(analyses["triggers"].get("security_score", 0))
        weights.append(1.5)
    
    # Calculate weighted average
    if not scores:
        return {"score": 0, "rating": "N/A"}
    
    total_weight = sum(weights)
    weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
    weighted_average = round(weighted_sum / total_weight)
    
    # Determine rating
    if weighted_average >= 90:
        rating = "Excellent"
    elif weighted_average >= 75:
        rating = "Good"
    elif weighted_average >= 60:
        rating = "Fair"
    elif weighted_average >= 40:
        rating = "Poor"
    else:
        rating = "Critical"
    
    return {
        "score": weighted_average,
        "rating": rating,
        "component_scores": {
            "naming_conventions": analyses.get("naming_conventions", {}).get("compliance_percentage", 0),
            "validation_rules": analyses.get("validation_rules", {}).get("security_score", 0),
            "triggers": analyses.get("triggers", {}).get("security_score", 0)
        }
    }
