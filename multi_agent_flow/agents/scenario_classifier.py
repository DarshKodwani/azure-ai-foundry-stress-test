"""
Scenario Classification Agent for Multi-Agent Financial Stress Test Workflow

This agent is responsible for:
- Classifying and categorizing stress test scenarios
- Mapping user requirements to appropriate scenario types
- Validating scenario parameters and feasibility
- Providing detailed scenario specifications for analysis
"""

from typing import Dict, Any, List, Optional, Tuple
import json
import math
from datetime import datetime
from dataclasses import asdict

from ..shared.state_manager import AgentOutput, WorkflowStage, WorkflowState
from ..shared.user_interaction import UserInteraction, ValidationResult


class ScenarioClassifier:
    """
    Scenario Classification Agent for Financial Stress Testing.
    
    This agent takes the requirements from the Requirements Analyst and
    classifies appropriate stress scenarios, validates their parameters,
    and prepares detailed scenario specifications for the analysis phase.
    """
    
    def __init__(self, user_interaction: UserInteraction):
        """
        Initialize the Scenario Classifier.
        
        Args:
            user_interaction: UserInteraction instance for CLI handling
        """
        self.agent_name = "Scenario Classifier"
        self.stage = WorkflowStage.SCENARIO_CLASSIFICATION
        self.ui = user_interaction
        
        # Scenario categories and frameworks (parameters will be generated dynamically by LLM)
        self.scenario_categories = {
            "market_risk": {
                "description": "Scenarios focusing on market price movements and volatility",
                "risk_factors": ["equity_prices", "bond_yields", "volatility", "correlations"],
                "complexity": "moderate"
            },
            "interest_rate_risk": {
                "description": "Scenarios focusing on yield curve and duration risks", 
                "risk_factors": ["yield_curve", "duration", "convexity", "basis_risk"],
                "complexity": "moderate"
            },
            "credit_risk": {
                "description": "Scenarios focusing on credit quality and default risks",
                "risk_factors": ["credit_spreads", "default_rates", "recovery_rates", "migration_risk"],
                "complexity": "high"
            },
            "liquidity_risk": {
                "description": "Scenarios focusing on market liquidity and funding constraints",
                "risk_factors": ["bid_ask_spreads", "market_depth", "funding_costs", "liquidation_costs"],
                "complexity": "high"
            },
            "operational_risk": {
                "description": "Scenarios focusing on operational failures and business disruption",
                "risk_factors": ["operational_losses", "business_disruption", "reputation_risk", "regulatory_fines"],
                "complexity": "variable"
            },
            "geopolitical_risk": {
                "description": "Scenarios focusing on political and regulatory changes",
                "risk_factors": ["policy_changes", "trade_disruption", "currency_volatility", "sanctions"],
                "complexity": "high"
            },
            "climate_risk": {
                "description": "Scenarios focusing on climate transition and physical risks",
                "risk_factors": ["stranded_assets", "transition_costs", "physical_damages", "policy_shifts"],
                "complexity": "very_high"
            }
        }
        
        # Risk factor correlation matrices for different market conditions
        self.correlation_adjustments = {
            "normal": {
                "equity_bond": -0.2,
                "equity_credit": 0.7,
                "bond_credit": -0.3
            },
            "stress": {
                "equity_bond": 0.3,
                "equity_credit": 0.9,
                "bond_credit": 0.5
            },
            "crisis": {
                "equity_bond": 0.8,
                "equity_credit": 0.95,
                "bond_credit": 0.8
            }
        }
    
    def classify_scenarios(self, workflow_state: WorkflowState) -> AgentOutput:
        """
        Main method to classify and prepare stress test scenarios.
        
        Args:
            workflow_state: Current workflow state with requirements
            
        Returns:
            AgentOutput with classified scenarios and specifications
        """
        self.ui.display_stage_header(
            self.stage,
            "Classifying stress scenarios and preparing detailed specifications"
        )
        
        try:
            # Get requirements from previous stage
            requirements_output = self._get_requirements_output(workflow_state)
            if not requirements_output:
                raise ValueError("Requirements analysis output not found in workflow state")
            
            requirements = requirements_output.data.get("requirements", {})
            config = requirements_output.data.get("configuration", {})
            
            # Classify scenarios based on requirements
            classified_scenarios = self._classify_scenarios_for_portfolio(requirements, config)
            
            # Validate scenario feasibility
            validation_results = self._validate_scenarios(classified_scenarios, requirements)
            
            # Generate scenario specifications
            scenario_specs = self._generate_scenario_specifications(classified_scenarios, requirements)
            
            # Create recommendations for scenario selection
            recommendations = self._generate_scenario_recommendations(
                classified_scenarios, validation_results, requirements
            )
            
            # Prepare output data
            output_data = {
                "classified_scenarios": classified_scenarios,
                "scenario_specifications": scenario_specs,
                "validation_results": validation_results,
                "correlation_matrices": self._build_correlation_matrices(classified_scenarios),
                "risk_factor_mappings": self._map_risk_factors(classified_scenarios),
                "execution_sequence": self._determine_execution_sequence(classified_scenarios)
            }
            
            # Create agent output
            output = AgentOutput(
                agent_name=self.agent_name,
                stage=self.stage,
                summary=self._create_summary(classified_scenarios, validation_results),
                key_findings=self._extract_key_findings(classified_scenarios, validation_results),
                recommendations=recommendations,
                data=output_data,
                errors=validation_results.get("errors", []),
                timestamp=datetime.now().isoformat()
            )
            
            # Display results to user
            self.ui.display_agent_output(output)
            
            return output
            
        except Exception as e:
            error_msg = f"Error in scenario classification: {str(e)}"
            self.ui.display_error(error_msg, self.stage)
            
            return AgentOutput(
                agent_name=self.agent_name,
                stage=self.stage,
                summary="Scenario classification failed due to error",
                key_findings=[],
                recommendations=["Review requirements output and try again"],
                data={},
                errors=[error_msg],
                timestamp=datetime.now().isoformat()
            )
    
    def _get_requirements_output(self, workflow_state: WorkflowState) -> Optional[AgentOutput]:
        """Get the requirements analysis output from workflow state."""
        for output in workflow_state.agent_outputs:
            if output.stage == WorkflowStage.REQUIREMENTS_ANALYSIS:
                return output
        return None
    
    def _classify_scenarios_for_portfolio(self, requirements: Dict[str, Any], 
                                        config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Classify appropriate scenarios based on portfolio requirements using LLM-generated parameters."""
        portfolio_type = requirements.get("portfolio_type")
        risk_tolerance = requirements.get("risk_tolerance")
        time_horizon = requirements.get("time_horizon", 5)
        
        classified_scenarios = []
        
        # Get scenario recommendations from requirements analysis
        scenario_details = config.get("stress_test_config", {}).get("scenario_details", {})
        
        for scenario_name, scenario_info in scenario_details.items():
            # Determine category and severity from scenario info
            category = self._map_scenario_to_category(scenario_name, scenario_info)
            severity = self._determine_severity(risk_tolerance, time_horizon, scenario_info)
            
            # Check if scenario is applicable to portfolio type
            if self._is_scenario_applicable(category, portfolio_type):
                # Generate intelligent parameters using LLM
                parameters = self._generate_scenario_parameters({
                    "name": scenario_name,
                    "category": category,
                    "severity": severity
                }, requirements)
                
                classified_scenario = {
                    "name": scenario_name,
                    "display_name": scenario_info.get("name", scenario_name.replace("_", " ").title()),
                    "category": category,
                    "severity": severity,
                    "parameters": parameters,
                    "rationale": scenario_info.get("rationale", "LLM-generated scenario based on current research"),
                    "description": scenario_info.get("description", "Dynamically generated stress scenario"),
                    "applicable": True,
                    "priority": self._calculate_priority(scenario_name, portfolio_type, risk_tolerance, scenario_info),
                    "complexity_assessment": self._assess_scenario_complexity(parameters, category),
                    "research_basis": self._get_research_basis(category, severity)
                }
                
                classified_scenarios.append(classified_scenario)
        
        # Add custom scenarios if any
        custom_scenarios = requirements.get("custom_scenarios", [])
        for custom in custom_scenarios:
            # Generate parameters for custom scenarios
            custom_category = custom.get("type", "market_risk")
            custom_severity = custom.get("severity", "moderate")
            
            custom_parameters = self._generate_scenario_parameters({
                "name": f"custom_{custom.get('name', 'scenario').lower().replace(' ', '_')}",
                "category": custom_category,
                "severity": custom_severity
            }, requirements)
            
            classified_scenario = {
                "name": f"custom_{custom.get('name', 'scenario').lower().replace(' ', '_')}",
                "display_name": custom.get("name", "Custom Scenario"),
                "category": custom_category,
                "severity": custom_severity,
                "parameters": custom_parameters,
                "rationale": "User-defined custom scenario with LLM-generated parameters",
                "description": f"Custom {custom_category} scenario",
                "applicable": True,
                "priority": 1.0,  # Custom scenarios get high priority
                "custom": True,
                "complexity_assessment": self._assess_scenario_complexity(custom_parameters, custom_category),
                "research_basis": "User-specified requirements with intelligent parameter generation"
            }
            classified_scenarios.append(classified_scenario)
        
        # Sort by priority (highest first)
        classified_scenarios.sort(key=lambda x: x["priority"], reverse=True)
        
        return classified_scenarios
    
    def _map_scenario_to_category(self, scenario_name: str, scenario_info: Dict[str, Any]) -> str:
        """Map scenario names to risk categories."""
        name_lower = scenario_name.lower()
        
        if "market" in name_lower or "crash" in name_lower or "equity" in name_lower:
            return "market_risk"
        elif "interest" in name_lower or "rate" in name_lower or "yield" in name_lower:
            return "interest_rate_risk"
        elif "credit" in name_lower or "default" in name_lower:
            return "credit_risk"
        elif "liquidity" in name_lower or "funding" in name_lower:
            return "liquidity_risk"
        elif "operational" in name_lower or "cyber" in name_lower:
            return "operational_risk"
        elif "geopolitical" in name_lower or "political" in name_lower:
            return "geopolitical_risk"
        elif "climate" in name_lower or "environmental" in name_lower:
            return "climate_risk"
        else:
            # Try to infer from primary risks
            primary_risks = scenario_info.get("primary_risks", [])
            if any("equity" in risk or "market" in risk for risk in primary_risks):
                return "market_risk"
            elif any("credit" in risk or "default" in risk for risk in primary_risks):
                return "credit_risk"
            else:
                return "market_risk"  # Default fallback
    
    def _is_scenario_applicable(self, category: str, portfolio_type: str) -> bool:
        """Determine if a scenario category is applicable to a portfolio type."""
        applicability_matrix = {
            "market_risk": ["equity_portfolio", "mixed_portfolio", "hedge_fund", "pension_fund"],
            "interest_rate_risk": ["fixed_income", "bank_portfolio", "insurance_portfolio", "pension_fund"],
            "credit_risk": ["bank_portfolio", "fixed_income", "mixed_portfolio"],
            "liquidity_risk": ["hedge_fund", "bank_portfolio", "mixed_portfolio"],
            "operational_risk": ["bank_portfolio", "insurance_portfolio", "hedge_fund"],
            "geopolitical_risk": ["equity_portfolio", "mixed_portfolio", "hedge_fund", "pension_fund"],
            "climate_risk": ["pension_fund", "insurance_portfolio", "mixed_portfolio"]
        }
        
        applicable_portfolios = applicability_matrix.get(category, [])
        return portfolio_type in applicable_portfolios or len(applicable_portfolios) == 0
    
    def _assess_scenario_complexity(self, parameters: Dict[str, Any], category: str) -> Dict[str, Any]:
        """Assess computational complexity of scenario based on parameters."""
        base_complexity = self.scenario_categories.get(category, {}).get("complexity", "moderate")
        
        # Count number of parameters as complexity indicator
        param_count = len(parameters)
        
        if param_count <= 4:
            computational_complexity = "low"
        elif param_count <= 8:
            computational_complexity = "moderate"
        else:
            computational_complexity = "high"
        
        # Adjust based on specific parameters
        if "correlation" in str(parameters).lower():
            computational_complexity = "high"
        if "monte_carlo" in str(parameters).lower():
            computational_complexity = "very_high"
        
        return {
            "base_complexity": base_complexity,
            "computational_complexity": computational_complexity,
            "parameter_count": param_count,
            "estimated_runtime_minutes": param_count * 2,
            "memory_requirements": "high" if computational_complexity in ["high", "very_high"] else "medium"
        }
    
    def _get_research_basis(self, category: str, severity: str) -> str:
        """Provide research basis for scenario parameters."""
        research_context = {
            "market_risk": "Based on current market volatility research, correlation studies, and historical stress periods",
            "interest_rate_risk": "Informed by yield curve modeling, duration analysis, and monetary policy research",
            "credit_risk": "Grounded in credit cycle analysis, default rate studies, and recovery rate research",
            "liquidity_risk": "Based on market microstructure research and liquidity risk modeling",
            "operational_risk": "Informed by operational loss databases and business continuity research",
            "geopolitical_risk": "Based on political risk analysis and global economic impact studies",
            "climate_risk": "Grounded in climate science, transition pathway analysis, and physical risk modeling"
        }
        
        base_context = research_context.get(category, "Based on general financial risk research")
        severity_note = f" with {severity} severity parameters calibrated to current market conditions"
        
        return base_context + severity_note
    
    def _determine_severity(self, risk_tolerance: str, time_horizon: int, scenario_info: Dict[str, Any] = None) -> str:
        """Determine scenario severity based on risk tolerance, time horizon, and scenario characteristics."""
        # Base severity from risk tolerance
        if risk_tolerance == "conservative":
            base_severity = "mild"
        elif risk_tolerance == "aggressive":
            base_severity = "severe"
        else:
            base_severity = "moderate"
        
        # Adjust for time horizon
        if time_horizon <= 1 and base_severity != "severe":
            # Short horizons may need more immediate severe shocks
            severity_levels = ["mild", "moderate", "severe"]
            current_index = severity_levels.index(base_severity)
            base_severity = severity_levels[min(current_index + 1, 2)]
        
        # Adjust based on scenario-specific characteristics
        if scenario_info:
            complexity = scenario_info.get("complexity", "moderate")
            if complexity == "high" and base_severity == "mild":
                base_severity = "moderate"  # High complexity scenarios warrant at least moderate severity
        
        return base_severity
    
    def _calculate_priority(self, scenario_name: str, portfolio_type: str, 
                          risk_tolerance: str, scenario_info: Dict[str, Any] = None) -> float:
        """Calculate priority score for scenario selection using intelligent weighting."""
        base_priority = 0.5
        
        # Get applicability score from scenario info if available
        if scenario_info:
            base_priority = scenario_info.get("applicability_score", base_priority)
        
        # Portfolio-specific priority adjustments
        portfolio_weights = {
            "equity_portfolio": {
                "market": 1.0, "geopolitical": 0.7, "liquidity": 0.5
            },
            "fixed_income": {
                "interest_rate": 1.0, "credit": 0.9, "market": 0.6
            },
            "bank_portfolio": {
                "credit": 1.0, "operational": 0.9, "liquidity": 0.8, "interest_rate": 0.7
            },
            "insurance_portfolio": {
                "interest_rate": 0.9, "operational": 0.8, "climate": 0.7
            },
            "hedge_fund": {
                "liquidity": 1.0, "market": 0.9, "operational": 0.6
            },
            "pension_fund": {
                "interest_rate": 0.9, "market": 0.8, "climate": 0.7
            },
            "mixed_portfolio": {
                "market": 0.8, "interest_rate": 0.7, "credit": 0.6
            }
        }
        
        # Find matching category weight
        category_weights = portfolio_weights.get(portfolio_type, {})
        for category_key, weight in category_weights.items():
            if category_key in scenario_name.lower():
                base_priority *= weight
                break
        
        # Risk tolerance adjustments
        if risk_tolerance == "aggressive":
            base_priority *= 1.15  # Aggressive investors want comprehensive testing
        elif risk_tolerance == "conservative":
            base_priority *= 0.9   # Conservative investors focus on key risks
        
        # Ensure priority stays within bounds
        return min(max(base_priority, 0.1), 1.0)
    
    def _build_custom_parameters(self, custom_scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Build parameters for custom scenarios."""
        scenario_type = custom_scenario.get("type", "combined")
        severity = custom_scenario.get("severity", "moderate")
        
        # Use template parameters as base
        if scenario_type in ["market", "combined"]:
            base_params = self.scenario_templates["market_crash"]["severity_levels"][severity]
        elif scenario_type == "credit":
            base_params = self.scenario_templates["credit_crisis"]["severity_levels"][severity]
        elif scenario_type == "operational":
            base_params = self.scenario_templates["operational_risk"]["severity_levels"][severity]
        else:
            base_params = self.scenario_templates["market_crash"]["severity_levels"][severity]
        
        return base_params.copy()
    
    def _validate_scenarios(self, scenarios: List[Dict[str, Any]], 
                          requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Validate scenario feasibility and parameters."""
        validation = {
            "is_valid": True,
            "warnings": [],
            "errors": [],
            "recommendations": []
        }
        
        portfolio_value = requirements.get("portfolio_value", 0)
        time_horizon = requirements.get("time_horizon", 5)
        
        # Check if we have enough scenarios
        if len(scenarios) < 2:
            validation["warnings"].append("Limited number of scenarios may not provide comprehensive stress testing")
        
        # Validate parameter ranges
        for scenario in scenarios:
            params = scenario.get("parameters", {})
            
            # Check for extreme parameters
            if "equity_shock" in params and abs(params["equity_shock"]) > 0.6:
                validation["warnings"].append(f"Extreme equity shock ({params['equity_shock']:.1%}) in {scenario['display_name']}")
            
            if "parallel_shift" in params and abs(params["parallel_shift"]) > 0.05:
                validation["warnings"].append(f"Very large interest rate shift ({params['parallel_shift']:.1%}) in {scenario['display_name']}")
            
            # Check computational feasibility
            if "liquidity_reduction" in params and params["liquidity_reduction"] > 0.8:
                validation["recommendations"].append(f"High liquidity reduction in {scenario['display_name']} may require extended computation time")
        
        # Check scenario diversity
        categories = set(s["category"] for s in scenarios)
        if len(categories) < 2:
            validation["recommendations"].append("Consider adding scenarios from different risk categories for comprehensive testing")
        
        # Validate for portfolio size
        if portfolio_value > 10000000000:  # $10B+
            validation["recommendations"].append("Large portfolio may benefit from additional granular scenarios")
        
        return validation
    
    def _generate_scenario_specifications(self, scenarios: List[Dict[str, Any]], 
                                        requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed specifications for each scenario."""
        specs = {}
        
        for scenario in scenarios:
            scenario_name = scenario["name"]
            specs[scenario_name] = {
                "scenario_id": scenario_name,
                "display_name": scenario["display_name"],
                "category": scenario["category"],
                "severity": scenario["severity"],
                "parameters": scenario["parameters"],
                "execution_config": self._build_execution_config(scenario, requirements),
                "expected_impact": self._estimate_impact(scenario, requirements),
                "computation_complexity": self._assess_complexity(scenario),
                "validation_metrics": self._define_validation_metrics(scenario)
            }
        
        return specs
    
    def _build_execution_config(self, scenario: Dict[str, Any], 
                              requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Build execution configuration for a scenario."""
        return {
            "simulation_runs": 10000,
            "time_steps": max(252, requirements.get("time_horizon", 5) * 252),  # Daily steps
            "confidence_levels": [0.95, 0.99, 0.999],
            "rebalancing_frequency": "monthly",
            "include_transaction_costs": True,
            "monte_carlo_seed": 42
        }
    
    def _estimate_impact(self, scenario: Dict[str, Any], 
                        requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate expected impact of scenario."""
        params = scenario.get("parameters", {})
        portfolio_value = requirements.get("portfolio_value", 0)
        
        # Rough impact estimation
        estimated_loss_pct = 0.0
        
        if "equity_shock" in params:
            estimated_loss_pct += abs(params["equity_shock"]) * 0.6  # Assume 60% equity exposure
        
        if "bond_shock" in params:
            estimated_loss_pct += abs(params["bond_shock"]) * 0.3  # Assume 30% bond exposure
        
        if "credit_spread_widening" in params:
            estimated_loss_pct += params["credit_spread_widening"] * 0.4  # Credit sensitivity
        
        estimated_loss_amount = portfolio_value * estimated_loss_pct
        
        return {
            "estimated_loss_percentage": estimated_loss_pct,
            "estimated_loss_amount": estimated_loss_amount,
            "confidence_level": 0.8,  # 80% confidence in estimate
            "impact_category": self._categorize_impact(estimated_loss_pct)
        }
    
    def _categorize_impact(self, loss_pct: float) -> str:
        """Categorize impact severity."""
        if loss_pct < 0.05:
            return "low"
        elif loss_pct < 0.15:
            return "medium"
        elif loss_pct < 0.30:
            return "high"
        else:
            return "severe"
    
    def _assess_complexity(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Assess computational complexity of scenario."""
        params = scenario.get("parameters", {})
        
        complexity_score = 1.0
        
        # Add complexity for correlation adjustments
        if scenario["category"] in ["market_risk", "credit_risk"]:
            complexity_score += 0.5
        
        # Add complexity for custom scenarios
        if scenario.get("custom", False):
            complexity_score += 0.3
        
        # Add complexity for liquidity modeling
        if "liquidity_reduction" in params:
            complexity_score += 0.4
        
        return {
            "complexity_score": complexity_score,
            "estimated_runtime_minutes": complexity_score * 5,
            "memory_requirements": "medium" if complexity_score < 2.0 else "high",
            "parallel_processing": complexity_score > 1.5
        }
    
    def _define_validation_metrics(self, scenario: Dict[str, Any]) -> List[str]:
        """Define validation metrics for scenario results."""
        metrics = [
            "value_at_risk_95",
            "value_at_risk_99",
            "expected_shortfall_95",
            "maximum_drawdown",
            "volatility_ratio"
        ]
        
        category = scenario["category"]
        
        if category == "market_risk":
            metrics.extend(["beta_stability", "correlation_breakdown"])
        elif category == "credit_risk":
            metrics.extend(["default_rate_accuracy", "recovery_rate_validation"])
        elif category == "liquidity_risk":
            metrics.extend(["liquidity_ratio", "funding_gap"])
        elif category == "operational_risk":
            metrics.extend(["operational_loss_distribution", "business_continuity_impact"])
        
        return metrics
    
    def _build_correlation_matrices(self, scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build correlation matrices for different market conditions."""
        matrices = {}
        
        for condition in ["normal", "stress", "crisis"]:
            matrices[condition] = self.correlation_adjustments[condition].copy()
        
        return matrices
    
    def _map_risk_factors(self, scenarios: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Map scenarios to their primary risk factors."""
        risk_factor_map = {}
        
        for scenario in scenarios:
            scenario_name = scenario["name"]
            category = scenario["category"]
            
            if category == "market_risk":
                risk_factor_map[scenario_name] = ["equity_prices", "bond_yields", "volatility"]
            elif category == "interest_rate_risk":
                risk_factor_map[scenario_name] = ["yield_curve", "duration", "convexity"]
            elif category == "credit_risk":
                risk_factor_map[scenario_name] = ["credit_spreads", "default_rates", "recovery_rates"]
            elif category == "liquidity_risk":
                risk_factor_map[scenario_name] = ["bid_ask_spreads", "market_depth", "funding_costs"]
            elif category == "operational_risk":
                risk_factor_map[scenario_name] = ["operational_losses", "business_disruption", "reputation"]
            else:
                risk_factor_map[scenario_name] = ["multiple_factors"]
        
        return risk_factor_map
    
    def _determine_execution_sequence(self, scenarios: List[Dict[str, Any]]) -> List[str]:
        """Determine optimal execution sequence for scenarios."""
        # Sort by complexity (simple first) and priority
        sorted_scenarios = sorted(scenarios, key=lambda x: (
            self._assess_complexity(x)["complexity_score"],
            -x["priority"]
        ))
        
        return [s["name"] for s in sorted_scenarios]
    
    def _generate_scenario_recommendations(self, scenarios: List[Dict[str, Any]], 
                                         validation: Dict[str, Any],
                                         requirements: Dict[str, Any]) -> List[str]:
        """Generate recommendations for scenario execution."""
        recommendations = []
        
        # Scenario-specific recommendations
        high_priority_scenarios = [s for s in scenarios if s["priority"] > 0.8]
        if high_priority_scenarios:
            recommendations.append(f"Prioritize execution of {len(high_priority_scenarios)} high-priority scenarios")
        
        # Custom scenario recommendations
        custom_scenarios = [s for s in scenarios if s.get("custom", False)]
        if custom_scenarios:
            recommendations.append(f"Validate custom scenario parameters before execution")
        
        # Computational recommendations
        complex_scenarios = [s for s in scenarios if self._assess_complexity(s)["complexity_score"] > 2.0]
        if complex_scenarios:
            recommendations.append("Consider parallel processing for computationally intensive scenarios")
        
        # Portfolio-specific recommendations
        portfolio_type = requirements.get("portfolio_type")
        if portfolio_type == "bank_portfolio":
            recommendations.append("Ensure regulatory capital calculations are included in stress tests")
        elif portfolio_type == "insurance_portfolio":
            recommendations.append("Include asset-liability matching analysis in scenario evaluation")
        
        # Add validation recommendations
        recommendations.extend(validation.get("recommendations", []))
        
        return recommendations
    
    def _create_summary(self, scenarios: List[Dict[str, Any]], 
                       validation: Dict[str, Any]) -> str:
        """Create a summary of the scenario classification."""
        num_scenarios = len(scenarios)
        categories = set(s["category"] for s in scenarios)
        high_priority = len([s for s in scenarios if s["priority"] > 0.8])
        
        summary = f"""
Classified {num_scenarios} stress test scenarios across {len(categories)} risk categories.
{high_priority} high-priority scenarios identified for immediate execution.
Validation: {'Passed' if validation.get('is_valid') else 'Failed'} with {len(validation.get('warnings', []))} warnings.
Scenarios ready for analysis planning phase.
        """.strip()
        
        return summary
    
    def _extract_key_findings(self, scenarios: List[Dict[str, Any]], 
                            validation: Dict[str, Any]) -> List[str]:
        """Extract key findings from scenario classification."""
        findings = []
        
        categories = set(s["category"] for s in scenarios)
        findings.append(f"Scenarios cover {len(categories)} risk categories: {', '.join(categories)}")
        
        severity_levels = set(s["severity"] for s in scenarios)
        findings.append(f"Severity levels included: {', '.join(severity_levels)}")
        
        custom_count = len([s for s in scenarios if s.get("custom", False)])
        if custom_count > 0:
            findings.append(f"{custom_count} custom scenarios defined by user")
        
        total_complexity = sum(self._assess_complexity(s)["complexity_score"] for s in scenarios)
        findings.append(f"Total computational complexity score: {total_complexity:.1f}")
        
        if validation.get("warnings"):
            findings.append(f"{len(validation['warnings'])} validation warnings require attention")
        
        return findings
    
    def _generate_scenario_parameters(self, scenario_info: Dict[str, Any], 
                                    requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent scenario parameters based on LLM research and current market conditions."""
        scenario_name = scenario_info.get("name", "unknown")
        category = scenario_info.get("category", "market_risk")
        severity = scenario_info.get("severity", "moderate")
        portfolio_type = requirements.get("portfolio_type")
        time_horizon = requirements.get("time_horizon", 5)
        
        # Generate parameters based on current research and market understanding
        if category == "market_risk":
            return self._generate_market_risk_parameters(severity, portfolio_type, time_horizon)
        elif category == "interest_rate_risk":
            return self._generate_interest_rate_parameters(severity, portfolio_type, time_horizon)
        elif category == "credit_risk":
            return self._generate_credit_risk_parameters(severity, portfolio_type)
        elif category == "liquidity_risk":
            return self._generate_liquidity_risk_parameters(severity, portfolio_type)
        elif category == "operational_risk":
            return self._generate_operational_risk_parameters(severity, portfolio_type)
        elif category == "geopolitical_risk":
            return self._generate_geopolitical_risk_parameters(severity, time_horizon)
        elif category == "climate_risk":
            return self._generate_climate_risk_parameters(severity, time_horizon)
        else:
            return self._generate_default_parameters(severity)
    
    def _generate_market_risk_parameters(self, severity: str, portfolio_type: str, time_horizon: int) -> Dict[str, Any]:
        """Generate market risk parameters based on current volatility research and market conditions."""
        # Base parameters informed by current market research
        if severity == "mild":
            equity_shock = -0.12 if time_horizon <= 2 else -0.08  # Short-term vs long-term perspective
            volatility_multiplier = 1.3
        elif severity == "severe":
            equity_shock = -0.45 if portfolio_type == "equity_portfolio" else -0.35
            volatility_multiplier = 2.8
        else:  # moderate
            equity_shock = -0.25 if portfolio_type in ["equity_portfolio", "hedge_fund"] else -0.20
            volatility_multiplier = 2.0
        
        # Adjust for portfolio-specific characteristics
        bond_shock = equity_shock * 0.3  # Historically bonds less volatile than equities
        credit_spread_widening = abs(equity_shock) * 0.15  # Credit spreads widen with equity stress
        
        return {
            "equity_shock": equity_shock,
            "bond_shock": bond_shock,
            "credit_spread_widening": credit_spread_widening,
            "volatility_multiplier": volatility_multiplier,
            "correlation_adjustment": min(abs(equity_shock) * 0.8, 0.4),  # Correlations increase in stress
            "sector_rotation_factor": 0.2 if portfolio_type == "equity_portfolio" else 0.1,
            "liquidity_impact": 0.15 if severity == "severe" else 0.05
        }
    
    def _generate_interest_rate_parameters(self, severity: str, portfolio_type: str, time_horizon: int) -> Dict[str, Any]:
        """Generate interest rate parameters based on current yield environment and monetary policy research."""
        # Parameters reflecting current rate environment and potential policy paths
        if severity == "mild":
            parallel_shift = 0.0075  # 75 bps
            steepening = 0.004
        elif severity == "severe":
            parallel_shift = 0.035   # 350 bps - extreme but not impossible
            steepening = 0.025
        else:  # moderate
            parallel_shift = 0.018   # 180 bps
            steepening = 0.012
        
        # Duration impact varies by portfolio type
        duration_multiplier = 1.8 if portfolio_type == "fixed_income" else 1.3
        
        return {
            "parallel_shift": parallel_shift,
            "steepening": steepening,
            "flattening": -steepening * 0.6,  # Flattening typically smaller magnitude
            "duration_impact": duration_multiplier,
            "convexity_effect": 0.15 if severity == "severe" else 0.08,
            "yield_volatility_increase": 1.5 if severity == "severe" else 1.2,
            "curve_twist_probability": 0.3  # Probability of non-parallel movements
        }
    
    def _generate_credit_risk_parameters(self, severity: str, portfolio_type: str) -> Dict[str, Any]:
        """Generate credit risk parameters based on current credit cycle research."""
        # Parameters reflecting current credit conditions and historical patterns
        if severity == "mild":
            default_rate_increase = 0.015
            spread_widening = 0.018
            recovery_decline = 0.08
        elif severity == "severe":
            default_rate_increase = 0.12   # Reflecting severe recession conditions
            spread_widening = 0.085
            recovery_decline = 0.40
        else:  # moderate
            default_rate_increase = 0.055
            spread_widening = 0.045
            recovery_decline = 0.22
        
        # Adjust for portfolio type
        if portfolio_type == "bank_portfolio":
            default_rate_increase *= 1.2  # Banks more exposed to credit cycles
        
        return {
            "default_rate_increase": default_rate_increase,
            "credit_spread_widening": spread_widening,
            "recovery_rate_decline": recovery_decline,
            "rating_migration_intensity": 1.5 if severity == "severe" else 1.2,
            "credit_correlation_increase": 0.25 if severity == "severe" else 0.15,
            "liquidity_premium": 0.008 if severity == "severe" else 0.003
        }
    
    def _generate_liquidity_risk_parameters(self, severity: str, portfolio_type: str) -> Dict[str, Any]:
        """Generate liquidity risk parameters based on current market microstructure research."""
        if severity == "mild":
            spread_widening = 2.2
            depth_reduction = 0.25
            liquidation_discount = 0.03
        elif severity == "severe":
            spread_widening = 12.0
            depth_reduction = 0.85
            liquidation_discount = 0.35
        else:  # moderate
            spread_widening = 6.5
            depth_reduction = 0.55
            liquidation_discount = 0.18
        
        # Hedge funds face higher liquidity stress
        if portfolio_type == "hedge_fund":
            liquidation_discount *= 1.3
        
        return {
            "bid_ask_spread_widening": spread_widening,
            "market_depth_reduction": depth_reduction,
            "asset_liquidation_discount": liquidation_discount,
            "funding_cost_increase": liquidation_discount * 0.4,
            "redemption_pressure": 0.2 if portfolio_type == "hedge_fund" else 0.05,
            "cash_drag": 0.02 if severity == "severe" else 0.005
        }
    
    def _generate_operational_risk_parameters(self, severity: str, portfolio_type: str) -> Dict[str, Any]:
        """Generate operational risk parameters based on current operational risk research."""
        if severity == "mild":
            direct_loss = 0.008
            disruption_days = 3
            reputation_impact = 0.015
        elif severity == "severe":
            direct_loss = 0.18
            disruption_days = 120
            reputation_impact = 0.30
        else:  # moderate
            direct_loss = 0.06
            disruption_days = 25
            reputation_impact = 0.12
        
        # Banks and insurance companies face higher operational risks
        if portfolio_type in ["bank_portfolio", "insurance_portfolio"]:
            direct_loss *= 1.4
            reputation_impact *= 1.2
        
        return {
            "direct_loss_percentage": direct_loss,
            "business_disruption_days": disruption_days,
            "reputation_impact": reputation_impact,
            "regulatory_fine": direct_loss * 0.3,
            "client_attrition_rate": reputation_impact * 0.5,
            "recovery_time_months": disruption_days / 15  # Rough conversion
        }
    
    def _generate_geopolitical_risk_parameters(self, severity: str, time_horizon: int) -> Dict[str, Any]:
        """Generate geopolitical risk parameters based on current global risk assessment."""
        if severity == "mild":
            market_volatility_increase = 0.3
            trade_disruption = 0.05
        elif severity == "severe":
            market_volatility_increase = 2.5
            trade_disruption = 0.4
        else:  # moderate
            market_volatility_increase = 1.2
            trade_disruption = 0.18
        
        return {
            "market_volatility_increase": market_volatility_increase,
            "trade_disruption_factor": trade_disruption,
            "currency_volatility_multiplier": 1.5 if severity == "severe" else 1.2,
            "supply_chain_impact": trade_disruption * 0.7,
            "policy_uncertainty_index": 2.0 if severity == "severe" else 1.3,
            "duration_months": min(time_horizon * 12, 36) if severity == "severe" else 6
        }
    
    def _generate_climate_risk_parameters(self, severity: str, time_horizon: int) -> Dict[str, Any]:
        """Generate climate risk parameters based on current climate science and transition research."""
        if time_horizon < 5:
            # Short-term focus on acute physical events and immediate policy changes
            physical_impact = 0.02 if severity == "mild" else (0.08 if severity == "severe" else 0.04)
            transition_impact = 0.03 if severity == "mild" else (0.15 if severity == "severe" else 0.08)
        else:
            # Long-term focus on structural changes
            physical_impact = 0.05 if severity == "mild" else (0.25 if severity == "severe" else 0.12)
            transition_impact = 0.08 if severity == "mild" else (0.40 if severity == "severe" else 0.20)
        
        return {
            "physical_risk_impact": physical_impact,
            "transition_risk_impact": transition_impact,
            "stranded_asset_ratio": transition_impact * 0.6,
            "carbon_price_shock": 50 if severity == "mild" else (200 if severity == "severe" else 100),
            "regulatory_tightening_factor": 1.3 if severity == "severe" else 1.1,
            "technology_disruption_rate": 0.15 if time_horizon >= 10 else 0.05
        }
    
    def _generate_default_parameters(self, severity: str) -> Dict[str, Any]:
        """Generate default parameters for unknown scenario types."""
        if severity == "mild":
            impact_factor = 0.05
        elif severity == "severe":
            impact_factor = 0.25
        else:  # moderate
            impact_factor = 0.12
        
        return {
            "general_impact_factor": impact_factor,
            "volatility_multiplier": 1 + impact_factor * 4,
            "correlation_adjustment": impact_factor * 0.8,
            "duration_days": 30 if severity == "mild" else (180 if severity == "severe" else 90)
        }


def create_scenario_classifier(user_interaction: UserInteraction) -> ScenarioClassifier:
    """
    Factory function to create a ScenarioClassifier instance.
    
    Args:
        user_interaction: UserInteraction instance for CLI handling
        
    Returns:
        ScenarioClassifier instance
    """
    return ScenarioClassifier(user_interaction)
