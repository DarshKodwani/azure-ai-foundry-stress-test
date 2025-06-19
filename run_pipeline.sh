#!/bin/bash

# Azure AI Foundry Stress Test Pipeline
# Runs the agent and generates a PDF report

echo "🚀 Starting Azure AI Foundry Stress Test Pipeline..."
echo "=================================================="

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
fi

# Step 1: Run the stress test agent
echo ""
echo "🔍 Step 1: Running stress test analysis..."
echo "------------------------------------------"
python run_agent.py

if [ $? -ne 0 ]; then
    echo "❌ Error: Agent execution failed"
    exit 1
fi

# Step 2: Generate PDF report
echo ""
echo "📄 Step 2: Generating PDF report..."
echo "-----------------------------------"
python generate_pdf_report.py

if [ $? -ne 0 ]; then
    echo "❌ Error: PDF generation failed"
    exit 1
fi

echo ""
echo "✅ Pipeline completed successfully!"
echo "📁 Check the 'reports/' directory for your PDF report"
echo "=================================================="
