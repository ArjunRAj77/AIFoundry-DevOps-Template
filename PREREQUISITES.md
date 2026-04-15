# System & Infrastructure Prerequisites

To successfully deploy and maintain the **AIFoundry-DevOps-Template**, your cloud infrastructure, CI/CD runners, and local development environments must meet the following baseline requirements.

This document outlines the exact provisioning required before attempting to execute the deployment engine.

---

## 1. Cloud Infrastructure (Azure)

Agents cannot exist without foundational infrastructure. The following Azure resources must be provisioned prior to deployment:

### Core Resources
*   **Azure Subscription & Resource Group:** An active subscription with sufficient quota for standard LLM inference.
*   **Azure AI Foundry Hub:** The overarching workspace container.
*   **Azure AI Project:** Created within the Hub. This acts as the boundary for your agents, connections, and RBAC.

### The Base Model (Crucial Step)
As noted in the architectural documentation, the Agent is just a wrapper. You must deploy its "brain" manually or via Terraform first:
1. Navigate to your AI Project in the Azure AI Foundry portal.
2. Go to **Models + endpoints** -> **Deploy base model**.
3. Deploy a target model (e.g., `gpt-4o-mini`).
4. **Important:** The exact string you define as the deployment name in the portal *must* match the `model_deployment_name` in your `config/*.yaml` files. Failure to match this will result in a `Resource Not Found` error during pipeline execution.

### Identity & Access Management (RBAC)
The executing identity (your local user account or the CI/CD Service Principal) must be granted the **Azure AI Developer** role scoped to the target AI Project.

---

## 2. CI/CD Configuration (GitHub Actions)

For the automated pipeline to function securely across environments (Dev, QA, Prod), we utilize OpenID Connect (OIDC) instead of long-lived secrets. 

### GitHub Environment Secrets
In your GitHub repository settings, configure the following secrets for the OIDC login (`azure/login@v1`):
*   `AZURE_CLIENT_ID`: The application ID of your deployed Service Principal / Managed Identity.
*   `AZURE_TENANT_ID`: Your Azure AD Directory ID.
*   `AZURE_SUBSCRIPTION_ID`: The target subscription ID.

### Environment-Specific Variables
The GitHub pipeline expects the target endpoints to be injected at runtime:
*   `AZURE_AI_PROJECT_ENDPOINT_DEV`
*   `AZURE_AI_PROJECT_ENDPOINT_QA`
*   `AZURE_AI_PROJECT_ENDPOINT_PROD`

---

## 3. Local Development Environment

If you are developing custom tools (`src/tools/`) or running the deployment engine locally for debugging, ensure the following setup:

### Toolchain
*   **Python 3.11+**
*   **Azure CLI:** Required for local `DefaultAzureCredential` authentication.

### Setup Steps
1. **Clone & Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Authenticate with Azure:**
   ```bash
   az login
   ```
   *(Ensure you log in with an account that has the Azure AI Developer role for the project).*

### Local Environment Variables
The deployment script (`deploy_agent.py`) dynamically pulls the project endpoint from your system variables based on the target environment.

**Modern Hub URL Format:**
`https://<hub-name>.services.ai.azure.com/api/projects/<project-name>`

*(Legacy API Note: If using an older Machine Learning Workspace backend, construct the full ARM Resource ID URL: `https://<region>.api.azureml.ms/subscriptions/<sub-id>/resourceGroups/<rg-name>/providers/Microsoft.MachineLearningServices/workspaces/<project-name>`)*

**Injecting the Variable (Windows / PowerShell):**
```powershell
$env:AZURE_AI_PROJECT_ENDPOINT_DEV="https://your-hub.services.ai.azure.com/api/projects/your-project"
```

**Injecting the Variable (Linux / Mac):**
```bash
export AZURE_AI_PROJECT_ENDPOINT_DEV="https://your-hub.services.ai.azure.com/api/projects/your-project"
```

Once the cloud resources are provisioned and your endpoint variable is set, you are cleared to proceed to the deployment phase documented in `README.md`.