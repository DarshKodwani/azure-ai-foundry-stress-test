"""
Agents Package for Multi-Agent Financial Stress Test Workflow

This package contains all the specialized agents for the financial stress test workflow:
- RequirementsAnalyst: Analyzes user requirements and sets up stress test parameters
- DataCollector: Gathers and validates financial data
- ScenarioGenerator: Creates and configures stress test scenarios  
- AnalysisEngine: Performs the core stress test calculations
- RiskAssessor: Evaluates risk metrics and exposure analysis
- ReportGenerator: Creates comprehensive stress test reports
"""

from .requirements_analyst import RequirementsAnalyst, create_requirements_analyst
from .scenario_classifier import ScenarioClassifier, create_scenario_classifier

__all__ = [
    'RequirementsAnalyst',
    'create_requirements_analyst',
    'ScenarioClassifier', 
    'create_scenario_classifier'
]
