# AI Foundry DevOps Template

An enterprise-grade, end-to-end CI/CD template for managing and promoting Azure AI Foundry agents across isolated environments (Dev, QA, Prod).

---

## 🚀 Quick Start (Local Testing)

The scripts in this repository are designed to connect to live Azure resources. 

### Step 1: Open Your Terminal
Open PowerShell or your preferred terminal and navigate to this folder:
```bash
cd G:\AI\AIFoundry-DevOps-Template
```

### Step 2: Create a Virtual Environment (Recommended)
A virtual environment keeps your Python packages isolated.
```bash
python -m venv venv
```
Activate it:
* **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`
* **Windows (Command Prompt):** `.\venv\Scripts\activate.bat`
* **Mac/Linux:** `source venv/bin/activate`

### Step 3: Install Dependencies
Install the required Python SDKs:
```bash
pip install -r requirements.txt
```

### Step 4: Configure Azure Credentials
Before deploying, you must provide the connection string for your Azure AI Project. Set this as an environment variable in your terminal:

**Windows (PowerShell):**
```powershell
$env:AZURE_AI_PROJECT_CONN_STR_DEV="your_connection_string_here"
```
**Mac/Linux:**
```bash
export AZURE_AI_PROJECT_CONN_STR_DEV="your_connection_string_here"
```
*(Ensure you are also authenticated with Azure via `az login` or appropriate Service Principal credentials if not using a managed identity).*

### Step 5: Run a Live Deployment (Phase 1)
Deploy the barebones agent to the Development environment:
```bash
python scripts/deploy_agent.py --env dev
```
*You should see a success message showing the agent's ID deployed to your Azure environment!*

---

## Architectural Vision & Phased Rollout

As AI moves from prototype to production, building agents manually in a UI falls apart. This template enforces an **SDK-First, Infrastructure-as-Code (IaC) approach**.

### Current Implementation (Phase 1: Barebones Agent)
Currently, `deploy_agent.py` is configured for **Phase 1 testing**. It deploys a basic Agent using the `src/agent/system_prompt.txt` instructions and the model configuration from `config/{env}.yaml`, but **without** any custom Python tools or Azure AI Search Knowledge Bases attached. This ensures your basic authentication and CI/CD pipelines are fully operational first.

### Roadmap (Phase 2: Tools & Knowledge Base)
Once the base pipeline is verified, you can easily activate Phase 2:
1. Open `scripts/deploy_agent.py`.
2. Locate the blocks labeled `[COMMENTED OUT FOR PHASE 1]`.
3. Uncomment the `ToolSet` initialization, the `FunctionTool` logic, and the `AzureAISearchTool` code.
4. Uncomment `toolset=toolset` in the `create_agent` call.
5. Deploy to instantly attach custom capabilities to your agent.

### How Components Connect

1. **Agent Definition (Source of Truth):**
   The agent's identity (`src/agent/system_prompt.txt`), capabilities (`src/tools/`), and model configurations are version-controlled. 
2. **Environment Isolation (`config/`):**
   Configurations define environment-specific bindings. For example, the Dev config binds the agent to a Dev database tool, while Prod binds to a read-only Prod replica.
3. **Model Flexibility:**
   The AI model is parameterized in the `config/{env}.yaml` files. You can easily switch models (e.g., from `gpt-4o-mini` to a Llama 3 deployment) by simply updating the `model_deployment_name`.
4. **Automated Deployment (`scripts/deploy_agent.py`):**
   The pipeline executes this script, which uses the modern `azure-ai-projects` SDK to upsert the agent.
5. **Data & Evaluation (`evals/`):**
   Before an agent reaches Production, it must pass a quantitative evaluation using Golden datasets.

## Project Structure

```text
📦 AIFoundry-DevOps-Template
 ┣ 📂 .github/workflows      # GitHub CI/CD orchestration
 ┣ 📂 azure-devops           # Azure DevOps pipeline YAML
 ┣ 📂 config                 # Environment-specific variables
 ┣ 📂 evals                  # Evaluation scripts and golden datasets
 ┣ 📂 scripts                # Deployment and lifecycle scripts
 ┣ 📂 src
 ┃ ┣ 📂 agent                # System prompts and agent metadata
 ┃ ┗ 📂 tools                # Python tool definitions
 ┣ 📜 PREREQUISITES.md       # Azure setup instructions
 ┗ 📜 requirements.txt       # Python dependencies
```