import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white, blue, red, green
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF

def main(workflow_results: str, report_title: str = "Financial Stress Testing Report", report_format: str = "executive") -> dict:
    try:
        # Parse workflow results
        if workflow_results.startswith('{'):
            results_data = json.loads(workflow_results)
        else:
            # Try to load from file if it's a filename
            if os.path.exists(workflow_results):
                with open(workflow_results, 'r') as f:
                    results_data = json.load(f)
            else:
                return {"report_path": f"Error: Could not parse workflow results: {workflow_results}"}
        
        # Generate PDF report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"stress_test_report_{timestamp}.pdf"
        report_path = os.path.join("reports", filename)
        
        # Ensure reports directory exists
        os.makedirs("reports", exist_ok=True)
        
        # Create the PDF
        doc = SimpleDocTemplate(report_path, pagesize=A4, 
                              topMargin=1*inch, bottomMargin=1*inch,
                              leftMargin=1*inch, rightMargin=1*inch)
        
        # Build the story (content)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#1f4e79'),
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=HexColor('#1f4e79'),
            borderWidth=1,
            borderColor=HexColor('#1f4e79'),
            borderPadding=5
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=15,
            textColor=HexColor('#2d5aa0')
        )
        
        # Add content based on format
        if report_format.lower() == "executive":
            story.extend(build_executive_report(results_data, title_style, heading_style, subheading_style, styles))
        elif report_format.lower() == "detailed":
            story.extend(build_detailed_report(results_data, title_style, heading_style, subheading_style, styles))
        else:  # comprehensive
            story.extend(build_comprehensive_report(results_data, title_style, heading_style, subheading_style, styles))
        
        # Build PDF
        doc.build(story)
        
        return {"report_path": f"PDF report generated successfully: {report_path}"}
        
    except Exception as e:
        return {"report_path": f"Error generating PDF report: {str(e)}"}

