"""
Shared Utilities Package for Multi-Agent Financial Stress Test Workflow

This package contains shared utilities and common functionality used across
all agents in the workflow:
- state_manager: Workflow state management and agent output standardization
- user_interaction: CLI interface and user validation utilities
"""

from .state_manager import (
    WorkflowStage,
    AgentOutput, 
    WorkflowState
)
from .user_interaction import (
    ValidationResult,
    UserInteraction,
    create_user_interaction
)

__all__ = [
    'WorkflowStage',
    'AgentOutput',
    'WorkflowState', 
    'ValidationResult',
    'UserInteraction',
    'create_user_interaction'
]
