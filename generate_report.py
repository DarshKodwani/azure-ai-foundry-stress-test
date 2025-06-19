#!/usr/bin/env python3
"""
PDF Report Generator for Azure AI Foundry Stress Testing Workflow

This script generates professional PDF reports from JSON workflow results.
Can be used standalone or as part of the workflow.

Usage:
    python generate_report.py <json_file> [report_type] [report_title]
    
    json_file: Path to the workflow results JSON file
    report_type: executive, detailed, or comprehensive (default: executive)
    report_title: Custom title for the report (optional)

Examples:
    python generate_report.py workflow_results_20250619_130515.json
    python generate_report.py workflow_results.json detailed "Q4 2025 Stress Test"
    python generate_report.py results.json comprehensive
"""

import sys
import os
import json
from datetime import datetime

# Add the current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def main():
    """Main function to generate PDF report from JSON results."""
    
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("❌ Error: JSON file path required")
        print("\nUsage:")
        print("    python generate_report.py <json_file> [report_type] [report_title]")
        print("\nReport types: executive, detailed, comprehensive")
        print("\nExample:")
        print("    python generate_report.py workflow_results_20250619_130515.json executive")
        return 1
    
    json_file = sys.argv[1]
    report_type = sys.argv[2] if len(sys.argv) > 2 else "executive"
    report_title = sys.argv[3] if len(sys.argv) > 3 else "Financial Stress Testing Report"
    
    # Validate inputs
    if not os.path.exists(json_file):
        print(f"❌ Error: JSON file not found: {json_file}")
        return 1
    
    if report_type not in ["executive", "detailed", "comprehensive"]:
        print(f"❌ Error: Invalid report type '{report_type}'. Use: executive, detailed, or comprehensive")
        return 1
    
    print(f"🚀 Generating PDF Report...")
    print(f"📄 Input: {json_file}")
    print(f"📊 Type: {report_type}")
    print(f"📝 Title: {report_title}")
    print()
    
    try:
        # Load and execute the PDF tool
        from tools.pdf_report_tool.pdf_report_tool import main as generate_pdf
        
        # Read the JSON file
        with open(json_file, 'r') as f:
            workflow_results = f.read()
        
        # Generate the PDF
        result = generate_pdf(
            workflow_results=workflow_results,
            report_title=report_title,
            report_format=report_type
        )
        
        # Check result
        report_path = result.get('report_path', '')
        if 'Error' in report_path:
            print(f"❌ {report_path}")
            return 1
        else:
            print(f"✅ {report_path}")
            
            # Get the actual filename from the result
            if ':' in report_path:
                actual_file = report_path.split(':')[-1].strip()
                if os.path.exists(actual_file):
                    file_size = os.path.getsize(actual_file)
                    print(f"📁 File size: {file_size:,} bytes")
                    print(f"📍 Location: {os.path.abspath(actual_file)}")
        
        return 0
        
    except ImportError as e:
        print(f"❌ Import Error: {str(e)}")
        print("   Please ensure reportlab is installed:")
        print("   pip install reportlab")
        return 1
    except FileNotFoundError as e:
        print(f"❌ File Error: {str(e)}")
        print("   Please ensure you're running from the correct directory")
        return 1
    except json.JSONDecodeError as e:
        print(f"❌ JSON Error: Invalid JSON format in {json_file}")
        print(f"   {str(e)}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        return 1

def list_available_json_files():
    """List available JSON workflow files."""
    print("📁 Available workflow JSON files:")
    json_files = [f for f in os.listdir('.') if f.startswith('workflow_results_') and f.endswith('.json')]
    
    if json_files:
        for i, file in enumerate(sorted(json_files), 1):
            file_date = datetime.fromtimestamp(os.path.getmtime(file))
            print(f"   {i}. {file} ({file_date.strftime('%Y-%m-%d %H:%M')})")
    else:
        print("   No workflow result files found")
    print()

def interactive_mode():
    """Interactive mode for report generation."""
    print("🎯 INTERACTIVE PDF REPORT GENERATOR")
    print("="*50)
    
    list_available_json_files()
    
    # Get JSON file
    json_file = input("Enter JSON file name (or path): ").strip()
    if not json_file:
        print("❌ No file specified")
        return 1
    
    # Get report type
    print("\n📊 Report Types:")
    print("   1. Executive (Summary for leadership)")
    print("   2. Detailed (Technical analysis)")
    print("   3. Comprehensive (Complete with appendix)")
    
    type_choice = input("\nSelect report type (1-3): ").strip()
    type_map = {'1': 'executive', '2': 'detailed', '3': 'comprehensive'}
    report_type = type_map.get(type_choice, 'executive')
    
    # Get title
    report_title = input("\nEnter custom report title (press Enter for default): ").strip()
    if not report_title:
        report_title = "Financial Stress Testing Report"
    
    # Generate report
    print(f"\n🚀 Generating {report_type} report...")
    sys.argv = ['generate_report.py', json_file, report_type, report_title]
    return main()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments - run interactive mode
        exit_code = interactive_mode()
    else:
        # Arguments provided - run direct mode
        exit_code = main()
    
    sys.exit(exit_code)
