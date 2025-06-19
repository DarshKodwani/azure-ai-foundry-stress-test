#!/usr/bin/env python3
"""
Azure AI Foundry Skills-Based Stress Testing Workflow Runner

This script runs the interactive multi-skill stress testing workflow
using Azure AI Foundry skills architecture.
"""

import sys
import os

# Add the current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from azure_foundry_workflow import SkillsWorkflowOrchestrator
    
    def main():
        """Run the Azure AI Foundry Skills Workflow."""
        print("🚀 Starting Azure AI Foundry Skills-Based Stress Testing Workflow...")
        
        # Check environment setup
        if not os.path.exists('.env'):
            print("⚠️  Warning: .env file not found. Please ensure your Azure OpenAI credentials are configured.")
            print("   Required environment variables:")
            print("   - OPENAI_API_KEY")
            print("   - OPENAI_API_BASE") 
            print("   - OPENAI_API_VERSION")
            print("   - DEPLOYMENT_NAME")
            print()
        
        # Check if skills directory exists
        if not os.path.exists('skills'):
            print("❌ Error: 'skills' directory not found.")
            print("   Please ensure you're running this script from the correct directory.")
            return 1
        
        # Check if tools directory exists
        if not os.path.exists('tools'):
            print("❌ Error: 'tools' directory not found.")
            print("   Please ensure you're running this script from the correct directory.")
            return 1
        
        # Initialize and run the orchestrator
        orchestrator = SkillsWorkflowOrchestrator()
        orchestrator.execute_workflow()
        
        return 0
        
except ImportError as e:
    print(f"❌ Import Error: {str(e)}")
    print("   Please ensure all required dependencies are installed:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected Error: {str(e)}")
    sys.exit(1)

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
