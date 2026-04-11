# AI Foundry DevOps Template

An enterprise-grade, end-to-end CI/CD template for managing and promoting Azure AI Foundry agents across isolated environments (Dev, QA, Prod).

---

## 🚀 Quick Start for Beginners (Local Testing)

If you are new to this and just want to see how the automation works **without** needing an Azure account or spending any money, follow these steps:

### Step 1: Open Your Terminal
Open PowerShell or your preferred terminal and navigate to this folder:
```bash
cd G:\AI\AIFoundry-DevOps-Template
```

### Step 2: Create a Virtual Environment (Recommended)
A virtual environment keeps your Python packages isolated so they don't mess up your global system.
```bash
python -m venv venv
```
Activate it:
* **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`
* **Windows (Command Prompt):** `.\venv\Scripts\activate.bat`
* **Mac/Linux:** `source venv/bin/activate`

### Step 3: Install Dependencies
Install the required Python packages (we created a `requirements.txt` for this):
```bash
pip install -r requirements.txt
```

### Step 4: Run a "Dry Run" Deployment
Let's pretend to deploy the agent to the Development environment. The `--dry-run` flag tells the script to simulate the process without actually trying to connect to Azure:
```bash
python scripts/deploy_agent.py --env dev --dry-run
```
*You should see a success message showing the agent's configuration!*

### Step 5: Run a "Dry Run" Evaluation
Before an agent goes to Production, it must pass a test. Let's simulate grading the agent using our QA dataset:
```bash
python evals/run_evals.py --env qa --threshold 0.85 --dry-run
```
*You should see the system simulate grading the agent, passing the 85% threshold, and allowing the promotion!*

---

## Architectural Vision

As AI moves from prototype to production, building agents manually in a UI falls apart. This template enforces an **SDK-First, Infrastructure-as-Code (IaC) approach**.

### How Components Connect

1. **Agent Definition (Source of Truth):**
   The agent's identity (`src/agent/system_prompt.txt`), capabilities (`src/tools/`), and model configurations are version-controlled. 
2. **Environment Isolation (`config/`):**
   Configurations define environment-specific bindings. For example, the Dev config binds the agent to a Dev database tool, while Prod binds to a read-only Prod replica.
3. **Automated Deployment (`scripts/deploy_agent.py`):**
   The pipeline executes this script, which uses the `azure-ai-projects` SDK to upsert the agent into the respective Azure AI Project based on the active environment configuration.
4. **Data & Evaluation (`evals/`):**
   Before an agent reaches Production, it must pass a quantitative evaluation using Golden datasets (`evals/datasets/`).

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
