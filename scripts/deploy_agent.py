import os
import sys
import yaml
import argparse

try:
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects.models import PromptAgentDefinition
    
    # [COMMENTED OUT FOR PHASE 1]
    # from azure.ai.projects.models import ToolSet, FunctionTool, AzureAISearchTool
except ImportError:
    print("[X] FATAL: Missing required Azure SDK packages.")
    print("    Run: pip install azure-ai-projects azure-identity pyyaml")
    sys.exit(1)

def load_config(env: str) -> dict:
    """Loads the environment-specific configuration YAML."""
    config_path = os.path.join("config", f"{env}.yaml")
    print(f"[*] Loading configuration from: {config_path}")
    if not os.path.exists(config_path):
        print(f"[X] ERROR: Configuration file not found: {config_path}")
        sys.exit(1)
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def load_system_prompt() -> str:
    """Loads the agent's system prompt from source control."""
    prompt_path = os.path.join("src", "agent", "system_prompt.txt")
    print(f"[*] Loading system prompt from: {prompt_path}")
    if not os.path.exists(prompt_path):
        print(f"[X] ERROR: System prompt file not found: {prompt_path}")
        sys.exit(1)
    with open(prompt_path, "r") as f:
        return f.read()

def deploy_agent(env: str):
    """
    Deploys an Azure AI Agent.
    """
    print(f"\n{'='*50}")
    print(f"🚀 INITIATING DEPLOYMENT PIPELINE: {env.upper()}")
    print(f"{'='*50}\n")
    
    config = load_config(env)
    system_prompt = load_system_prompt()
    
    agent_name = config.get("agent", {}).get("name", f"Agent-{env.upper()}")
    model_name = config.get("agent", {}).get("model_deployment_name")
    temperature = config.get("agent", {}).get("temperature", 0.7)
    
    if not model_name:
        print("[X] ERROR: 'model_deployment_name' is missing in the configuration.")
        sys.exit(1)

    # Validate Endpoint exists in environment
    endpoint_var = f"AZURE_AI_PROJECT_ENDPOINT_{env.upper()}"
    endpoint = os.environ.get(endpoint_var)
    if not endpoint:
        print(f"[X] ERROR: Missing project endpoint.")
        print(f"    Ensure the environment variable {endpoint_var} is set.")
        sys.exit(1)

    # Mildly obfuscate endpoint to prevent leaking full subscription IDs in CI/CD logs if preferred, 
    # but still show enough to verify the target.
    masked_endpoint = endpoint
    if "subscriptions/" in endpoint:
        parts = endpoint.split("subscriptions/")
        if len(parts) > 1 and "/" in parts[1]:
            sub_id = parts[1].split("/")[0]
            masked_endpoint = endpoint.replace(sub_id, "********-****-****-****-************")

    print("\n" + "="*50)
    print("📋 DEPLOYMENT PRE-FLIGHT CHECK")
    print("="*50)
    print(f"Environment    : {env.upper()}")
    print(f"Target Endpoint: {masked_endpoint}")
    print(f"Agent Name     : {agent_name}")
    print(f"Model          : {model_name}")
    print(f"Temperature    : {temperature}")
    print(f"System Prompt  : {len(system_prompt)} characters loaded")
    print("="*50 + "\n")

    print("[*] Authenticating with Azure (DefaultAzureCredential)...")
    
    try:
        # Initialize the client using the recommended factory method
        project_client = AIProjectClient(
            credential=DefaultAzureCredential(),
            endpoint=endpoint
        )
        print("[+] Authentication successful. Client initialized.")

        # [COMMENTED OUT FOR PHASE 1: TOOLSET AND KNOWLEDGE BASE]
        # print("[*] Initializing tools and knowledge base...")
        # toolset = ToolSet()
        #
        # 1. Attach custom Python Functions
        # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        # from src.tools.system_status import check_system_status
        # system_status_tool = FunctionTool(check_system_status)
        # toolset.add(system_status_tool)
        # print("[+] Custom Python functions attached.")
        #
        # 2. Attach Knowledge Base (Azure AI Search Index)
        # search_conn = config.get("knowledge_base", {}).get("ai_search_connection_name")
        # search_index = config.get("knowledge_base", {}).get("index_name")
        # if search_conn and search_index:
        #     # To attach a Search index programmatically, we need the connection ID
        #     search_connection = project_client.connections.get(connection_name=search_conn)
        #     ai_search_tool = AzureAISearchTool(
        #         index_name=search_index,
        #         connection_id=search_connection.id
        #     )
        #     toolset.add(ai_search_tool)
        #     print("[+] Azure AI Search knowledge base attached.")

        with project_client:
            print(f"[*] Packaging PromptAgentDefinition...")
            # Base deployment (Active for Phase 1)
            agent_definition = PromptAgentDefinition(
                model=model_name,
                instructions=system_prompt,
                temperature=temperature
                # toolset=toolset  # [COMMENTED OUT FOR PHASE 1]
            )
            
            print(f"[*] Transmitting to Azure AI Foundry to create/update agent version...")
            agent = project_client.agents.create_version(
                agent_name=agent_name,
                definition=agent_definition
            )
            
            print(f"\n{'='*50}")
            print(f"✅ DEPLOYMENT SUCCESSFUL")
            print(f"{'='*50}")
            print(f"Agent Name : {agent.name}")
            print(f"Agent ID   : {agent.id}")
            print(f"Model      : {model_name}")
            print(f"{'='*50}\n")
    
    except Exception as e:
        print(f"\n[X] DEPLOYMENT FAILED")
        print(f"    Reason: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy Azure AI Agent")
    parser.add_argument("--env", required=True, choices=["dev", "qa", "prod"], help="Target environment (dev, qa, prod)")
    args = parser.parse_args()
    
    deploy_agent(args.env)