# Azure AI Foundry Financial Stress Testing Workflow

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Azure AI Foundry](https://img.shields.io/badge/Azure_AI-Foundry-0078d4.svg)](https://azure.microsoft.com/en-us/products/ai-foundry/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready, interactive financial stress testing workflow built with **Azure AI Foundry skills architecture**. Features LLM-driven scenario generation, comprehensive risk analysis, and professional PDF reporting.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Azure OpenAI API access
- Basic understanding of financial stress testing

### Installation
1. **Clone and install dependencies:**
   ```bash
   git clone <repository-url>
   cd foundary_stresstest
   pip install -r requirements.txt
   ```

2. **Configure Azure OpenAI:**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure OpenAI credentials
   ```

3. **Run the workflow:**
   ```bash
   python run_foundry_workflow.py
   ```

## 🏗️ Architecture

### Skills-Based Design (Azure AI Foundry)
- **Skills**: YAML definitions in `skills/` directory
- **Tools**: Python implementations in `tools/` directory  
- **Orchestrator**: Interactive workflow management with CLI validation

### Workflow Pipeline
1. **Requirements Analysis** - Portfolio and risk assessment
2. **Scenario Classification** - AI-generated stress test scenarios
3. **Model Execution** - Quantitative risk calculations
4. **Results Synthesis** - Comprehensive analysis and recommendations
5. **PDF Generation** - Professional reporting (optional)

## 📊 Features

✅ **Azure AI Foundry Native** - Pure skills-based architecture  
✅ **Interactive CLI** - User validation at each stage  
✅ **LLM-Driven Scenarios** - No hardcoded parameters  
✅ **Professional PDFs** - Executive, detailed, and comprehensive reports  
✅ **Regulatory Compliance** - Basel III, Solvency II, CCAR support  
✅ **Production Ready** - Error handling, logging, and validation  

## 🎯 Usage

### Interactive Workflow
```bash
python run_foundry_workflow.py
```
Follow CLI prompts for portfolio details, approve each stage, and optionally generate PDF reports.

### Standalone PDF Generation
```bash
# Interactive mode
python generate_report.py

# Direct mode
python generate_report.py workflow_results.json executive "Q4 2025 Stress Test"
```

### Report Types
- **Executive** (2-4 pages) - For board and senior management
- **Detailed** (5-10 pages) - For risk managers and analysts  
- **Comprehensive** (10+ pages) - For regulators and auditors

## 📁 Project Structure

```
foundary_stresstest/
├── skills/                    # Azure AI Foundry Skills
│   ├── requirements_analysis/
│   ├── scenario_classification/
│   ├── model_execution/
│   ├── results_synthesis/
│   └── report_generation/
├── tools/                     # Skill Tool Implementations
│   ├── requirements_analyst_tool/
│   ├── scenario_classifier_tool/
│   ├── model_execution_tool/
│   ├── results_synthesis_tool/
│   └── pdf_report_tool/
├── reports/                   # Generated PDF reports
├── azure_foundry_workflow.py # Main orchestrator
├── run_foundry_workflow.py   # Workflow launcher
├── generate_report.py        # PDF generator
├── requirements.txt          # Dependencies
├── .env.example             # Environment template
└── USAGE_GUIDE.md           # Detailed usage instructions
```

## ⚙️ Configuration

### Environment Variables (.env)
```bash
OPENAI_API_KEY=your_azure_openai_key
OPENAI_API_BASE=https://your-instance.openai.azure.com/
OPENAI_API_VERSION=2024-10-21
DEPLOYMENT_NAME=gpt-4o
```

### Portfolio Types Supported
- Equity Portfolio
- Fixed Income Portfolio
- Mixed Portfolio  
- Bank Portfolio
- Insurance Portfolio

### Regulatory Frameworks
- Basel III (Banking)
- Solvency II (Insurance)
- CCAR (US Stress Testing)
- Custom/None

## 🔧 Customization

### Adding New Skills
1. Create skill YAML: `skills/new_skill/new_skill.yaml`
2. Create tool: `tools/new_tool/new_tool.yaml` and `new_tool.py`
3. Add to workflow sequence in `azure_foundry_workflow.py`

### Modifying Existing Skills
- Edit YAML for skill definition changes
- Edit Python for implementation logic
- Skills are dynamically loaded by the orchestrator

## 📖 Documentation

- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Comprehensive usage instructions
- **[.env.example](.env.example)** - Environment configuration template
- **Skills YAML files** - Individual skill documentation

## 🚨 Troubleshooting

### Common Issues

**Azure OpenAI Errors**
- Verify `.env` configuration
- Check API quotas and rate limits
- Ensure correct deployment name

**PDF Generation Issues**
```bash
pip install reportlab
```

**Import Errors**
```bash
pip install -r requirements.txt
```

**File Not Found**
- Ensure running from project root directory
- Check file paths and permissions

## 🔮 Production Deployment

### Azure Deployment Options
- **Azure Container Apps** - Serverless containers
- **Azure Functions** - Event-driven execution  
- **Azure App Service** - Web application hosting
- **Azure Batch** - Large-scale parallel processing

### Security Considerations
- Store API keys in Azure Key Vault
- Use Managed Identity for authentication
- Enable logging and monitoring
- Implement rate limiting and error handling

## 📈 Performance

### Optimization Tips
- Cache LLM responses for repeated scenarios
- Implement parallel skill execution where possible
- Use streaming for large PDF reports
- Monitor Azure OpenAI token usage

### Scalability
- Skills are stateless and horizontally scalable
- JSON output enables integration with external systems
- Workflow results can be stored in databases
- PDF generation can be offloaded to separate services

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-skill`)
3. Follow Azure AI Foundry skills pattern
4. Add tests for new functionality
5. Update documentation
6. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For issues, questions, or feature requests:
1. Check the [USAGE_GUIDE.md](USAGE_GUIDE.md)
2. Review Azure AI Foundry documentation
3. Create an issue in this repository
4. Contact the development team

---

**Built with Azure AI Foundry** | **Production Ready** | **Enterprise Grade**
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
