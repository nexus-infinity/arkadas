"""
Trident Module - Downward to Trident validation.

Provides interface for validation through the Trident system,
ensuring data integrity and correctness through three-pronged validation.
"""

from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum


class ValidationResult(Enum):
    """Result of validation check."""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    PENDING = "pending"


class ValidationRule:
    """Individual validation rule."""
    
    def __init__(self, 
                 rule_id: str,
                 rule_name: str,
                 validator: Callable[[Any], bool],
                 error_message: str = ""):
        """
        Initialize validation rule.
        
        Args:
            rule_id: Unique rule identifier
            rule_name: Human-readable rule name
            validator: Function that returns True if valid
            error_message: Error message for failures
        """
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.validator = validator
        self.error_message = error_message or f"{rule_name} validation failed"
        self.times_applied = 0
        self.times_passed = 0
        
    def validate(self, data: Any) -> bool:
        """
        Validate data against this rule.
        
        Args:
            data: Data to validate
            
        Returns:
            True if validation passes
        """
        self.times_applied += 1
        result = self.validator(data)
        if result:
            self.times_passed += 1
        return result
    
    def get_pass_rate(self) -> float:
        """Get pass rate for this rule."""
        if self.times_applied == 0:
            return 0.0
        return self.times_passed / self.times_applied


class TridentProng(Enum):
    """Three prongs of Trident validation."""
    STRUCTURAL = "structural"   # Data structure and format
    SEMANTIC = "semantic"       # Meaning and logic
    SECURITY = "security"       # Security and safety


class ValidationReport:
    """Report from Trident validation."""
    
    def __init__(self, data_id: str):
        """
        Initialize validation report.
        
        Args:
            data_id: Identifier for validated data
        """
        self.data_id = data_id
        self.timestamp = datetime.now()
        self.prong_results: Dict[TridentProng, ValidationResult] = {}
        self.rule_results: Dict[str, bool] = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def add_prong_result(self, prong: TridentProng, result: ValidationResult):
        """Add result for a prong."""
        self.prong_results[prong] = result
        
    def add_rule_result(self, rule_id: str, passed: bool, error: str = ""):
        """Add result for a specific rule."""
        self.rule_results[rule_id] = passed
        if not passed and error:
            self.errors.append(error)
            
    def add_warning(self, warning: str):
        """Add a warning."""
        self.warnings.append(warning)
        
    def is_valid(self) -> bool:
        """Check if overall validation passed."""
        # All prongs must pass
        for result in self.prong_results.values():
            if result == ValidationResult.FAILED:
                return False
        return True
    
    def get_summary(self) -> Dict[str, Any]:
        """Get validation summary."""
        return {
            'data_id': self.data_id,
            'timestamp': self.timestamp.isoformat(),
            'valid': self.is_valid(),
            'prong_results': {p.value: r.value for p, r in self.prong_results.items()},
            'rules_checked': len(self.rule_results),
            'rules_passed': sum(1 for p in self.rule_results.values() if p),
            'error_count': len(self.errors),
            'warning_count': len(self.warnings)
        }


class TridentValidator:
    """Three-pronged validation system."""
    
    def __init__(self):
        """Initialize Trident validator."""
        self.rules: Dict[TridentProng, List[ValidationRule]] = {
            TridentProng.STRUCTURAL: [],
            TridentProng.SEMANTIC: [],
            TridentProng.SECURITY: []
        }
        self.validation_history: List[ValidationReport] = []
        self.strict_mode = False
        
    def add_rule(self, prong: TridentProng, rule: ValidationRule):
        """
        Add a validation rule to a prong.
        
        Args:
            prong: Trident prong to add rule to
            rule: Validation rule
        """
        self.rules[prong].append(rule)
        
    def validate(self, data: Any, data_id: str = "unknown") -> ValidationReport:
        """
        Perform full Trident validation.
        
        Args:
            data: Data to validate
            data_id: Identifier for data
            
        Returns:
            ValidationReport with results
        """
        report = ValidationReport(data_id)
        
        # Validate through each prong
        for prong, rules in self.rules.items():
            prong_passed = True
            
            for rule in rules:
                passed = rule.validate(data)
                report.add_rule_result(rule.rule_id, passed, rule.error_message)
                
                if not passed:
                    prong_passed = False
                    if self.strict_mode:
                        # In strict mode, fail fast
                        break
                        
            if prong_passed:
                report.add_prong_result(prong, ValidationResult.PASSED)
            else:
                report.add_prong_result(prong, ValidationResult.FAILED)
                
        self.validation_history.append(report)
        return report
    
    def quick_validate(self, data: Any) -> bool:
        """
        Quick validation check (returns boolean only).
        
        Args:
            data: Data to validate
            
        Returns:
            True if valid
        """
        report = self.validate(data, "quick_check")
        return report.is_valid()
    
    def validate_structural(self, data: Any) -> bool:
        """
        Validate only structural prong.
        
        Args:
            data: Data to validate
            
        Returns:
            True if structural validation passes
        """
        rules = self.rules[TridentProng.STRUCTURAL]
        return all(rule.validate(data) for rule in rules)
    
    def validate_semantic(self, data: Any) -> bool:
        """
        Validate only semantic prong.
        
        Args:
            data: Data to validate
            
        Returns:
            True if semantic validation passes
        """
        rules = self.rules[TridentProng.SEMANTIC]
        return all(rule.validate(data) for rule in rules)
    
    def validate_security(self, data: Any) -> bool:
        """
        Validate only security prong.
        
        Args:
            data: Data to validate
            
        Returns:
            True if security validation passes
        """
        rules = self.rules[TridentProng.SECURITY]
        return all(rule.validate(data) for rule in rules)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get validation statistics.
        
        Returns:
            Statistics dictionary
        """
        total_validations = len(self.validation_history)
        passed_validations = sum(1 for r in self.validation_history if r.is_valid())
        
        prong_stats = {}
        for prong in TridentProng:
            rules = self.rules[prong]
            prong_stats[prong.value] = {
                'rule_count': len(rules),
                'average_pass_rate': sum(r.get_pass_rate() for r in rules) / len(rules) if rules else 0.0
            }
        
        return {
            'total_validations': total_validations,
            'passed_validations': passed_validations,
            'pass_rate': passed_validations / total_validations if total_validations > 0 else 0.0,
            'prong_statistics': prong_stats,
            'strict_mode': self.strict_mode
        }
    
    def clear_history(self):
        """Clear validation history."""
        self.validation_history.clear()
        
    def set_strict_mode(self, enabled: bool):
        """
        Enable or disable strict mode.
        
        Args:
            enabled: True to enable strict mode
        """
        self.strict_mode = enabled
