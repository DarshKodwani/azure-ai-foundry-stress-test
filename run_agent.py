import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

def main():
    if not os.getenv("PROJECT_ENDPOINT"):
        print("Error: PROJECT_ENDPOINT environment variable is required")
        return
    
    try:
        project_client = AIProjectClient(
            credential=DefaultAzureCredential(),
            endpoint=os.environ["PROJECT_ENDPOINT"],
        )
        
        from tools.summarize_tool.summarize_tool import main as summarize_tool
        
        scenario_input = '''
        In the 2022 Bank of England stress test, the scenario featured a deep global recession with UK GDP falling by 5%, unemployment rising to 8.5%, and property prices dropping by over 30%. The stress also included a sharp rise in interest rates and inflation.
        '''
        
        print("Running stress test summarization...")
        result = summarize_tool(scenario_input)
        print("Summary:")
        print(result["summary"])
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
