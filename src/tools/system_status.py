from typing import Dict

# -------------------------------------------------------------------------
# TOOL DEFINITION
# In Azure AI Foundry, tools can be defined as standard Python functions.
# The SDK automatically parses the docstring and type hints to create the 
# OpenAPI schema that the LLM uses to understand when/how to call it.
# -------------------------------------------------------------------------

def check_system_status(service_name: str) -> str:
    """
    Retrieves the current health status of a specified internal service.
    
    :param service_name: The name of the service to check (e.g., 'database', 'payment_gateway', 'frontend').
    :return: A string describing the current status of the service.
    """
    # MOCK IMPLEMENTATION: 
    # For testing the pipeline and agent without requiring actual backend services.
    # In a real scenario, this would make HTTP requests or database queries based 
    # on the environment variables bound in the config/{env}.yaml files.
    
    mock_statuses = {
        "database": "Operational - 12ms latency",
        "payment_gateway": "Degraded - High error rate on Stripe API",
        "frontend": "Operational - 100% uptime",
    }
    
    # Return the simulated status or a fallback message
    return mock_statuses.get(service_name.lower(), f"Service '{service_name}' not found or unrecognized.")
