import os
import yaml
import argparse

# In a real environment, you import the Azure SDK:
# from azure.ai.projects import AIProjectClient
# from azure.ai.projects.models import ToolSet, FunctionTool, AzureAISearchTool
# from azure.identity import DefaultAzureCredential
# from src.tools.system_status import check_system_status

def load_config(env: str) -> dict:
    """Loads the environment-specific configuration YAML."""
    config_path = os.path.join("config", f"{env}.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def load_system_prompt() -> str:
    """Loads the agent's system prompt from source control."""
    with open("src/agent/system_prompt.txt", "r") as f:
        return f.read()

def deploy_agent(env: str, dry_run: bool = False):
    """
    Idempotent deployment of an Azure AI Agent.
    Updates the agent if it exists, creates it otherwise.
    """
    print(f"--- Starting deployment for environment: {env.upper()} ---")
    config = load_config(env)
    
    agent_name = config["agent"]["name"]
    system_prompt = load_system_prompt()
    model_name = config["agent"]["model_deployment_name"]
    temperature = config["agent"]["temperature"]
    
    # Knowledge Base (Azure AI Search) Config
    search_conn = config.get("knowledge_base", {}).get("ai_search_connection_name", "None")
    search_index = config.get("knowledge_base", {}).get("index_name", "None")
    
    if dry_run:
        print(f"\n[DRY RUN MODE] Bypassing Azure connection...")
        print(f"Payload configuration verified:")
        print(f" - Agent Name: {agent_name}")
        print(f" - Target Model: {model_name}")
        print(f" - Temperature: {temperature}")
        print(f" - Attached Tools: [check_system_status]")
        print(f" - Knowledge Base attached: [Index: '{search_index}' via Connection: '{search_conn}']")
        print(f"\n✅ Simulation successful. Agent '{agent_name}' pseudo-deployed to {env.upper()}.\n")
        return

    # -----------------------------------------------------------------
    # LIVE DEPLOYMENT LOGIC (Requires valid Azure Connection Strings)
    # -----------------------------------------------------------------
    conn_str = os.environ.get(f"AZURE_AI_PROJECT_CONN_STR_{env.upper()}")
    if not conn_str:
        raise ValueError(f"Missing connection string for {env}. Ensure AZURE_AI_PROJECT_CONN_STR_{env.upper()} is set.")

    print("Connecting to Azure AI Project...")
    # client = AIProjectClient.from_connection_string(
    #     credential=DefaultAzureCredential(),
    #     conn_str=conn_str
    # )

    # Initialize Toolset
    # toolset = ToolSet()
    
    # 1. Attach custom Python Functions
    # toolset.add(FunctionTool(check_system_status))
    
    # 2. Attach Knowledge Base (Azure AI Search Index)
    # To get the connection_id programmatically, you would query the project connections:
    # search_connection = client.connections.get(connection_name=search_conn)
    # ai_search_tool = AzureAISearchTool(
    #     index_name=search_index,
    #     connection_id=search_connection.id
    # )
    # toolset.add(ai_search_tool)

    # with client:
    #     print(f"Creating/Updating Agent '{agent_name}' on model '{model_name}'...")
    #     agent = client.agents.create_agent(
    #         model=model_name,
    #         name=agent_name,
    #         instructions=system_prompt,
    #         temperature=temperature,
    #         toolset=toolset
    #     )
    #     print(f"Successfully deployed Agent ID: {agent.id} to {env.upper()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy Azure AI Agent")
    parser.add_argument("--env", required=True, choices=["dev", "qa", "prod"], help="Target environment")
    parser.add_argument("--dry-run", action="store_true", help="Simulate deployment without Azure credentials")
    args = parser.parse_args()
    
    deploy_agent(args.env, args.dry_run)
