# AI Foundry DevOps Template

An enterprise-grade, end-to-end CI/CD template for managing and promoting Azure AI Foundry agents across isolated environments (Dev, QA, Prod).

## Architectural Vision

As AI moves from prototype to production, the "click-ops" approach of building agents in a UI falls apart. This template enforces an **SDK-First, Infrastructure-as-Code (IaC) approach**.

### How Components Connect

1. **Agent Definition (Source of Truth):**
   The agent's identity (`src/agent/system_prompt.txt`), capabilities (`src/tools/`), and model configurations are version-controlled. 
2. **Environment Isolation (`config/`):**
   Configurations define environment-specific bindings. For example, the Dev config binds the agent to a Dev database tool, while Prod binds to a read-only Prod replica.
3. **Automated Deployment (`scripts/deploy_agent.py`):**
   The pipeline executes this script, which uses the `azure-ai-projects` SDK to upsert the agent into the respective Azure AI Project based on the active environment configuration.
4. **Data & Evaluation (`evals/`):**
   Before an agent reaches Production, it must pass a quantitative evaluation. Golden datasets (`evals/datasets/`) containing expected inputs and outputs are run against the newly deployed QA agent using the Azure AI Evaluators SDK.

## Project Structure

```text
📦 AIFoundry-DevOps-Template
 ┣ 📂 .github/workflows      # CI/CD orchestration
 ┣ 📂 config                 # Environment-specific variables
 ┣ 📂 evals                  # Evaluation scripts and golden datasets
 ┣ 📂 infrastructure         # (To-Do) Bicep/Terraform templates for Hubs/Projects
 ┣ 📂 scripts                # Deployment and lifecycle scripts
 ┗ 📂 src
   ┣ 📂 agent                # System prompts and agent metadata
   ┗ 📂 tools                # Python tool definitions
```

## Getting Started

1. Set up your Azure AI Foundry Hub and Projects (Dev, QA, Prod) via your preferred IaC tool.
2. Update the environment variables in the `config/` directory.
3. Define your agent's persona in `src/agent/system_prompt.txt`.
4. Push to `main` to trigger the CI/CD pipeline.
