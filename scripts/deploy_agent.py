import os
import sys
import yaml
import argparse

try:
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential
    
    # [COMMENTED OUT FOR PHASE 1]
    # from azure.ai.projects.models import ToolSet, FunctionTool, AzureAISearchTool
except ImportError:
    print("❌ Error: Missing required Azure SDK packages. Run `pip install azure-ai-projects azure-identity pyyaml`")
    sys.exit(1)

def load_config(env: str) -> dict:
    """Loads the environment-specific configuration YAML."""
    config_path = os.path.join("config", f"{env}.yaml")
    if not os.path.exists(config_path):
        print(f"❌ Error: Configuration file not found for environment '{env}': {config_path}")
        sys.exit(1)
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def load_system_prompt() -> str:
    """Loads the agent's system prompt from source control."""
    prompt_path = os.path.join("src", "agent", "system_prompt.txt")
    if not os.path.exists(prompt_path):
        print(f"❌ Error: System prompt file not found: {prompt_path}")
        sys.exit(1)
    with open(prompt_path, "r") as f:
        return f.read()

def deploy_agent(env: str):
    """
    Deploys an Azure AI Agent.
    """
    print(f"--- Starting deployment for environment: {env.upper()} ---")
    config = load_config(env)
    
    agent_name = config.get("agent", {}).get("name", f"Agent-{env.upper()}")
    model_name = config.get("agent", {}).get("model_deployment_name")
    temperature = config.get("agent", {}).get("temperature", 0.7)
    system_prompt = load_system_prompt()
    
    if not model_name:
        print("❌ Error: 'model_deployment_name' is missing in the configuration.")
        sys.exit(1)

    # Validate Connection String exists in environment
    conn_str = os.environ.get(f"AZURE_AI_PROJECT_CONN_STR_{env.upper()}")
    if not conn_str:
        print(f"❌ Error: Missing connection string for {env}. Ensure AZURE_AI_PROJECT_CONN_STR_{env.upper()} is set.")
        sys.exit(1)

    print("Authenticating with Azure AI Project...")
    
    try:
        # Initialize the client using the recommended factory method
        project_client = AIProjectClient.from_connection_string(
            credential=DefaultAzureCredential(),
            conn_str=conn_str
        )

        # [COMMENTED OUT FOR PHASE 1: TOOLSET AND KNOWLEDGE BASE]
        # print("Initializing tools and knowledge base...")
        # toolset = ToolSet()
        #
        # 1. Attach custom Python Functions
        # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        # from src.tools.system_status import check_system_status
        # system_status_tool = FunctionTool(check_system_status)
        # toolset.add(system_status_tool)
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

        with project_client:
            print(f"Creating Agent '{agent_name}' on model '{model_name}'...")
            
            # Base deployment (Active for Phase 1)
            agent = project_client.agents.create_agent(
                model=model_name,
                name=agent_name,
                instructions=system_prompt,
                temperature=temperature
                # toolset=toolset  # [COMMENTED OUT FOR PHASE 1]
            )
            
            print(f"✅ Successfully deployed Agent! ID: {agent.id} to {env.upper()}")
    
    except Exception as e:
        print(f"❌ Deployment failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy Azure AI Agent")
    parser.add_argument("--env", required=True, choices=["dev", "qa", "prod"], help="Target environment (dev, qa, prod)")
    args = parser.parse_args()
    
    deploy_agent(args.env)
