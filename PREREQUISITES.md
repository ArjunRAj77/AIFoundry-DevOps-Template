# Prerequisites

Before you can run the deployment pipeline, you must ensure your local development environment and your Azure Cloud environment are configured correctly.

## 1. Azure Cloud Setup

You cannot deploy an agent into a vacuum. You must have the following set up in your Azure environment first:

1. **Azure Subscription & Resource Group:** An active billing account.
2. **Azure AI Foundry Hub & Project:** Create a Hub and an AI Project inside the Azure AI Foundry portal.
3. **Base Model Deployment:** 
   * Navigate to your AI Project in the portal.
   * Go to **Models + endpoints** (or Deployments) -> **Deploy model** -> **Deploy base model**.
   * Deploy a language model (we recommend `gpt-4o-mini`).
   * **Write down the Deployment Name!** You will need to put this exact name inside the `config/dev.yaml` file (`model_deployment_name` field).
4. **Permissions:** The account you use to deploy *must* have the **Azure AI Developer** role assigned to it for the target AI Project.

## 2. Local Environment Setup

Ensure you have Python installed, then install the required libraries via the `requirements.txt`:

```bash
pip install -r requirements.txt
```
*(This installs `azure-ai-projects`, `azure-identity`, `pyyaml`, etc.)*

You must also install the **Azure CLI**. Once installed, log in to your Azure account so the script can authenticate using `DefaultAzureCredential`:

```bash
az login
```

## 3. Environment Variables

The deployment script requires an environment variable containing the exact URL of your Azure AI Project Endpoint.

### Finding your Endpoint URL:
If you are using a modern Azure AI Project, the URL format is:
`https://<your-ai-services-account-name>.services.ai.azure.com/api/projects/<your-project-name>`

*(If you are using an older Machine Learning Workspace backend, the URL format must be the long-form Resource ID: `https://<region>.api.azureml.ms/subscriptions/<sub-id>/resourceGroups/<rg-name>/providers/Microsoft.MachineLearningServices/workspaces/<project-name>`)*

### Setting the Variable:
Set the variable for the environment you are targeting. For development (`--env dev`):

**PowerShell (Windows):**
```powershell
$env:AZURE_AI_PROJECT_ENDPOINT_DEV="<your-endpoint-url-here>"
```

**Bash (Linux/Mac):**
```bash
export AZURE_AI_PROJECT_ENDPOINT_DEV="<your-endpoint-url-here>"
```

Once this is set, your system is fully pre-flighted and ready to deploy via the instructions in `README.md`.