import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class WorkflowStage(Enum):
    """Enumeration of workflow stages"""
    INITIAL = "initial"
    REQUIREMENTS_ANALYSIS = "requirements_analysis"
    SCENARIO_CLASSIFICATION = "scenario_classification"
    ANALYSIS_PLANNING = "analysis_planning"
    DOMAIN_ANALYSIS = "domain_analysis"
    REGULATORY_CONTEXT = "regulatory_context"
    REPORT_SYNTHESIS = "report_synthesis"
    COMPLETED = "completed"

@dataclass
class AgentOutput:
    """Standard structure for agent outputs"""
    agent_name: str
    stage: WorkflowStage
    output: Dict[str, Any]
    timestamp: str
    user_validated: bool = False
    user_feedback: Optional[str] = None

class WorkflowState:
    """Manages the state of the multi-agent workflow"""
    
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or self._generate_session_id()
        self.state_file = f"workflow_state_{self.session_id}.json"
        self.current_stage = WorkflowStage.INITIAL
        self.agent_outputs: Dict[str, AgentOutput] = {}
        self.user_input = ""
        self.workflow_metadata = {
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "session_id": self.session_id
        }
        
        # Load existing state if file exists
        self._load_state()
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID"""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _load_state(self):
        """Load workflow state from file if it exists"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                
                self.current_stage = WorkflowStage(data.get('current_stage', 'initial'))
                self.user_input = data.get('user_input', '')
                self.workflow_metadata = data.get('workflow_metadata', self.workflow_metadata)
                
                # Reconstruct agent outputs
                for stage_name, output_data in data.get('agent_outputs', {}).items():
                    self.agent_outputs[stage_name] = AgentOutput(
                        agent_name=output_data['agent_name'],
                        stage=WorkflowStage(output_data['stage']),
                        output=output_data['output'],
                        timestamp=output_data['timestamp'],
                        user_validated=output_data.get('user_validated', False),
                        user_feedback=output_data.get('user_feedback')
                    )
                
                print(f"✅ Loaded existing workflow state: {self.session_id}")
                
            except Exception as e:
                print(f"⚠️ Could not load state file: {e}")
                # Continue with fresh state
    
    def save_state(self):
        """Save current workflow state to file"""
        try:
            # Convert agent outputs to serializable format
            serializable_outputs = {}
            for stage_name, agent_output in self.agent_outputs.items():
                serializable_outputs[stage_name] = {
                    'agent_name': agent_output.agent_name,
                    'stage': agent_output.stage.value,
                    'output': agent_output.output,
                    'timestamp': agent_output.timestamp,
                    'user_validated': agent_output.user_validated,
                    'user_feedback': agent_output.user_feedback
                }
            
            state_data = {
                'session_id': self.session_id,
                'current_stage': self.current_stage.value,
                'user_input': self.user_input,
                'agent_outputs': serializable_outputs,
                'workflow_metadata': self.workflow_metadata
            }
            
            # Update last_updated timestamp
            state_data['workflow_metadata']['last_updated'] = datetime.now().isoformat()
            
            with open(self.state_file, 'w') as f:
                json.dump(state_data, f, indent=2)
                
            print(f"💾 Workflow state saved")
            
        except Exception as e:
            print(f"❌ Error saving state: {e}")
    
    def set_user_input(self, user_input: str):
        """Set the initial user input"""
        self.user_input = user_input
        self.save_state()
    
    def add_agent_output(self, agent_output: AgentOutput):
        """Add output from an agent"""
        stage_key = agent_output.stage.value
        self.agent_outputs[stage_key] = agent_output
        self.current_stage = agent_output.stage
        self.save_state()
    
    def validate_agent_output(self, stage: WorkflowStage, user_feedback: Optional[str] = None):
        """Mark an agent output as validated by user"""
        stage_key = stage.value
        if stage_key in self.agent_outputs:
            self.agent_outputs[stage_key].user_validated = True
            self.agent_outputs[stage_key].user_feedback = user_feedback
            self.save_state()
            return True
        return False
    
    def get_agent_output(self, stage: WorkflowStage) -> Optional[AgentOutput]:
        """Get output from a specific agent/stage"""
        stage_key = stage.value
        return self.agent_outputs.get(stage_key)
    
    def get_all_validated_outputs(self) -> Dict[str, AgentOutput]:
        """Get all user-validated agent outputs"""
        return {
            stage: output for stage, output in self.agent_outputs.items()
            if output.user_validated
        }
    
    def is_stage_completed(self, stage: WorkflowStage) -> bool:
        """Check if a stage has been completed and validated"""
        stage_key = stage.value
        return (stage_key in self.agent_outputs and 
                self.agent_outputs[stage_key].user_validated)
    
    def get_next_stage(self) -> Optional[WorkflowStage]:
        """Get the next stage in the workflow"""
        stages = list(WorkflowStage)
        current_index = stages.index(self.current_stage)
        
        if current_index < len(stages) - 1:
            return stages[current_index + 1]
        return None
    
    def get_workflow_summary(self) -> Dict[str, Any]:
        """Get a summary of the current workflow state"""
        completed_stages = [
            stage for stage, output in self.agent_outputs.items()
            if output.user_validated
        ]
        
        return {
            'session_id': self.session_id,
            'current_stage': self.current_stage.value,
            'completed_stages': completed_stages,
            'total_stages': len(WorkflowStage) - 2,  # Exclude INITIAL and COMPLETED
            'progress_percentage': len(completed_stages) / (len(WorkflowStage) - 2) * 100,
            'user_input': self.user_input[:100] + "..." if len(self.user_input) > 100 else self.user_input,
            'created_at': self.workflow_metadata['created_at'],
            'last_updated': self.workflow_metadata['last_updated']
        }
    
    def cleanup_state_file(self):
        """Remove the state file (typically called when workflow is completed)"""
        try:
            if os.path.exists(self.state_file):
                os.remove(self.state_file)
                print(f"🗑️ Cleaned up state file: {self.state_file}")
        except Exception as e:
            print(f"⚠️ Could not remove state file: {e}")
    
    def reset_workflow(self):
        """Reset the workflow to initial state"""
        self.current_stage = WorkflowStage.INITIAL
        self.agent_outputs = {}
        self.user_input = ""
        self.workflow_metadata['last_updated'] = datetime.now().isoformat()
        self.save_state()
        print("🔄 Workflow reset to initial state")
