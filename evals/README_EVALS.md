# Evaluation Strategy & Datasets

To safely promote an AI agent to production, we must quantitatively prove that its quality hasn't degraded. This directory contains the scaffolding for Automated Batch Evaluations.

## How it works
1. **Golden Datasets (`datasets/`):** JSONL files containing a representative sample of user queries and the expected "ideal" responses or context.
2. **Evaluation Script (`run_evals.py`):** Connects to the newly deployed QA agent, feeds it the golden queries, and records the responses.
3. **Azure AI Evaluators:** The script uses Azure's built-in evaluator models (like Groundedness, Coherence, Relevance) to score the agent's responses.
4. **Pipeline Quality Gate:** If the aggregate score falls below a threshold (e.g., 85%), the CI/CD pipeline fails, preventing deployment to Production.

## Best Practices
- **Data Freshness:** Regularly update the golden dataset with edge-cases discovered in Production.
- **Red Teaming:** Include a dataset specifically for adversarial inputs (jailbreak attempts) to evaluate the safety filters.
