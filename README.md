# Agentic Stress Test Summarizer (Azure AI Foundry)

This project implements a financial stress test summarization pipeline using Azure AI Foundry, Azure OpenAI, and Python.

## Goal

Build an agent that:
1. Takes a BoE-style stress scenario as input
2. Summarizes it using Azure OpenAI
3. Returns a structured output

## Project Structure

```
foundary_stresstest/
├── tools/
│   └── summarize_tool/
│       ├── summarize_tool.yaml
│       └── summarize_tool.py
├── skills/
│   └── summarize_scenario/
│       └── summarize_stress_scenario.yaml
├── agents/
│   └── stress_agent.yaml
├── .env.example
├── requirements.txt
└── run_agent.py
```

## Setup

### Prerequisites
- Python 3.9+
- Azure OpenAI resource + deployment
- Azure AI Foundry project

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your Azure credentials
```

3. Set environment variables:
```bash
export OPENAI_API_KEY=your-api-key
export OPENAI_API_BASE=https://your-endpoint.openai.azure.com
export DEPLOYMENT_NAME=gpt-4o
export PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/project
```

## Usage

### Run the Complete Pipeline
```bash
./run_pipeline.sh
```
This will:
1. Run the stress test analysis
2. Generate a professional PDF report
3. Open the reports folder (on macOS)

### Run Components Individually
```bash
# Run just the analysis
python run_agent.py

# Generate PDF from previous analysis
python generate_pdf_report.py
```

## Output

The pipeline generates:
- Console output with the AI analysis
- Professional PDF report in the `reports/` directory
- Structured, formatted report suitable for regulatory review

## Author

Built by Darsh Kodwani
