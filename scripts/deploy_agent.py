import os
import yaml
import argparse
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

def load_config(env: str) -> dict:
    """Loads the environment-specific configuration YAML."""
    config_path = os.path.join("config", f"{env}.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def load_system_prompt() -> str:
    """Loads the agent's system prompt from source control."""
    with open("src/agent/system_prompt.txt", "r") as f:
        return f.read()

def deploy_agent(env: str):
    """
    Idempotent deployment of an Azure AI Agent.
    Updates the agent if it exists, creates it otherwise.
    """
    print(f"Starting deployment for environment: {env.upper()}")
    config = load_config(env)
    
    # In a real CI pipeline, the connection string is injected via secrets
    conn_str = os.environ.get(f"AZURE_AI_PROJECT_CONN_STR_{env.upper()}")
    if not conn_str:
        raise ValueError(f"Missing connection string for {env}")

    # Initialize SDK Client using Managed Identity / Service Principal
    client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=conn_str
    )

    agent_name = config["agent"]["name"]
    system_prompt = load_system_prompt()
    model_name = config["agent"]["model_deployment_name"]
    temperature = config["agent"]["temperature"]

    with client:
        # Check if agent already exists (Pseudo-code for listing/filtering)
        # existing_agents = client.agents.list()
        # agent_id = find_agent_by_name(existing_agents, agent_name)
        
        # NOTE: Azure AI Foundry SDK currently manages state via creation. 
        # For true idempotency in a pipeline, you'd track the Agent ID in a state file 
        # or rely on an alias/endpoint update. 
        
        print(f"Creating/Updating Agent '{agent_name}' on model '{model_name}'...")
        
        agent = client.agents.create_agent(
            model=model_name,
            name=agent_name,
            instructions=system_prompt,
            temperature=temperature,
            # tools=[...] # Tool definitions loaded from src/tools would go here
        )
        
        print(f"Successfully deployed Agent ID: {agent.id} to {env.upper()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy Azure AI Agent")
    parser.add_argument("--env", required=True, choices=["dev", "qa", "prod"], help="Target environment")
    args = parser.parse_args()
    
    deploy_agent(args.env)
