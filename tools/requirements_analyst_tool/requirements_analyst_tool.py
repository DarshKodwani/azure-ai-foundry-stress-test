import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

def main(portfolio_type: str, portfolio_value: float, risk_tolerance: str, 
         time_horizon: float, regulatory_framework: str, custom_scenarios: str, 
         output_format: str) -> dict:
    try:
        client = AzureOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            api_version=os.getenv("OPENAI_API_VERSION", "2024-10-21"),
            azure_endpoint=os.getenv("OPENAI_API_BASE")
        )

        prompt = f"""
        You are an expert financial risk analyst specializing in stress testing requirements analysis.
        
        Analyze the following portfolio requirements and provide intelligent recommendations:
        
        Portfolio Details:
        - Type: {portfolio_type}
        - Value: ${portfolio_value:,.2f}
        - Risk Tolerance: {risk_tolerance}
        - Time Horizon: {time_horizon} years
        - Regulatory Framework: {regulatory_framework}
        - Custom Scenarios: {custom_scenarios if custom_scenarios else 'None specified'}
        
        Provide a comprehensive analysis including:
        1. Portfolio risk profile assessment
        2. Appropriate stress testing methodologies
        3. Recommended scenario types based on portfolio characteristics
        4. Key risk factors to focus on
        5. Regulatory considerations (if applicable)
        6. Suggested stress test parameters and severity levels
        
        Format your response as a structured analysis suitable for {output_format} output.
        Use clear sections and bullet points with dashes for readability.
        """

        response = client.chat.completions.create(
            model=os.getenv("DEPLOYMENT_NAME", "gpt-4o"),
            messages=[
                {"role": "system", "content": "You are an expert financial risk analyst specializing in stress testing requirements analysis. Provide clear, actionable recommendations based on portfolio characteristics and regulatory requirements."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3
        )

        analysis_result = response.choices[0].message.content
        
        # Structure the output
        result = {
            "portfolio_type": portfolio_type,
            "portfolio_value": portfolio_value,
            "risk_tolerance": risk_tolerance,
            "time_horizon": time_horizon,
            "regulatory_framework": regulatory_framework,
            "analysis": analysis_result,
            "recommended_scenarios": extract_scenarios(analysis_result),
            "key_risk_factors": extract_risk_factors(analysis_result)
        }
        
        return {"analysis_result": json.dumps(result, indent=2)}
    
    except Exception as e:
        return {"analysis_result": f"Error: {str(e)}. Please check your Azure OpenAI configuration and environment variables."}

def extract_scenarios(analysis_text: str) -> list:
    """Extract recommended scenarios from the analysis text"""
    # Simple extraction - in a real implementation, this could be more sophisticated
    scenarios = []
    if "market crash" in analysis_text.lower():
        scenarios.append("market_crash")
    if "interest rate" in analysis_text.lower():
        scenarios.append("interest_rate_shock")
    if "credit" in analysis_text.lower():
        scenarios.append("credit_stress")
    if "liquidity" in analysis_text.lower():
        scenarios.append("liquidity_crisis")
    return scenarios

def extract_risk_factors(analysis_text: str) -> list:
    """Extract key risk factors from the analysis text"""
    # Simple extraction - in a real implementation, this could be more sophisticated
    risk_factors = []
    if "market risk" in analysis_text.lower():
        risk_factors.append("market_risk")
    if "credit risk" in analysis_text.lower():
        risk_factors.append("credit_risk")
    if "operational risk" in analysis_text.lower():
        risk_factors.append("operational_risk")
    if "liquidity risk" in analysis_text.lower():
        risk_factors.append("liquidity_risk")
    return risk_factors
