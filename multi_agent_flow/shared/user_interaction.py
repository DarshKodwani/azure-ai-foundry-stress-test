"""
User Interaction Module for Multi-Agent Financial Stress Test Workflow

This module provides utilities for handling user interactions, including:
- CLI prompts and validation
- User confirmation for agent outputs
- Input validation and error handling
- Progress display and feedback

Author: AI Assistant
Date: 2024
"""

import sys
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
import json
from .state_manager import AgentOutput, WorkflowStage


class ValidationResult(Enum):
    """Enum for user validation results"""
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFY = "modify"
    SKIP = "skip"


class UserInteraction:
    """
    Handles all user interactions for the multi-agent workflow.
    
    This class provides methods for:
    - Displaying agent outputs for review
    - Getting user validation/approval
    - Handling user input with validation
    - Providing workflow progress feedback
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize the UserInteraction handler.
        
        Args:
            verbose: Whether to display detailed information
        """
        self.verbose = verbose
        self.colors = {
            'header': '\033[95m',
            'blue': '\033[94m',
            'cyan': '\033[96m',
            'green': '\033[92m',
            'warning': '\033[93m',
            'fail': '\033[91m',
            'end': '\033[0m',
            'bold': '\033[1m',
            'underline': '\033[4m'
        }
    
    def _colorize(self, text: str, color: str) -> str:
        """Apply color formatting to text if terminal supports it."""
        if sys.stdout.isatty():
            return f"{self.colors.get(color, '')}{text}{self.colors['end']}"
        return text
    
    def display_banner(self, title: str, subtitle: str = None) -> None:
        """Display a formatted banner for workflow sections."""
        print("\n" + "=" * 80)
        print(self._colorize(f"  {title}", 'header'))
        if subtitle:
            print(self._colorize(f"  {subtitle}", 'cyan'))
        print("=" * 80 + "\n")
    
    def display_stage_header(self, stage: WorkflowStage, description: str = None) -> None:
        """Display header for a workflow stage."""
        stage_title = stage.value.replace('_', ' ').title()
        print(f"\n{self._colorize('🔄 STAGE:', 'bold')} {self._colorize(stage_title, 'blue')}")
        if description:
            print(f"{self._colorize('📋 Description:', 'bold')} {description}")
        print("-" * 60)
    
    def display_agent_output(self, output: AgentOutput) -> None:
        """
        Display an agent's output in a formatted manner.
        
        Args:
            output: The AgentOutput object to display
        """
        print(f"\n{self._colorize('🤖 AGENT OUTPUT:', 'bold')} {self._colorize(output.agent_name, 'green')}")
        print(f"{self._colorize('⏰ Timestamp:', 'bold')} {output.timestamp}")
        print(f"{self._colorize('📊 Stage:', 'bold')} {output.stage.value}")
        
        if output.summary:
            print(f"\n{self._colorize('📝 Summary:', 'bold')}")
            print(f"  {output.summary}")
        
        if output.key_findings:
            print(f"\n{self._colorize('🔍 Key Findings:', 'bold')}")
            for i, finding in enumerate(output.key_findings, 1):
                print(f"  {i}. {finding}")
        
        if output.recommendations:
            print(f"\n{self._colorize('💡 Recommendations:', 'bold')}")
            for i, rec in enumerate(output.recommendations, 1):
                print(f"  {i}. {rec}")
        
        if output.data and self.verbose:
            print(f"\n{self._colorize('📈 Data Summary:', 'bold')}")
            if isinstance(output.data, dict):
                for key, value in output.data.items():
                    if isinstance(value, (list, dict)):
                        print(f"  {key}: {type(value).__name__} with {len(value)} items")
                    else:
                        print(f"  {key}: {value}")
            else:
                print(f"  Data type: {type(output.data).__name__}")
        
        if output.errors:
            print(f"\n{self._colorize('⚠️ Errors/Warnings:', 'warning')}")
            for error in output.errors:
                print(f"  • {error}")
        
        print("-" * 60)
    
    def get_user_validation(self, output: AgentOutput) -> ValidationResult:
        """
        Get user validation for an agent's output.
        
        Args:
            output: The AgentOutput to validate
            
        Returns:
            ValidationResult indicating user's decision
        """
        print(f"\n{self._colorize('👤 USER VALIDATION REQUIRED', 'bold')}")
        print("Please review the agent output above and choose an action:")
        print(f"  {self._colorize('1.', 'green')} Approve - Continue to next stage")
        print(f"  {self._colorize('2.', 'warning')} Reject - Stop workflow")
        print(f"  {self._colorize('3.', 'cyan')} Modify - Request changes")
        print(f"  {self._colorize('4.', 'blue')} Skip - Skip this stage")
        
        while True:
            try:
                choice = input(f"\n{self._colorize('Your choice (1-4):', 'bold')} ").strip()
                
                if choice == '1':
                    return ValidationResult.APPROVED
                elif choice == '2':
                    return ValidationResult.REJECTED
                elif choice == '3':
                    return ValidationResult.MODIFY
                elif choice == '4':
                    return ValidationResult.SKIP
                else:
                    print(f"{self._colorize('Invalid choice. Please enter 1, 2, 3, or 4.', 'fail')}")
                    
            except KeyboardInterrupt:
                print(f"\n{self._colorize('Workflow interrupted by user.', 'warning')}")
                return ValidationResult.REJECTED
            except EOFError:
                print(f"\n{self._colorize('End of input reached. Rejecting by default.', 'warning')}")
                return ValidationResult.REJECTED
    
    def get_modification_feedback(self) -> str:
        """
        Get feedback from user about what modifications are needed.
        
        Returns:
            User's modification feedback
        """
        print(f"\n{self._colorize('📝 Please provide feedback for modifications:', 'bold')}")
        print("(Enter your feedback below, press Enter twice to finish)")
        
        lines = []
        empty_lines = 0
        
        while empty_lines < 2:
            try:
                line = input()
                if line.strip():
                    lines.append(line)
                    empty_lines = 0
                else:
                    empty_lines += 1
                    if empty_lines == 1:
                        lines.append("")  # Add one empty line
                        
            except (KeyboardInterrupt, EOFError):
                break
        
        # Remove trailing empty lines
        while lines and not lines[-1].strip():
            lines.pop()
        
        return "\n".join(lines)
    
    def get_user_input(self, prompt: str, validator: Callable[[str], bool] = None, 
                      error_msg: str = "Invalid input. Please try again.") -> str:
        """
        Get validated user input.
        
        Args:
            prompt: The prompt to display to the user
            validator: Optional validation function
            error_msg: Error message for invalid input
            
        Returns:
            Validated user input
        """
        while True:
            try:
                user_input = input(f"{self._colorize(prompt, 'bold')} ").strip()
                
                if validator is None or validator(user_input):
                    return user_input
                else:
                    print(f"{self._colorize(error_msg, 'fail')}")
                    
            except (KeyboardInterrupt, EOFError):
                print(f"\n{self._colorize('Input cancelled by user.', 'warning')}")
                return ""
    
    def confirm_action(self, action: str) -> bool:
        """
        Get user confirmation for an action.
        
        Args:
            action: Description of the action to confirm
            
        Returns:
            True if user confirms, False otherwise
        """
        response = self.get_user_input(
            f"Confirm: {action} (y/n):",
            validator=lambda x: x.lower() in ['y', 'yes', 'n', 'no'],
            error_msg="Please enter 'y' or 'n'"
        )
        return response.lower() in ['y', 'yes']
    
    def display_progress(self, current_stage: WorkflowStage, 
                        completed_stages: List[WorkflowStage]) -> None:
        """
        Display workflow progress.
        
        Args:
            current_stage: The current workflow stage
            completed_stages: List of completed stages
        """
        all_stages = list(WorkflowStage)
        
        print(f"\n{self._colorize('📊 WORKFLOW PROGRESS', 'bold')}")
        print("-" * 40)
        
        for stage in all_stages:
            if stage in completed_stages:
                status = self._colorize("✅ COMPLETED", 'green')
            elif stage == current_stage:
                status = self._colorize("🔄 IN PROGRESS", 'cyan')
            else:
                status = self._colorize("⏳ PENDING", 'warning')
            
            stage_name = stage.value.replace('_', ' ').title()
            print(f"  {stage_name:<25} {status}")
        
        print("-" * 40)
    
    def display_summary(self, outputs: List[AgentOutput], 
                       total_time: float = None) -> None:
        """
        Display a summary of all agent outputs.
        
        Args:
            outputs: List of all AgentOutput objects
            total_time: Total workflow execution time in seconds
        """
        print(f"\n{self._colorize('📋 WORKFLOW SUMMARY', 'bold')}")
        print("=" * 60)
        
        if total_time:
            print(f"{self._colorize('⏱️ Total Execution Time:', 'bold')} {total_time:.2f} seconds")
        
        print(f"{self._colorize('🔢 Total Stages Completed:', 'bold')} {len(outputs)}")
        
        print(f"\n{self._colorize('📊 Stages Overview:', 'bold')}")
        for i, output in enumerate(outputs, 1):
            stage_name = output.stage.value.replace('_', ' ').title()
            status = self._colorize("✅", 'green') if not output.errors else self._colorize("⚠️", 'warning')
            print(f"  {i}. {status} {stage_name} ({output.agent_name})")
        
        # Show any errors across all stages
        all_errors = []
        for output in outputs:
            if output.errors:
                all_errors.extend([(output.stage, error) for error in output.errors])
        
        if all_errors:
            print(f"\n{self._colorize('⚠️ Issues Found:', 'warning')}")
            for stage, error in all_errors:
                print(f"  • {stage.value}: {error}")
        
        print("=" * 60)
    
    def display_error(self, error: str, stage: WorkflowStage = None) -> None:
        """Display an error message with formatting."""
        print(f"\n{self._colorize('❌ ERROR', 'fail')}")
        if stage:
            print(f"{self._colorize('Stage:', 'bold')} {stage.value}")
        print(f"{self._colorize('Message:', 'bold')} {error}")
        print()
    
    def display_warning(self, warning: str) -> None:
        """Display a warning message with formatting."""
        print(f"{self._colorize('⚠️ WARNING:', 'warning')} {warning}")
    
    def display_info(self, info: str) -> None:
        """Display an info message with formatting."""
        print(f"{self._colorize('ℹ️ INFO:', 'cyan')} {info}")
    
    def display_success(self, message: str) -> None:
        """Display a success message with formatting."""
        print(f"{self._colorize('✅ SUCCESS:', 'green')} {message}")


def create_user_interaction(verbose: bool = True) -> UserInteraction:
    """
    Factory function to create a UserInteraction instance.
    
    Args:
        verbose: Whether to enable verbose output
        
    Returns:
        UserInteraction instance
    """
    return UserInteraction(verbose=verbose)
