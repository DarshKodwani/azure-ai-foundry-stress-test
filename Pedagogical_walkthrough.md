# Pedagogical Walkthrough: Azure AI Foundry Stress Test Summarizer

## Table of Contents
1. [Overview & Architecture](#overview--architecture)
2. [Azure AI Foundry Platform](#azure-ai-foundry-platform)
3. [Project Structure Deep Dive](#project-structure-deep-dive)
4. [Configuration Files](#configuration-files)
5. [Core Components](#core-components)
6. [Data Flow & Execution](#data-flow--execution)
7. [Azure Integration Details](#azure-integration-details)
8. [Best Practices & Design Patterns](#best-practices--design-patterns)
9. [Extension Opportunities](#extension-opportunities)

---

## Overview & Architecture

This project demonstrates a **multi-agent AI system** built on Azure AI Foundry, designed specifically for financial stress testing scenarios. It follows a **modular, declarative architecture** where business logic is separated into discrete, reusable components.

### Key Architectural Principles:
- **Agent-Oriented Design**: Uses the agent pattern where specialized components handle specific tasks
- **Declarative Configuration**: YAML files define capabilities without hardcoding logic
- **Separation of Concerns**: Tools, skills, and agents have distinct responsibilities
- **Cloud-Native**: Leverages Azure's managed AI services for scalability and reliability

---

## Azure AI Foundry Platform

### What is Azure AI Foundry?
Azure AI Foundry is Microsoft's comprehensive platform for building, deploying, and managing AI applications. It provides:

1. **Unified Development Environment**: Single platform for AI model deployment, management, and orchestration
2. **Multi-Model Support**: Access to OpenAI models, Microsoft models, and third-party models
3. **Agent Framework**: Built-in support for creating intelligent agents with tools and skills
4. **Enterprise Security**: Role-based access control, data protection, and compliance features
5. **Integrated Services**: Seamless connection to Azure OpenAI, Azure Search, and other Azure services

### Key Components We Use:
- **Azure OpenAI Service**: Provides the LLM capabilities (GPT-4o in our case)
- **AI Projects**: Container for organizing agents, tools, and configurations
- **Agent Runtime**: Execution environment for our intelligent agents
- **Connection Management**: Secure credential and endpoint management

---

## Project Structure Deep Dive

```
foundary_stresstest/
├── tools/                  # Atomic AI capabilities
├── skills/                 # Business logic combinations
├── agents/                 # High-level orchestrators
├── configuration files     # Environment and setup
└── application entry       # Main execution point
```

### Design Philosophy:
This structure follows the **"Tools → Skills → Agents"** hierarchy:
- **Tools**: Perform single, specific AI operations
- **Skills**: Combine tools to solve business problems
- **Agents**: Orchestrate skills to complete complex workflows

---

## Configuration Files

### `.env` & `.env.example`
**Purpose**: Environment variable management for secure credential storage.

```bash
# Azure OpenAI Configuration
OPENAI_API_KEY=your-api-key-here           # Authentication token
OPENAI_API_BASE=https://your-endpoint...   # Service endpoint
OPENAI_API_VERSION=2024-10-21              # API version for compatibility
DEPLOYMENT_NAME=gpt-4o                     # Specific model deployment

# Azure AI Foundry Project Configuration
PROJECT_ENDPOINT=https://your-project...   # Project-specific endpoint
```

**Why This Matters**:
- **Security**: Keeps credentials out of source code
- **Flexibility**: Easy environment switching (dev/staging/prod)
- **Azure Integration**: Follows Azure's authentication patterns

### `requirements.txt`
**Purpose**: Python dependency specification for consistent environments.

```
openai                  # OpenAI Python SDK for LLM interactions
azure-ai-projects       # Azure AI Foundry project management
azure-identity          # Azure authentication handling
python-dotenv          # Environment variable loading
```

**Dependency Analysis**:
- `openai`: Provides the `AzureOpenAI` client for model interactions
- `azure-ai-projects`: Core Azure AI Foundry functionality
- `azure-identity`: Handles Azure AD authentication seamlessly
- `python-dotenv`: Loads environment variables from `.env` files

### `.gitignore`
**Purpose**: Prevents sensitive files from being committed to version control.

Key exclusions:
- `.env` (contains secrets)
- `__pycache__/` (Python bytecode)
- `.venv/` (virtual environment)
- IDE files (`.vscode/`, `.idea/`)

---

## Core Components

### 1. Tools Layer: `tools/summarize_tool/`

#### `summarize_tool.yaml`
**Purpose**: Declarative tool specification following Azure AI Foundry's tool schema.

```yaml
name: summarize_tool
type: python                    # Execution environment
description: Use Azure OpenAI to summarize financial stress scenarios
entry_point: summarize_tool.py  # Implementation file
inputs:
  - name: scenario_text         # Input schema definition
    type: string
outputs:
  - name: summary              # Output schema definition
    type: string
```

**Educational Value**:
- **Schema-Driven Development**: Defines interfaces before implementation
- **Type Safety**: Explicit input/output types prevent runtime errors
- **Documentation**: Description serves as inline documentation
- **Modularity**: Can be reused across different skills and agents

#### `summarize_tool.py`
**Purpose**: The actual implementation of the summarization logic.

```python
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

def main(scenario_text: str) -> dict:
    try:
        client = AzureOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            api_version=os.getenv("OPENAI_API_VERSION", "2024-10-21"),
            azure_endpoint=os.getenv("OPENAI_API_BASE")
        )

        response = client.chat.completions.create(
            model=os.getenv("DEPLOYMENT_NAME", "gpt-4o"),
            messages=[
                {"role": "system", "content": "You are an expert financial analyst..."},
                {"role": "user", "content": f"Summarize this Bank of England stress scenario..."}
            ],
            max_tokens=500,
            temperature=0.3
        )

        return {"summary": response.choices[0].message.content}
    
    except Exception as e:
        return {"summary": f"Error: {str(e)}..."}
```

**Technical Deep Dive**:
- **Azure OpenAI Client**: Uses the official Azure-specific client
- **Environment-Driven Configuration**: All settings come from environment variables
- **Error Handling**: Graceful degradation with informative error messages
- **Prompt Engineering**: Specialized system prompt for financial analysis
- **Parameter Tuning**: `temperature=0.3` for consistent, focused outputs

### 2. Skills Layer: `skills/summarize_scenario/`

#### `summarize_stress_scenario.yaml`
**Purpose**: Combines tools into business-specific capabilities.

```yaml
name: summarize_stress_scenario
description: Summarize a given stress scenario using the summarize_tool
tool: summarize_tool              # References the tool by name
inputs:
  - name: scenario_text
    type: string
prompt_template: |               # Jinja2 template for dynamic prompts
  Summarize the following financial stress test scenario:
  ---
  {{scenario_text}}
outputs:
  - name: summary
    type: string
```

**Educational Insights**:
- **Business Logic Layer**: Bridges low-level tools with high-level business needs
- **Template System**: Uses Jinja2 for dynamic prompt generation
- **Composition**: Shows how tools can be composed into more complex operations
- **Domain Specificity**: Tailored for financial stress testing use cases

### 3. Agents Layer: `agents/stress_agent.yaml`

#### `stress_agent.yaml`
**Purpose**: High-level orchestrator that can use multiple skills to complete complex tasks.

```yaml
name: stress_agent
description: Agent that summarizes financial stress test scenarios
skills:
  - summarize_stress_scenario     # List of available skills
memory:
  type: none                     # Memory configuration
entry_skill: summarize_stress_scenario  # Default skill to execute
```

**Agent Architecture Concepts**:
- **Skill Orchestration**: Agents can combine multiple skills
- **Memory Management**: Configurable memory for conversation context
- **Entry Points**: Define default behavior for agent invocation
- **Extensibility**: Easy to add new skills to expand capabilities

---

## Data Flow & Execution

### 1. Application Startup (`run_agent.py`)
```python
# 1. Load environment configuration
load_dotenv()

# 2. Initialize Azure AI Projects client
project_client = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=os.environ["PROJECT_ENDPOINT"],
)

# 3. Import and execute tool directly
from tools.summarize_tool.summarize_tool import main as summarize_tool
```

### 2. Tool Execution Flow
1. **Input Processing**: Receives stress scenario text
2. **Client Initialization**: Creates Azure OpenAI client with credentials
3. **Prompt Construction**: Builds system and user messages
4. **API Call**: Sends request to Azure OpenAI service
5. **Response Processing**: Extracts and formats the summary
6. **Error Handling**: Catches and reports any failures

### 3. Data Transformation Pipeline
```
Raw Scenario Text → 
Structured Prompt → 
Azure OpenAI API → 
AI-Generated Summary → 
Formatted Output
```

---

## Azure Integration Details

### Authentication Flow
1. **Environment Variables**: Primary authentication method using API keys
2. **DefaultAzureCredential**: Fallback to Azure AD authentication
3. **Project Endpoint**: Specific to your Azure AI Foundry project

### Service Integration Points
- **Azure OpenAI**: Core LLM functionality
- **Azure AI Projects**: Project management and orchestration
- **Azure Identity**: Authentication and authorization
- **Azure Monitor**: (Future) Logging and telemetry

### API Versioning Strategy
- Uses `2024-10-21` API version for stability
- Environment variable allows easy version updates
- Maintains compatibility with Azure OpenAI service updates

---

## Best Practices & Design Patterns

### 1. Configuration Management
- **Externalized Configuration**: All settings in environment variables
- **Defaults**: Sensible fallbacks for optional settings
- **Security**: Credentials never hardcoded

### 2. Error Handling
- **Graceful Degradation**: Application continues with error messages
- **Informative Errors**: Clear guidance for troubleshooting
- **Exception Boundaries**: Contained error handling at each layer

### 3. Modularity
- **Single Responsibility**: Each component has one clear purpose
- **Loose Coupling**: Components interact through well-defined interfaces
- **High Cohesion**: Related functionality grouped together

### 4. Scalability Considerations
- **Stateless Design**: Tools and skills don't maintain state
- **Resource Management**: Proper client initialization and cleanup
- **Configuration-Driven**: Easy to modify behavior without code changes

---

## Extension Opportunities

### 1. Additional Tools
```yaml
# Example: Comparison Tool
name: compare_scenarios_tool
description: Compare multiple stress test scenarios
inputs:
  - name: scenario_a
    type: string
  - name: scenario_b
    type: string
outputs:
  - name: comparison_report
    type: string
```

### 2. Enhanced Skills
```yaml
# Example: Multi-Jurisdiction Skill
name: multi_jurisdiction_analysis
description: Analyze scenarios across BoE, Fed, and EBA frameworks
tools:
  - summarize_tool
  - compare_scenarios_tool
  - regulatory_mapping_tool
```

### 3. Advanced Agents
```yaml
# Example: Research Agent
name: stress_research_agent
description: Comprehensive stress test research and analysis
skills:
  - summarize_stress_scenario
  - multi_jurisdiction_analysis
  - historical_comparison
  - trend_analysis
memory:
  type: conversation    # Maintains context across interactions
```

### 4. Integration Enhancements
- **Database Integration**: Store and retrieve historical scenarios
- **API Endpoints**: Expose functionality as REST APIs
- **Batch Processing**: Handle multiple scenarios simultaneously
- **Visualization**: Generate charts and graphs from analysis
- **Reporting**: Create formatted reports in PDF/Word formats

### 5. Advanced AI Features
- **RAG (Retrieval-Augmented Generation)**: Incorporate regulatory documents
- **Fine-tuning**: Customize models for specific financial use cases
- **Multi-modal**: Include charts, tables, and other financial data
- **Streaming**: Real-time response streaming for better UX

---

## Conclusion

This project demonstrates a production-ready implementation of Azure AI Foundry's agent architecture. It showcases:

- **Modern AI Development Patterns**: Tool/Skill/Agent hierarchy
- **Enterprise-Grade Integration**: Azure services and security
- **Maintainable Architecture**: Clear separation of concerns
- **Extensible Design**: Easy to add new capabilities

The pedagogical value lies in understanding how declarative AI systems can be built using cloud-native platforms, providing a foundation for more complex AI applications in enterprise environments.
