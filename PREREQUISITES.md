# Pre-Flight Checklist & Prerequisites

As a standard engineering practice, before executing any automated infrastructure or AI deployments, the foundational environment and access controls must be established. This document details the hard prerequisites for deploying this Azure AI Foundry template.

---

## 1. Azure Infrastructure Requirements

You must have an active Azure Subscription with sufficient permissions (Owner or User Access Administrator + Contributor) to provision the following resources:

* **Azure AI Foundry Hub:** A central Hub resource to manage shared security and governance.
* **Isolated AI Projects:** Three distinct Azure AI Projects must be created under the Hub to map to our environments:
  * `Project-Dev`
  * `Project-QA`
  * `Project-Prod`
* **Model Deployments:** Each project requires provisioned AI models (e.g., `gpt-4o`). The deployment names must match the configurations set in the `config/*.yaml` files.
* **Connections:** Any external tool connections (e.g., Azure SQL, Cosmos DB, API endpoints) must be established within the respective AI Projects.

---

## 2. CI/CD Identity & Access Management (IAM)

To ensure secure, keyless authentication from our pipelines to Azure, we mandate the use of **OpenID Connect (OIDC)** and **Workload Identity Federation**. 

### Service Principal Setup
1. Create a Microsoft Entra ID (Azure AD) App Registration / Service Principal.
2. Grant this Service Principal the **Azure AI Developer** role on all three Azure AI Projects (Dev, QA, Prod).
3. Setup Federated Identity Credentials on the Service Principal pointing to your GitHub repository or Azure DevOps project.

---

## 3. Pipeline Specific Configurations

Depending on your CI/CD orchestrator, you must configure the following pipeline variables and environments.

### Option A: GitHub Actions
If you are using `.github/workflows/ai-agent-ci-cd.yml`:

* **Repository Secrets:** Add the following to your GitHub Repo Secrets:
  * `AZURE_CLIENT_ID`: The application ID of your Service Principal.
  * `AZURE_TENANT_ID`: Your Azure Tenant ID.
  * `AZURE_SUBSCRIPTION_ID`: Your Azure Subscription ID.
  * `AZURE_AI_PROJECT_CONN_STR_DEV`: Connection string for the Dev AI Project.
  * `AZURE_AI_PROJECT_CONN_STR_QA`: Connection string for the QA AI Project.
  * `AZURE_AI_PROJECT_CONN_STR_PROD`: Connection string for the Prod AI Project.
* **GitHub Environments:**
  * Navigate to Settings > Environments in your repo.
  * Create `Development`, `QA`, and `Production`.
  * **CRITICAL:** On the `Production` environment, check "Required reviewers" and assign the lead engineers or product owners.

### Option B: Azure DevOps
If you are using `azure-devops/azure-pipelines.yml`:

* **Service Connection:** 
  * Create an "Azure Resource Manager" Service Connection using "Workload Identity federation (automatic)".
  * Name it exactly `Azure-Service-Connection` (or update the YAML to match your name).
* **Variable Group:**
  * Go to Pipelines > Library.
  * Create a Variable Group named `AI-Foundry-Secrets`.
  * Add the three connection strings (`AZURE_AI_PROJECT_CONN_STR_DEV`, `AZURE_AI_PROJECT_CONN_STR_QA`, `AZURE_AI_PROJECT_CONN_STR_PROD`) as secure variables.
* **ADO Environments:**
  * Go to Pipelines > Environments.
  * Create `Development`, `QA`, and `Production`.
  * **CRITICAL:** Open the `Production` environment, go to "Approvals and checks", and add a manual approval step.

---

## 4. Local Development Environment

For local testing and tool development, ensure your local machine meets these standards:

* **Python:** Version 3.11 or higher.
* **Azure CLI:** Installed and authenticated (`az login`).
* **Environment Variables:** Set the connection strings locally in your `.env` or terminal profile.
* **Dependencies:** Install the project dependencies:
  ```bash
  pip install azure-ai-projects azure-identity azure-ai-evaluation pyyaml pytest flake8
  ```