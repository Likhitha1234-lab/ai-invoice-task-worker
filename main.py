from agent.agent import run_agent


run_agent(
    "Find the latest invoice from Acme Corporation. "
    "Use the invoice date inside the PDFs to determine which invoice is latest. "
    "Submit the latest invoice to the company invoice system. "
    "After submitting it, verify that the invoice was actually stored. "
    "Then give me a short summary of what you did."
)