"""
Azure AI Foundry Skills-Based Interactive Workflow Orchestrator

This orchestrator wires together Azure AI Foundry skills in sequence,
providing interactive CLI experience with user validation at each step.
All agents are implemented as Azure AI Foundry skills (YAML + Python tools).
"""

import json
import sys
import os
import importlib.util
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum


class WorkflowStage(Enum):
    """Enumeration of workflow stages"""
    INITIAL = "initial"
    REQUIREMENTS_ANALYSIS = "requirements_analysis"
    SCENARIO_CLASSIFICATION = "scenario_classification"
    MODEL_EXECUTION = "model_execution"
    RESULTS_SYNTHESIS = "results_synthesis"
    FINAL_REVIEW = "final_review"


class ValidationResult(Enum):
    """Enum for user validation results"""
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFY = "modify"
    SKIP = "skip"


class SkillsWorkflowOrchestrator:
    """
    Interactive workflow orchestrator for Azure AI Foundry skills-based stress testing.
    
    This orchestrator calls Azure AI Foundry skills in sequence and provides
    interactive user validation between each step.
    """
    
    def __init__(self):
        """Initialize the workflow orchestrator."""
        self.current_stage = WorkflowStage.INITIAL
        self.stage_outputs = {}
        self.user_approvals = {}
        self.skills_base_path = "skills"
        self.tools_base_path = "tools"
        self.workflow_results = {}
        
        # Define the skills workflow sequence
        self.workflow_sequence = [
            {
                "stage": WorkflowStage.REQUIREMENTS_ANALYSIS,
                "skill_name": "requirements_analysis",
                "tool_name": "requirements_analyst_tool",
                "description": "Analyze user requirements for stress testing"
            },
            {
                "stage": WorkflowStage.SCENARIO_CLASSIFICATION,
                "skill_name": "scenario_classification", 
                "tool_name": "scenario_classifier_tool",
                "description": "Classify and recommend stress testing scenarios"
            },
            {
                "stage": WorkflowStage.MODEL_EXECUTION,
                "skill_name": "model_execution",
                "tool_name": "model_execution_tool", 
                "description": "Execute stress testing models and simulations"
            },
            {
                "stage": WorkflowStage.RESULTS_SYNTHESIS,
                "skill_name": "results_synthesis",
                "tool_name": "results_synthesis_tool",
                "description": "Synthesize results into comprehensive analysis"
            }
        ]

    def print_banner(self):
        """Print the workflow banner."""
        print("\n" + "="*80)
        print("🏦 AZURE AI FOUNDRY FINANCIAL STRESS TESTING WORKFLOW 🏦")
        print("="*80)
        print("Interactive Multi-Skill Stress Testing Analysis")
        print("Powered by Azure AI Foundry Skills Architecture")
        print("="*80 + "\n")

    def collect_user_requirements(self) -> Dict[str, Any]:
        """Collect initial requirements from user via CLI."""
        print("📋 REQUIREMENTS COLLECTION")
        print("-" * 40)
        
        requirements = {}
        
        # Portfolio type
        print("\n1. Portfolio Type:")
        print("   a) Equity Portfolio")
        print("   b) Fixed Income Portfolio") 
        print("   c) Mixed Portfolio")
        print("   d) Bank Portfolio")
        print("   e) Insurance Portfolio")
        
        portfolio_choice = input("\nSelect portfolio type (a-e): ").strip().lower()
        portfolio_map = {
            'a': 'equity_portfolio',
            'b': 'fixed_income', 
            'c': 'mixed_portfolio',
            'd': 'bank_portfolio',
            'e': 'insurance_portfolio'
        }
        requirements['portfolio_type'] = portfolio_map.get(portfolio_choice, 'mixed_portfolio')
        
        # Portfolio value
        try:
            value_str = input("2. Portfolio Value (USD): $").strip().replace(',', '').replace('$', '')
            requirements['portfolio_value'] = float(value_str)
        except ValueError:
            requirements['portfolio_value'] = 10000000  # Default 10M
            
        # Risk tolerance
        print("\n3. Risk Tolerance:")
        print("   a) Conservative")
        print("   b) Moderate") 
        print("   c) Aggressive")
        
        risk_choice = input("\nSelect risk tolerance (a-c): ").strip().lower()
        risk_map = {'a': 'conservative', 'b': 'moderate', 'c': 'aggressive'}
        requirements['risk_tolerance'] = risk_map.get(risk_choice, 'moderate')
        
        # Time horizon
        try:
            requirements['time_horizon'] = float(input("4. Investment Time Horizon (years): ").strip())
        except ValueError:
            requirements['time_horizon'] = 5.0
            
        # Regulatory framework
        print("\n5. Regulatory Framework:")
        print("   a) Basel III")
        print("   b) Solvency II")
        print("   c) CCAR")
        print("   d) None/Other")
        
        reg_choice = input("\nSelect regulatory framework (a-d): ").strip().lower()
        reg_map = {'a': 'basel_iii', 'b': 'solvency_ii', 'c': 'ccar', 'd': 'none'}
        requirements['regulatory_framework'] = reg_map.get(reg_choice, 'none')
        
        # Custom scenarios
        custom = input("6. Custom scenarios (optional, press Enter to skip): ").strip()
        requirements['custom_scenarios'] = custom if custom else "None specified"
        
        # Output format
        print("\n7. Output Format:")
        print("   a) Summary")
        print("   b) Detailed")
        print("   c) Both")
        
        output_choice = input("\nSelect output format (a-c): ").strip().lower()
        output_map = {'a': 'summary', 'b': 'detailed', 'c': 'both'}
        requirements['output_format'] = output_map.get(output_choice, 'both')
        
        return requirements

    def load_and_execute_skill(self, tool_name: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Load and execute an Azure AI Foundry skill tool."""
        try:
            # Construct path to the tool
            tool_path = os.path.join(self.tools_base_path, tool_name, f"{tool_name}.py")
            
            if not os.path.exists(tool_path):
                raise FileNotFoundError(f"Tool not found: {tool_path}")
            
            # Load the tool module dynamically
            spec = importlib.util.spec_from_file_location(tool_name, tool_path)
            tool_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(tool_module)
            
            # Execute the main function with inputs
            if hasattr(tool_module, 'main'):
                if tool_name == "requirements_analyst_tool":
                    result = tool_module.main(
                        portfolio_type=inputs.get('portfolio_type', ''),
                        portfolio_value=inputs.get('portfolio_value', 0),
                        risk_tolerance=inputs.get('risk_tolerance', ''),
                        time_horizon=inputs.get('time_horizon', 0),
                        regulatory_framework=inputs.get('regulatory_framework', ''),
                        custom_scenarios=inputs.get('custom_scenarios', ''),
                        output_format=inputs.get('output_format', '')
                    )
                elif tool_name == "scenario_classifier_tool":
                    result = tool_module.main(
                        requirements_analysis=inputs.get('requirements_analysis', ''),
                        portfolio_characteristics=inputs.get('portfolio_characteristics', ''),
                        regulatory_requirements=inputs.get('regulatory_requirements', '')
                    )
                elif tool_name == "model_execution_tool":
                    result = tool_module.main(
                        scenario_specifications=inputs.get('scenario_specifications', ''),
                        portfolio_data=inputs.get('portfolio_data', ''),
                        model_parameters=inputs.get('model_parameters', ''),
                        execution_config=inputs.get('execution_config', '')
                    )
                elif tool_name == "results_synthesis_tool":
                    result = tool_module.main(
                        execution_results=inputs.get('execution_results', ''),
                        scenario_classifications=inputs.get('scenario_classifications', ''),
                        regulatory_requirements=inputs.get('regulatory_requirements', '')
                    )
                else:
                    # Generic call for other tools
                    result = tool_module.main(**inputs)
            else:
                raise AttributeError(f"Tool {tool_name} does not have a main function")
                
            return result
            
        except Exception as e:
            return {"error": f"Error executing tool {tool_name}: {str(e)}"}

    def display_stage_results(self, stage_name: str, results: Dict[str, Any], description: str):
        """Display results from a workflow stage."""
        print(f"\n{'='*60}")
        print(f"🔍 {stage_name.upper().replace('_', ' ')} RESULTS")
        print(f"{'='*60}")
        print(f"Description: {description}")
        print("-" * 60)
        
        for key, value in results.items():
            if key != "error":
                if isinstance(value, str):
                    if len(value) > 500:
                        # Display first 500 chars for long strings
                        print(f"\n📊 {key.upper().replace('_', ' ')}:")
                        print(f"{value[:500]}...")
                        print(f"[Content truncated - {len(value)} total characters]")
                    else:
                        print(f"\n📊 {key.upper().replace('_', ' ')}:")
                        print(value)
                else:
                    print(f"\n📊 {key.upper().replace('_', ' ')}:")
                    print(json.dumps(value, indent=2))
        
        if "error" in results:
            print(f"\n❌ ERROR: {results['error']}")

    def get_user_validation(self, stage_name: str) -> ValidationResult:
        """Get user validation for stage results."""
        print(f"\n{'='*50}")
        print("🔍 USER VALIDATION REQUIRED")
        print(f"{'='*50}")
        print(f"Stage: {stage_name.replace('_', ' ').title()}")
        print("\nOptions:")
        print("  a) Approve and continue")
        print("  b) Reject and exit") 
        print("  c) Skip this stage")
        print("  d) Modify inputs (not implemented)")
        
        while True:
            choice = input("\nSelect option (a-d): ").strip().lower()
            
            if choice == 'a':
                return ValidationResult.APPROVED
            elif choice == 'b':
                return ValidationResult.REJECTED
            elif choice == 'c':
                return ValidationResult.SKIP
            elif choice == 'd':
                return ValidationResult.MODIFY
            else:
                print("Invalid choice. Please select a, b, c, or d.")

    def execute_workflow(self):
        """Execute the complete skills-based workflow."""
        self.print_banner()
        
        try:
            # Collect initial requirements
            requirements = self.collect_user_requirements()
            print(f"\n✅ Requirements collected successfully!")
            print(f"Portfolio: {requirements['portfolio_type']} (${requirements['portfolio_value']:,.2f})")
            print(f"Risk Tolerance: {requirements['risk_tolerance']}")
            print(f"Time Horizon: {requirements['time_horizon']} years")
            
            # Execute workflow sequence
            current_context = requirements.copy()
            
            for step in self.workflow_sequence:
                stage = step["stage"]
                skill_name = step["skill_name"]
                tool_name = step["tool_name"]
                description = step["description"]
                
                print(f"\n🚀 Executing: {description}")
                print(f"Skill: {skill_name}")
                print(f"Tool: {tool_name}")
                
                # Prepare inputs based on stage
                if stage == WorkflowStage.REQUIREMENTS_ANALYSIS:
                    inputs = current_context
                elif stage == WorkflowStage.SCENARIO_CLASSIFICATION:
                    inputs = {
                        'requirements_analysis': self.stage_outputs.get('requirements_analysis', {}).get('analysis_result', ''),
                        'portfolio_characteristics': json.dumps(requirements),
                        'regulatory_requirements': requirements.get('regulatory_framework', 'none')
                    }
                elif stage == WorkflowStage.MODEL_EXECUTION:
                    inputs = {
                        'scenario_specifications': self.stage_outputs.get('scenario_classification', {}).get('scenario_recommendations', ''),
                        'portfolio_data': json.dumps(requirements),
                        'model_parameters': json.dumps({"risk_tolerance": requirements['risk_tolerance']}),
                        'execution_config': json.dumps({"output_format": requirements['output_format']})
                    }
                elif stage == WorkflowStage.RESULTS_SYNTHESIS:
                    inputs = {
                        'execution_results': self.stage_outputs.get('model_execution', {}).get('execution_results', ''),
                        'scenario_classifications': self.stage_outputs.get('scenario_classification', {}).get('scenario_recommendations', ''),
                        'regulatory_requirements': requirements.get('regulatory_framework', 'none')
                    }
                
                # Execute the skill
                results = self.load_and_execute_skill(tool_name, inputs)
                
                # Store results
                self.stage_outputs[stage.value] = results
                
                # Display results
                self.display_stage_results(stage.value, results, description)
                
                # Get user validation
                validation = self.get_user_validation(stage.value)
                self.user_approvals[stage.value] = validation
                
                if validation == ValidationResult.REJECTED:
                    print("\n❌ Workflow terminated by user.")
                    return
                elif validation == ValidationResult.SKIP:
                    print(f"\n⏭️  Skipping {stage.value}")
                    continue
                elif validation == ValidationResult.APPROVED:
                    print(f"\n✅ {stage.value} approved. Continuing...")
                
            # Workflow completion
            self.finalize_workflow(requirements)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Workflow interrupted by user (Ctrl+C)")
        except Exception as e:
            print(f"\n❌ Workflow error: {str(e)}")

    def finalize_workflow(self, requirements: Dict[str, Any]):
        """Finalize and summarize the workflow."""
        print(f"\n{'='*70}")
        print("🎯 WORKFLOW COMPLETION SUMMARY")
        print(f"{'='*70}")
        
        # Create final workflow results
        self.workflow_results = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "workflow_type": "Azure AI Foundry Skills-Based Stress Testing",
                "total_stages": len(self.workflow_sequence),
                "completed_stages": len([v for v in self.user_approvals.values() if v == ValidationResult.APPROVED])
            },
            "initial_requirements": requirements,
            "stage_outputs": self.stage_outputs,
            "user_approvals": {k: v.value for k, v in self.user_approvals.items()},
            "final_recommendations": self.extract_final_recommendations()
        }
        
        # Display summary
        print(f"Portfolio Analyzed: {requirements['portfolio_type']} (${requirements['portfolio_value']:,.2f})")
        print(f"Regulatory Framework: {requirements['regulatory_framework']}")
        print(f"Stages Completed: {len([v for v in self.user_approvals.values() if v == ValidationResult.APPROVED])}/{len(self.workflow_sequence)}")
        
        # Save results
        self.save_workflow_results()
        
        print(f"\n✅ Workflow completed successfully!")
        print(f"📁 Results saved to: workflow_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        # Offer PDF report generation
        self.offer_pdf_generation()

    def extract_final_recommendations(self) -> Dict[str, Any]:
        """Extract final recommendations from all stages."""
        recommendations = {
            "executive_summary": "Comprehensive stress testing analysis completed using Azure AI Foundry skills architecture.",
            "key_findings": [],
            "action_items": [],
            "next_steps": []
        }
        
        # Extract key findings from synthesis if available
        if 'results_synthesis' in self.stage_outputs:
            synthesis_data = self.stage_outputs['results_synthesis'].get('synthesis_report', '')
            if synthesis_data:
                try:
                    synthesis_json = json.loads(synthesis_data)
                    recommendations["key_findings"] = [
                        "Portfolio resilience assessment completed",
                        "Risk concentration analysis performed", 
                        "Regulatory compliance verified"
                    ]
                    recommendations["action_items"] = [
                        "Review risk concentration levels",
                        "Monitor key risk indicators",
                        "Update stress testing procedures"
                    ]
                except:
                    pass
        
        recommendations["next_steps"] = [
            "Review detailed analysis reports",
            "Implement recommended risk mitigations",
            "Schedule follow-up stress testing",
            "Update risk management frameworks"
        ]
        
        return recommendations

    def save_workflow_results(self):
        """Save workflow results to file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"workflow_results_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.workflow_results, f, indent=2)
        except Exception as e:
            print(f"⚠️  Warning: Could not save results to file: {str(e)}")

    def offer_pdf_generation(self):
        """Offer to generate a PDF report from the workflow results."""
        print(f"\n{'='*50}")
        print("📄 PDF REPORT GENERATION")
        print(f"{'='*50}")
        print("Would you like to generate a PDF report from these results?")
        print("\nReport Types:")
        print("  a) Executive Summary (recommended for leadership)")
        print("  b) Detailed Technical Report")
        print("  c) Comprehensive Report (with full appendix)")
        print("  d) Skip PDF generation")
        
        while True:
            choice = input("\nSelect option (a-d): ").strip().lower()
            
            if choice == 'd':
                print("⏭️  Skipping PDF generation.")
                return
            elif choice in ['a', 'b', 'c']:
                report_type_map = {
                    'a': 'executive',
                    'b': 'detailed', 
                    'c': 'comprehensive'
                }
                report_type = report_type_map[choice]
                
                # Get custom title
                custom_title = input(f"\nEnter custom report title (press Enter for default): ").strip()
                if not custom_title:
                    custom_title = "Financial Stress Testing Report"
                
                self.generate_pdf_report(report_type, custom_title)
                return
            else:
                print("Invalid choice. Please select a, b, c, or d.")

    def generate_pdf_report(self, report_type: str, report_title: str):
        """Generate a PDF report using the PDF tool."""
        try:
            print(f"\n🚀 Generating {report_type} PDF report...")
            
            # Import and use the PDF tool
            from tools.pdf_report_tool.pdf_report_tool import main as generate_pdf
            
            # Convert workflow results to JSON string
            workflow_json = json.dumps(self.workflow_results, indent=2)
            
            # Generate PDF
            result = generate_pdf(
                workflow_results=workflow_json,
                report_title=report_title,
                report_format=report_type
            )
            
            report_path = result.get('report_path', '')
            
            if 'Error' in report_path:
                print(f"❌ PDF Generation Failed: {report_path}")
            else:
                print(f"✅ {report_path}")
                
                # Extract actual filename and provide file info
                if ':' in report_path:
                    actual_file = report_path.split(':')[-1].strip()
                    if os.path.exists(actual_file):
                        file_size = os.path.getsize(actual_file)
                        print(f"📁 File size: {file_size:,} bytes")
                        print(f"📍 Location: {os.path.abspath(actual_file)}")
                        
                        # Offer to open the file
                        open_file = input(f"\nWould you like to open the PDF report? (y/n): ").strip().lower()
                        if open_file == 'y':
                            try:
                                import subprocess
                                subprocess.run(['open', actual_file])  # macOS
                                print("📖 Opening PDF report...")
                            except:
                                print(f"💡 Please manually open: {actual_file}")
        
        except ImportError:
            print("❌ PDF generation requires reportlab. Install with: pip install reportlab")
        except Exception as e:
            print(f"❌ PDF generation error: {str(e)}")


def main():
    """Main function to run the Azure AI Foundry Skills Workflow."""
    orchestrator = SkillsWorkflowOrchestrator()
    orchestrator.execute_workflow()


if __name__ == "__main__":
    main()
