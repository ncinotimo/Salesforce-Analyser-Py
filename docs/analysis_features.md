# Analysis Features

This guide covers the analysis capabilities provided by the Salesforce/nCino Analyzer.

## Naming Convention Analysis

The naming convention analyzer evaluates field names against nCino standards and best practices.

### What It Detects

1. **Standard Prefixes**:
   - `LLC_BI__` prefix for managed package fields
   - `nc_` prefix for custom project-specific fields

2. **Object-Specific Patterns**:
   - Standard patterns like `LLC_BI__Loan__c` and `LLC_BI__*__c`
   - Custom patterns like `nc_Loan_*__c` and `nc_*__c`

3. **Invalid Patterns**:
   - Fields starting with lowercase letters
   - Direct usage of `Loan_` or `loan_` prefixes without proper namespace
   - Fields ending with `__X` instead of `__c`

### Severity Levels

The analyzer categorizes violations into three severity levels:

- **Critical**: Issues that could cause conflicts, data corruption, or system instability
- **Medium**: Consistency issues that impact maintainability
- **Low**: Minor formatting or style issues

### Recommendations

For each violation, the analyzer provides:
- Specific recommendation for fixing the naming issue
- Overall recommendations to improve naming convention compliance
- Compliance percentage score

## Validation Rule Bypass Pattern Analysis

The validation rule analyzer detects bypass patterns that could create security risks or maintenance challenges.

### What It Detects

1. **Profile-Based Bypasses**:
   - Checks that use `$Profile.Name` to bypass rules for specific profiles
   - Example: `AND(condition, $Profile.Name != 'System Administrator')`

2. **User ID Bypasses**:
   - Hardcoded User IDs in validation rules
   - Example: `$User.Id = '005000000000001'`

3. **Custom Permission Bypasses**:
   - Using permissions to bypass validation rules
   - Example: `NOT($Permission.Bypass_Validation)`

4. **Record Type Bypasses**:
   - Rules that apply differently based on record type
   - Example: `RecordType.Name != 'Business_Loan'`

5. **Owner ID Bypasses**:
   - Rules that behave differently for record owners
   - Example: `OwnerId = $User.Id`

### Severity Levels

- **High**: Direct security risks like hardcoded User IDs
- **Medium**: Maintenance risks like profile-based checks
- **Low**: Minor issues like inconsistent permission usage

### Security Score

The analyzer calculates a security score (0-100) based on:
- Percentage of rules with bypass patterns
- Severity of detected patterns
- Consistency of implementation

## Apex Trigger Bypass Pattern Analysis

The Apex trigger analyzer identifies security patterns and bypass mechanisms in trigger code.

### What It Detects

1. **Feature Management Permission Checks**:
   - Usage of `FeatureManagement.checkPermission`
   - Example: `if (FeatureManagement.checkPermission('Bypass_Trigger'))`

2. **Custom Setting Bypasses**:
   - Using custom settings to control trigger execution
   - Example: `if (TriggerSettings__c.getInstance().IsActive__c)`

3. **Hardcoded ID Checks**:
   - Hardcoded User IDs or Profile IDs in code
   - Example: `if (UserInfo.getUserId() == '005000000000001')`

4. **Profile Name Checks**:
   - Bypasses based on profile names
   - Example: `if (UserInfo.getProfileId() == '00e000000000001')`

### Recommendations

For each pattern, the analyzer provides:
- Description of the risk
- Recommended approach
- Refactoring priorities

## Comprehensive Reporting

The analyzer can generate comprehensive reports combining all analyses.

### Report Components

1. **Executive Summary**:
   - Overall assessment
   - Key findings
   - Risk breakdown by severity

2. **Detailed Findings**:
   - Field naming convention violations
   - Validation rule bypass patterns
   - Apex trigger security issues

3. **Recommendations**:
   - Prioritized list of issues to address
   - General recommendations for improvement
   - Best practices to implement

4. **Overall Configuration Health Score**:
   - Combined score (0-100)
   - Rating (Critical, Poor, Fair, Good, Excellent)
   - Component-specific scores

## Analysis Examples

### Naming Convention Analysis Example

```python
# Analyze field naming conventions
results = naming_analyzer.analyze_fields(fields)
summary = naming_analyzer.generate_summary_report(results)

print(f"Compliance: {results['compliance_percentage']}%")
print(f"Critical violations: {len(results['by_severity']['critical'])}")
```

### Validation Rule Analysis Example

```python
# Analyze validation rule bypass patterns
results = bypass_analyzer.analyze_validation_rules(validation_rules)
priorities = bypass_analyzer.generate_refactoring_priorities(results, 'validation')

print(f"Security score: {results['security_score']}/100")
print(f"Rules with bypasses: {results['bypass_percentage']}%")
```

### Comprehensive Analysis Example

```python
# Generate comprehensive report
report = generate_comprehensive_report({
    "naming_conventions": naming_results,
    "validation_rules": validation_results,
    "triggers": trigger_results
})

print(f"Overall score: {report['overall_score']['score']}/100")
print(f"Rating: {report['overall_score']['rating']}")
```

## Best Practices for Analysis

1. **Regular Scanning**: Incorporate analysis into CI/CD pipelines
2. **Baseline Comparison**: Track changes in scores over time
3. **Risk Prioritization**: Address high and medium issues first
4. **Documentation**: Document exceptions to standard patterns
5. **Team Training**: Use findings to educate development team

## Analysis Algorithm Details

### Naming Convention Analysis

The naming convention analyzer uses regular expressions to match field names against defined patterns.

Example pattern:
```python
{
    "pattern": re.compile(r"^LLC_BI__"),
    "description": "Managed package fields from nCino",
    "expected": True
}
```

### Bypass Pattern Detection

The bypass pattern analyzer uses regex patterns to identify security concerns.

Example pattern:
```python
{
    "name": "User ID bypass",
    "regex": re.compile(r"\$User\.Id\s*=[=!]=|\$User\.Id.*CONTAINS"),
    "severity": "High"
}
```

### Scoring Calculation

The security score is calculated using a weighted approach:
- Start with a perfect score (100)
- Deduct for percentage of components with bypass patterns
- Apply higher deductions for high severity issues
- Apply moderate deductions for medium severity issues