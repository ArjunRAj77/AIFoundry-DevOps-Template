# AIFoundry DevOps Template

Welcome to the **AIFoundry DevOps Template**. This project provides a production-ready, Infrastructure-as-Code (IaC) CI/CD pipeline template for managing and deploying AI Agents into Azure AI Foundry.

## What Does This Do?

Historically, AI agents have been configured through manual clicks in web portals. This template allows you to define your agents, their system prompts, temperatures, models, and tools strictly in code. 

**Benefits of this setup:**
1. **Version Control for AI:** Your `system_prompt.txt` and `config/` YAML files live in source control. Any changes to the agent's behavior are tracked by Git commits.
2. **Deterministic Deployments:** Running the deployment script programmatically ensures that QA, DEV, and PROD environments are identical. No more "it works on my machine" AI bugs.
3. **Automatic Versioning:** The pipeline leverages the modern Azure AI Projects v2+ SDK (`create_version()`). This means every time the pipeline runs, it does not destroy your agent—it automatically stamps a new version (v1, v2, v3, etc.) allowing for safe rollbacks and A/B testing.
4. **Separation of Concerns:** The base model (e.g., `gpt-4o-mini`) acts as the "brain" and runs continuously. The Agent acts as the wrapper (the personality, the memory, the tools). You manage the Agent code here while keeping the underlying model stable.

## Architecture

* **`src/agent/system_prompt.txt`**: The core instructions for your AI agent.
* **`config/*.yaml`**: Environment-specific overrides (DEV, QA, PROD) containing the target base model and temperature.
* **`scripts/deploy_agent.py`**: The Python deployment engine that authenticates via `DefaultAzureCredential` and pushes the definition to Azure AI Foundry.
* **`evals/`**: (Placeholder) Directory for programmatic evaluations (like PromptFlow or AI Evaluation) to test the agent before pushing to prod.

## Quick Start Guide (CI/CD Deployment)

This template is designed to run automatically in your CI/CD pipelines (Infrastructure-as-Code), not from a local developer machine. Starter pipelines are included in the repository.

### 1. Base Configuration
1. Ensure you have fulfilled all Azure requirements in `PREREQUISITES.md`.
2. Open `config/dev.yaml` and ensure `model_deployment_name` perfectly matches your deployed base model in Azure.

### 2. Pipeline Integration

**Option A: GitHub Actions**
1. Locate the starter workflow inside the `.github/workflows/` directory.
2. Go to your repository **Settings > Secrets and variables > Actions**.
3. Add a Repository Variable named `AZURE_AI_PROJECT_ENDPOINT_DEV` with your endpoint URL.
4. Set up Azure authentication (we recommend OIDC federated credentials, mapping your repo to an Azure Managed Identity with the **Azure AI Developer** role).
5. Commit and push to the `main` branch to trigger your first agent deployment!

**Option B: Azure DevOps**
1. Locate the starter pipeline inside the `azure-devops/` directory.
2. In Azure DevOps, go to **Pipelines > Library** and create a **Variable Group**. Add `AZURE_AI_PROJECT_ENDPOINT_DEV` to it.
3. Go to **Project Settings > Service connections** and ensure you have an Azure Resource Manager (ARM) Workload Identity connection mapped to your Azure subscription.
4. Create a new pipeline referencing the YAML file, link your Variable Group and Service Connection, and click **Run**.

*(Note: If you absolutely must test the script locally before committing, ensure you run `az login` first, set the environment variable locally, and run `python scripts/deploy_agent.py --env dev`.)*

## Managing Environments

To deploy to QA or PROD, you must:
1. Create a `config/qa.yaml` or `config/prod.yaml`.
2. Set the corresponding environment variables: `AZURE_AI_PROJECT_ENDPOINT_QA` or `AZURE_AI_PROJECT_ENDPOINT_PROD`.
3. Pass the correct flag to the script: `--env qa`

## Extending the Agent (Phase 2)

Once the base deployment works, you can easily attach specialized tools (like Python functions or Azure AI Search Knowledge Bases). Look inside `scripts/deploy_agent.py` for the commented-out `ToolSet` blocks. You can uncomment these to inject tools natively into the agent definition.