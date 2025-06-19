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
                {"role": "system", "content": "You are an expert financial analyst specializing in stress testing and regulatory scenarios. Always provide clear, well-structured summaries without using markdown formatting. Use plain text with clear section headers, bullet points using dashes, and proper paragraph breaks for readability in PDF reports."},
                {"role": "user", "content": f"Summarize this Bank of England stress scenario in a clear, structured format suitable for a professional PDF report. Do NOT use markdown formatting (no **, ##, ###, etc.). Use plain text with clear section titles, bullet points with dashes, and proper spacing. Include key metrics, impacts, and analysis:\n\n{scenario_text}"}
            ],
            max_tokens=600,
            temperature=0.3
        )

        return {"summary": response.choices[0].message.content}
    
    except Exception as e:
        return {"summary": f"Error: {str(e)}. Please check your Azure OpenAI configuration and environment variables."}
