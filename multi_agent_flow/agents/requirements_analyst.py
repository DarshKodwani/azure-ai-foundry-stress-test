"""
Requirements Analyst Agent for Multi-Agent Financial Stress Test Workflow

This agent is responsible for:
- Analyzing user requirements for stress testing
- Validating input parameters and constraints
- Setting up the foundation for subsequent analysis stages
- Providing recommendations for stress test configuration
"""

from typing import Dict, Any, List, Optional, Tuple
import json
import os
from datetime import datetime
from dataclasses import asdict

from ..shared.state_manager import AgentOutput, WorkflowStage, WorkflowState
from ..shared.user_interaction import UserInteraction, ValidationResult


class RequirementsAnalyst:
    """
    Requirements Analyst Agent for Financial Stress Testing.
    
    This agent analyzes user requirements and sets up the foundation
    for the stress test workflow. It validates parameters, identifies
    constraints, and provides configuration recommendations.
    """
    
    def __init__(self, user_interaction: UserInteraction):
        """
        Initialize the Requirements Analyst.
        
        Args:
            user_interaction: UserInteraction instance for CLI handling
        """
        self.agent_name = "Requirements Analyst"
        self.stage = WorkflowStage.REQUIREMENTS_ANALYSIS
        self.ui = user_interaction
        
        # Default stress test parameters
        self.default_scenarios = {
            "market_crash": {
                "name": "Market Crash Scenario",
                "equity_shock": -0.30,  # 30% equity decline
                "bond_shock": -0.10,    # 10% bond decline
                "credit_spread_widening": 0.03,  # 300 bps widening
                "duration": "1_year"
            },
            "interest_rate_shock": {
                "name": "Interest Rate Shock",
                "rate_increase": 0.02,  # 200 bps increase
                "yield_curve_shift": "parallel",
                "duration": "immediate"
            },
            "credit_crisis": {
                "name": "Credit Crisis",
                "default_rate_increase": 0.05,  # 5% increase in default rates
                "credit_spread_widening": 0.05,  # 500 bps widening
                "liquidity_reduction": 0.40,    # 40% liquidity reduction
                "duration": "2_years"
            },
            "combined_scenario": {
                "name": "Combined Stress Scenario",
                "equity_shock": -0.25,
                "bond_shock": -0.08,
                "rate_increase": 0.015,
                "credit_spread_widening": 0.04,
                "duration": "1_year"
            }
        }
        
        # Supported portfolio types
        self.portfolio_types = {
            "equity_portfolio": "Equity-focused investment portfolio",
            "fixed_income": "Fixed income/bond portfolio",
            "mixed_portfolio": "Mixed asset allocation portfolio",
            "hedge_fund": "Alternative investment/hedge fund portfolio",
            "pension_fund": "Pension fund portfolio",
            "insurance_portfolio": "Insurance company investment portfolio",
            "bank_portfolio": "Banking institution portfolio"
        }
    
    def analyze_requirements(self, workflow_state: WorkflowState) -> AgentOutput:
        """
        Main method to analyze user requirements for stress testing.
        
        Args:
            workflow_state: Current workflow state
            
        Returns:
            AgentOutput with requirements analysis results
        """
        self.ui.display_stage_header(
            self.stage, 
            "Analyzing user requirements and setting up stress test parameters"
        )
        
        try:
            # Collect user requirements
            requirements = self._collect_requirements()
            
            # Validate requirements
            validation_results = self._validate_requirements(requirements)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(requirements, validation_results)
            
            # Prepare output data
            output_data = {
                "requirements": requirements,
                "validation_results": validation_results,
                "recommended_scenarios": self._get_recommended_scenarios(requirements),
                "configuration": self._build_configuration(requirements, recommendations)
            }
            
            # Create agent output
            output = AgentOutput(
                agent_name=self.agent_name,
                stage=self.stage,
                summary=self._create_summary(requirements, validation_results),
                key_findings=self._extract_key_findings(requirements, validation_results),
                recommendations=recommendations,
                data=output_data,
                errors=validation_results.get("errors", []),
                timestamp=datetime.now().isoformat()
            )
            
            # Display results to user
            self.ui.display_agent_output(output)
            
            return output
            
        except Exception as e:
            error_msg = f"Error in requirements analysis: {str(e)}"
            self.ui.display_error(error_msg, self.stage)
            
            return AgentOutput(
                agent_name=self.agent_name,
                stage=self.stage,
                summary="Requirements analysis failed due to error",
                key_findings=[],
                recommendations=["Review input parameters and try again"],
                data={},
                errors=[error_msg],
                timestamp=datetime.now().isoformat()
            )
    
    def _collect_requirements(self) -> Dict[str, Any]:
        """Collect requirements from user input."""
        self.ui.display_info("Collecting stress test requirements...")
        
        requirements = {}
        
        # Portfolio type
        self.ui.display_info("\nAvailable portfolio types:")
        for key, description in self.portfolio_types.items():
            print(f"  {key}: {description}")
        
        portfolio_type = self.ui.get_user_input(
            "Enter portfolio type:",
            validator=lambda x: x in self.portfolio_types,
            error_msg=f"Please choose from: {', '.join(self.portfolio_types.keys())}"
        )
        requirements["portfolio_type"] = portfolio_type
        
        # Portfolio value
        portfolio_value = self.ui.get_user_input(
            "Enter total portfolio value (e.g., 100000000 for $100M):",
            validator=lambda x: x.isdigit() and int(x) > 0,
            error_msg="Please enter a positive number"
        )
        requirements["portfolio_value"] = int(portfolio_value)
        
        # Risk tolerance
        risk_tolerance = self.ui.get_user_input(
            "Enter risk tolerance (conservative/moderate/aggressive):",
            validator=lambda x: x.lower() in ["conservative", "moderate", "aggressive"],
            error_msg="Please enter: conservative, moderate, or aggressive"
        )
        requirements["risk_tolerance"] = risk_tolerance.lower()
        
        # Time horizon
        time_horizon = self.ui.get_user_input(
            "Enter investment time horizon in years (e.g., 5):",
            validator=lambda x: x.isdigit() and 1 <= int(x) <= 50,
            error_msg="Please enter a number between 1 and 50"
        )
        requirements["time_horizon"] = int(time_horizon)
        
        # Regulatory requirements
        has_regulatory = self.ui.confirm_action("Are there specific regulatory requirements (e.g., Basel III, Solvency II)?")
        if has_regulatory:
            regulatory_framework = self.ui.get_user_input("Enter regulatory framework (e.g., basel_iii, solvency_ii, none):")
            requirements["regulatory_framework"] = regulatory_framework
        else:
            requirements["regulatory_framework"] = "none"
        
        # Custom scenarios
        has_custom_scenarios = self.ui.confirm_action("Do you want to define custom stress scenarios?")
        if has_custom_scenarios:
            requirements["custom_scenarios"] = self._collect_custom_scenarios()
        else:
            requirements["custom_scenarios"] = []
        
        # Output preferences
        requirements["output_format"] = self.ui.get_user_input(
            "Preferred output format (detailed/summary/both):",
            validator=lambda x: x.lower() in ["detailed", "summary", "both"],
            error_msg="Please enter: detailed, summary, or both"
        ).lower()
        
        return requirements
    
    def _collect_custom_scenarios(self) -> List[Dict[str, Any]]:
        """Collect custom stress scenarios from user."""
        scenarios = []
        
        while True:
            self.ui.display_info(f"\nDefining custom scenario #{len(scenarios) + 1}")
            
            scenario = {}
            scenario["name"] = self.ui.get_user_input("Scenario name:")
            
            # Scenario type
            scenario_type = self.ui.get_user_input(
                "Scenario type (market/credit/operational/combined):",
                validator=lambda x: x.lower() in ["market", "credit", "operational", "combined"],
                error_msg="Please enter: market, credit, operational, or combined"
            )
            scenario["type"] = scenario_type.lower()
            
            # Severity
            severity = self.ui.get_user_input(
                "Severity level (mild/moderate/severe):",
                validator=lambda x: x.lower() in ["mild", "moderate", "severe"],
                error_msg="Please enter: mild, moderate, or severe"
            )
            scenario["severity"] = severity.lower()
            
            # Duration
            duration = self.ui.get_user_input(
                "Duration (immediate/1_month/3_months/1_year/2_years):",
                validator=lambda x: x in ["immediate", "1_month", "3_months", "1_year", "2_years"],
                error_msg="Please enter: immediate, 1_month, 3_months, 1_year, or 2_years"
            )
            scenario["duration"] = duration
            
            scenarios.append(scenario)
            
            if not self.ui.confirm_action("Add another custom scenario?"):
                break
        
        return scenarios
    
    def _validate_requirements(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the collected requirements."""
        validation = {
            "is_valid": True,
            "warnings": [],
            "errors": [],
            "recommendations": []
        }
        
        # Validate portfolio value
        portfolio_value = requirements.get("portfolio_value", 0)
        if portfolio_value < 1000000:  # Less than $1M
            validation["warnings"].append(
                f"Portfolio value ${portfolio_value:,} is relatively small for comprehensive stress testing"
            )
        elif portfolio_value > 100000000000:  # Greater than $100B
            validation["warnings"].append(
                f"Portfolio value ${portfolio_value:,} is very large - ensure sufficient computational resources"
            )
        
        # Validate risk tolerance vs portfolio type
        risk_tolerance = requirements.get("risk_tolerance")
        portfolio_type = requirements.get("portfolio_type")
        
        if risk_tolerance == "conservative" and portfolio_type in ["hedge_fund"]:
            validation["warnings"].append(
                "Conservative risk tolerance may not align with hedge fund portfolio type"
            )
        
        # Validate time horizon vs scenarios
        time_horizon = requirements.get("time_horizon", 0)
        if time_horizon < 3:
            validation["recommendations"].append(
                "Consider including immediate shock scenarios for short time horizons"
            )
        elif time_horizon > 10:
            validation["recommendations"].append(
                "Consider long-term structural change scenarios for extended time horizons"
            )
        
        # Validate regulatory framework
        regulatory = requirements.get("regulatory_framework", "none")
        if regulatory != "none" and portfolio_type in ["pension_fund", "bank_portfolio", "insurance_portfolio"]:
            validation["recommendations"].append(
                f"Ensure stress scenarios align with {regulatory} requirements"
            )
        
        return validation
    
    def _generate_recommendations(self, requirements: Dict[str, Any], 
                                validation: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on requirements and validation."""
        recommendations = []
        
        portfolio_type = requirements.get("portfolio_type")
        risk_tolerance = requirements.get("risk_tolerance")
        time_horizon = requirements.get("time_horizon", 0)
        
        # Portfolio-specific recommendations
        if portfolio_type == "equity_portfolio":
            recommendations.append("Focus on market crash and volatility scenarios")
            recommendations.append("Include sector-specific stress tests")
        elif portfolio_type == "fixed_income":
            recommendations.append("Emphasize interest rate shock scenarios")
            recommendations.append("Include credit spread widening tests")
        elif portfolio_type == "bank_portfolio":
            recommendations.append("Include credit loss scenarios")
            recommendations.append("Test liquidity stress scenarios")
        elif portfolio_type == "insurance_portfolio":
            recommendations.append("Include catastrophic event scenarios")
            recommendations.append("Test liability matching under stress")
        
        # Risk tolerance recommendations
        if risk_tolerance == "conservative":
            recommendations.append("Use moderate stress scenario parameters")
            recommendations.append("Focus on capital preservation metrics")
        elif risk_tolerance == "aggressive":
            recommendations.append("Include severe stress scenarios")
            recommendations.append("Test maximum drawdown scenarios")
        
        # Time horizon recommendations
        if time_horizon <= 2:
            recommendations.append("Focus on immediate and short-term shock scenarios")
        elif time_horizon >= 10:
            recommendations.append("Include structural change and long-term trend scenarios")
        
        # Add validation recommendations
        recommendations.extend(validation.get("recommendations", []))
        
        return recommendations
    
    def _get_recommended_scenarios(self, requirements: Dict[str, Any]) -> List[str]:
        """Get recommended stress scenarios based on requirements."""
        portfolio_type = requirements.get("portfolio_type")
        risk_tolerance = requirements.get("risk_tolerance")
        
        recommended = []
        
        # Always include market crash for most portfolios
        if portfolio_type in ["equity_portfolio", "mixed_portfolio", "hedge_fund", "pension_fund"]:
            recommended.append("market_crash")
        
        # Interest rate scenarios for fixed income
        if portfolio_type in ["fixed_income", "bank_portfolio", "insurance_portfolio", "pension_fund"]:
            recommended.append("interest_rate_shock")
        
        # Credit scenarios for credit-sensitive portfolios
        if portfolio_type in ["bank_portfolio", "fixed_income", "mixed_portfolio"]:
            recommended.append("credit_crisis")
        
        # Combined scenario for comprehensive testing
        if risk_tolerance in ["moderate", "aggressive"]:
            recommended.append("combined_scenario")
        
        return recommended
    
    def _build_configuration(self, requirements: Dict[str, Any], 
                           recommendations: List[str]) -> Dict[str, Any]:
        """Build the stress test configuration."""
        config = {
            "portfolio_config": {
                "type": requirements.get("portfolio_type"),
                "value": requirements.get("portfolio_value"),
                "risk_tolerance": requirements.get("risk_tolerance"),
                "time_horizon": requirements.get("time_horizon")
            },
            "stress_test_config": {
                "scenarios": self._get_recommended_scenarios(requirements),
                "regulatory_framework": requirements.get("regulatory_framework", "none"),
                "output_format": requirements.get("output_format", "both"),
                "custom_scenarios": requirements.get("custom_scenarios", [])
            },
            "analysis_config": {
                "include_var": True,
                "include_expected_shortfall": True,
                "confidence_levels": [0.95, 0.99],
                "monte_carlo_simulations": 10000,
                "historical_lookback_years": 10
            }
        }
        
        return config
    
    def _create_summary(self, requirements: Dict[str, Any], 
                       validation: Dict[str, Any]) -> str:
        """Create a summary of the requirements analysis."""
        portfolio_type = requirements.get("portfolio_type", "unknown")
        portfolio_value = requirements.get("portfolio_value", 0)
        risk_tolerance = requirements.get("risk_tolerance", "unknown")
        
        summary = f"""
Requirements analysis completed for {portfolio_type} portfolio valued at ${portfolio_value:,}.
Risk tolerance: {risk_tolerance}. Time horizon: {requirements.get('time_horizon', 'unknown')} years.
Regulatory framework: {requirements.get('regulatory_framework', 'none')}.
Validation: {'Passed' if validation.get('is_valid') else 'Failed'} with {len(validation.get('warnings', []))} warnings.
        """.strip()
        
        return summary
    
    def _extract_key_findings(self, requirements: Dict[str, Any], 
                            validation: Dict[str, Any]) -> List[str]:
        """Extract key findings from the requirements analysis."""
        findings = []
        
        portfolio_value = requirements.get("portfolio_value", 0)
        if portfolio_value >= 1000000000:  # $1B+
            findings.append("Large portfolio size requires comprehensive stress testing approach")
        
        portfolio_type = requirements.get("portfolio_type")
        if portfolio_type in ["bank_portfolio", "insurance_portfolio"]:
            findings.append("Regulated portfolio type requires specific regulatory compliance testing")
        
        custom_scenarios = requirements.get("custom_scenarios", [])
        if custom_scenarios:
            findings.append(f"User defined {len(custom_scenarios)} custom stress scenarios")
        
        if validation.get("warnings"):
            findings.append(f"Analysis identified {len(validation['warnings'])} potential concerns")
        
        regulatory = requirements.get("regulatory_framework", "none")
        if regulatory != "none":
            findings.append(f"Regulatory compliance required for {regulatory}")
        
        return findings


def create_requirements_analyst(user_interaction: UserInteraction) -> RequirementsAnalyst:
    """
    Factory function to create a RequirementsAnalyst instance.
    
    Args:
        user_interaction: UserInteraction instance for CLI handling
        
    Returns:
        RequirementsAnalyst instance
    """
    return RequirementsAnalyst(user_interaction)