def build_executive_report(data, title_style, heading_style, subheading_style, styles):
    """Build an executive summary report."""
    story = []
    
    # Title Page
    story.append(Paragraph("Financial Stress Testing", title_style))
    story.append(Paragraph("Executive Summary Report", title_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Metadata
    metadata = data.get('metadata', {})
    story.append(Paragraph("Report Information", heading_style))
    
    report_info = [
        ['Report Date:', datetime.now().strftime('%B %d, %Y')],
        ['Workflow Type:', metadata.get('workflow_type', 'Unknown')],
        ['Total Stages:', str(metadata.get('total_stages', 'N/A'))],
        ['Completed Stages:', str(metadata.get('completed_stages', 'N/A'))],
        ['Generation Time:', metadata.get('timestamp', 'N/A')]
    ]
    
    info_table = Table(report_info, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#cccccc')),
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#f0f0f0'))
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Portfolio Overview
    requirements = data.get('initial_requirements', {})
    story.append(Paragraph("Portfolio Overview", heading_style))
    
    portfolio_data = [
        ['Portfolio Type:', requirements.get('portfolio_type', 'N/A').replace('_', ' ').title()],
        ['Portfolio Value:', f"${requirements.get('portfolio_value', 0):,.2f}"],
        ['Risk Tolerance:', requirements.get('risk_tolerance', 'N/A').title()],
        ['Time Horizon:', f"{requirements.get('time_horizon', 'N/A')} years"],
        ['Regulatory Framework:', requirements.get('regulatory_framework', 'N/A').replace('_', ' ').upper()]
    ]
    
    portfolio_table = Table(portfolio_data, colWidths=[2*inch, 4*inch])
    portfolio_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#cccccc')),
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#e6f3ff'))
    ]))
    story.append(portfolio_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    
    final_recs = data.get('final_recommendations', {})
    exec_summary = final_recs.get('executive_summary', 'Comprehensive stress testing analysis completed.')
    story.append(Paragraph(exec_summary, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Key Findings
    story.append(Paragraph("Key Findings", subheading_style))
    key_findings = final_recs.get('key_findings', [])
    for finding in key_findings:
        story.append(Paragraph(f"• {finding}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Action Items
    story.append(Paragraph("Immediate Action Items", subheading_style))
    action_items = final_recs.get('action_items', [])
    for item in action_items:
        story.append(Paragraph(f"• {item}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Next Steps
    story.append(Paragraph("Next Steps", subheading_style))
    next_steps = final_recs.get('next_steps', [])
    for step in next_steps:
        story.append(Paragraph(f"• {step}", styles['Normal']))
    
    # Footer
    story.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=HexColor('#666666'),
        alignment=TA_CENTER
    )
    story.append(Paragraph("This report was generated using Azure AI Foundry Skills-Based Stress Testing Workflow", footer_style))
    
    return story

def build_detailed_report(data, title_style, heading_style, subheading_style, styles):
    """Build a detailed technical report."""
    story = []
    
    # Title
    story.append(Paragraph("Financial Stress Testing", title_style))
    story.append(Paragraph("Detailed Technical Report", title_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Include executive content
    story.extend(build_executive_report(data, title_style, heading_style, subheading_style, styles))
    
    # Add page break
    story.append(PageBreak())
    
    # Detailed Stage Results
    story.append(Paragraph("Detailed Stage Analysis", heading_style))
    
    stage_outputs = data.get('stage_outputs', {})
    
    for stage_name, stage_data in stage_outputs.items():
        story.append(Paragraph(f"{stage_name.replace('_', ' ').title()}", subheading_style))
        
        if isinstance(stage_data, dict):
            for key, value in stage_data.items():
                if key != 'error' and value:
                    story.append(Paragraph(f"<b>{key.replace('_', ' ').title()}:</b>", styles['Normal']))
                    
                    if isinstance(value, str):
                        # Truncate very long strings
                        display_value = value[:1000] + "..." if len(value) > 1000 else value
                        story.append(Paragraph(display_value, styles['Normal']))
                    else:
                        story.append(Paragraph(str(value), styles['Normal']))
                    
                    story.append(Spacer(1, 0.1*inch))
        
        story.append(Spacer(1, 0.2*inch))
    
    return story

def build_comprehensive_report(data, title_style, heading_style, subheading_style, styles):
    """Build a comprehensive report with all details."""
    story = []
    
    # Include detailed content
    story.extend(build_detailed_report(data, title_style, heading_style, subheading_style, styles))
    
    # Add additional comprehensive sections
    story.append(PageBreak())
    story.append(Paragraph("Technical Appendix", heading_style))
    
    # User Approvals
    story.append(Paragraph("Workflow Approvals", subheading_style))
    user_approvals = data.get('user_approvals', {})
    
    approval_data = []
    for stage, approval in user_approvals.items():
        approval_data.append([stage.replace('_', ' ').title(), approval.title()])
    
    if approval_data:
        approval_table = Table([['Stage', 'Status']] + approval_data, colWidths=[3*inch, 2*inch])
        approval_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#cccccc')),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1f4e79')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white)
        ]))
        story.append(approval_table)
    
    story.append(Spacer(1, 0.3*inch))
    
    # Raw Data Section
    story.append(Paragraph("Raw Workflow Data", subheading_style))
    story.append(Paragraph("Complete workflow results in JSON format:", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    # Format JSON nicely
    json_style = ParagraphStyle(
        'JSON',
        parent=styles['Code'],
        fontSize=8,
        fontName='Courier',
        leftIndent=20,
        rightIndent=20,
        spaceAfter=10
    )
    
    try:
        formatted_json = json.dumps(data, indent=2)[:2000] + "\n... [Content truncated for readability]"
        story.append(Paragraph(formatted_json.replace('\n', '<br/>').replace(' ', '&nbsp;'), json_style))
    except:
        story.append(Paragraph("Raw data formatting error", styles['Normal']))
    
    return story

def create_risk_chart():
    """Create a sample risk visualization chart."""
    drawing = Drawing(400, 200)
    
    # Create a simple bar chart
    chart = VerticalBarChart()
    chart.x = 50
    chart.y = 50
    chart.height = 125
    chart.width = 300
    chart.data = [
        [20, 35, 15, 25],  # Sample risk values
    ]
    chart.categoryAxis.categoryNames = ['Market Risk', 'Credit Risk', 'Operational Risk', 'Liquidity Risk']
    chart.bars[0].fillColor = HexColor('#1f4e79')
    
    drawing.add(chart)
    return drawing
