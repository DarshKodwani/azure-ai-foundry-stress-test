# Multi-Agent Stress Testing Workflow

## 🎯 Overview

This document describes the enhanced multi-agent workflow for comprehensive stress testing analysis. The system breaks down complex stress test analysis into manageable, validated steps with human oversight at each stage.

## 🔄 Workflow Architecture

The workflow consists of 6 specialized agents, each with a specific role and validation checkpoint:

```
User Request → Agent 1 → Validation → Agent 2 → Validation → ... → Final Report
```

## 🤖 Agent Breakdown

### **Agent 1: Requirements Analyst Agent**
**Purpose**: Understand and clarify the stress testing requirements

**Input**: User's initial request (e.g., "Analyze BoE 2022 stress test")

**Tasks**: 
- Parse the request to identify: stress test type, jurisdiction, scenario details, analysis depth
- Ask clarifying questions: "Are you looking for regulatory impact? Capital adequacy? Specific business lines?"
- Determine output format preferences
- Identify target audience and use case

**Output**: Structured requirements document

**User Validation**: "Is this understanding correct? Any additional requirements?"

---

### **Agent 2: Scenario Classification Agent**
**Purpose**: Categorize and contextualize the stress scenario

**Input**: Validated requirements + raw scenario text

**Tasks**:
- Identify stress test framework (BoE, Fed, EBA, CCAR, etc.)
- Classify scenario type (baseline, adverse, severely adverse)
- Extract key macroeconomic variables and their trajectories
- Identify relevant time horizons and geographical scope
- Map to regulatory framework requirements

**Output**: Classified scenario with metadata

**User Validation**: "Does this classification look accurate? Should we focus on specific aspects?"

---

### **Agent 3: Analysis Planning Agent**
**Purpose**: Create a comprehensive analysis roadmap

**Input**: Validated requirements + classified scenario

**Tasks**:
- Determine analysis methodology (quantitative vs qualitative)
- Identify key risk areas to focus on (credit, market, operational, liquidity)
- Plan analysis sections (executive summary, methodology, findings, implications)
- Suggest comparative analysis opportunities (vs previous tests, peer jurisdictions)
- Define success metrics and deliverables

**Output**: Detailed analysis plan with methodology

**User Validation**: "Does this analysis approach meet your needs? Any adjustments?"

---

### **Agent 4: Domain Expert Agent**
**Purpose**: Perform deep technical analysis

**Input**: Validated analysis plan + scenario data

**Tasks**:
- Conduct detailed stress test analysis
- Calculate potential impacts on different metrics (capital ratios, provisions, etc.)
- Identify interconnected risks and second-order effects
- Generate technical findings and insights
- Perform quantitative assessments where applicable

**Output**: Comprehensive technical analysis

**User Validation**: "Are these findings aligned with your expectations? Need deeper dive anywhere?"

---

### **Agent 5: Regulatory Context Agent**
**Purpose**: Add regulatory and compliance perspective

**Input**: Technical analysis + original requirements

**Tasks**:
- Map findings to relevant regulatory frameworks
- Identify compliance implications
- Suggest risk management considerations
- Highlight supervisory expectations and guidance
- Assess regulatory impact and reporting requirements

**Output**: Regulatory-contextualized analysis

**User Validation**: "Is the regulatory context appropriate for your use case?"

---

### **Agent 6: Report Synthesis Agent**
**Purpose**: Create professional, audience-appropriate output

**Input**: All validated analyses + user preferences

**Tasks**:
- Structure findings for target audience (executives, risk managers, regulators)
- Create executive summary with key takeaways
- Format technical details appropriately
- Add relevant charts, tables, and visualizations
- Ensure consistent messaging and professional presentation

**Output**: Publication-ready report

**User Validation**: "Does this report format and content meet your needs?"

## 🔄 Interactive Flow Benefits

### **Quality Control**
User validation at each step prevents compounding errors and ensures accuracy throughout the analysis pipeline.

### **Customization**
Analysis can be tailored based on user feedback, allowing for specific focus areas and methodological preferences.

### **Transparency**
User understands how conclusions were reached, building confidence in the analysis and recommendations.

### **Flexibility**
Can pivot or deep-dive based on intermediate findings, adapting to emerging insights during the analysis.

### **Learning**
System learns from user corrections and preferences, improving future analyses.

## 🎯 Key Decision Points for Users

### **Depth vs Breadth**
"Focus on specific risk types or comprehensive overview?"

### **Audience**
"Who will read this report? Technical team or executives?"

### **Comparisons**
"Include historical comparisons or peer analysis?"

### **Methodology**
"Quantitative modeling or qualitative assessment?"

### **Output Format**
"Executive brief, technical report, or presentation?"

## 🚀 Implementation Architecture

The workflow is implemented using:
- **Individual Agent Scripts**: Each agent has its own Python module
- **State Management**: Shared state file tracks progress and user validations
- **Interactive CLI**: Command-line interface for user validation at each step
- **Azure AI Integration**: Leverages Azure AI Foundry for agent capabilities
- **PDF Generation**: Professional report output using ReportLab

## 📁 File Structure

```
multi_agent_flow/
├── agents/
│   ├── requirements_analyst.py
│   ├── scenario_classifier.py
│   ├── analysis_planner.py
│   ├── domain_expert.py
│   ├── regulatory_context.py
│   └── report_synthesizer.py
├── shared/
│   ├── state_manager.py
│   └── user_interaction.py
├── config/
│   └── agent_configs.yaml
└── run_multi_agent_flow.py
```

## 🎮 Usage

```bash
# Run the interactive multi-agent workflow
python run_multi_agent_flow.py

# Or run individual agents
python agents/requirements_analyst.py
```

Each step will present findings and ask for user validation before proceeding to the next agent in the workflow.

---

**Note**: This multi-agent approach transforms stress testing from a single-shot analysis into a collaborative, iterative process that ensures comprehensive, accurate, and user-validated results.
