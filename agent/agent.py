import json

from openai import OpenAI
from dotenv import load_dotenv

from agent.tools import (
    list_files,
    get_invoice_details,
    submit_invoice,
    verify_invoice
)


load_dotenv()

client = OpenAI()


tools = [
    {
        "type": "function",
        "name": "list_files",
        "description": "List all invoice PDF files available in the invoice folder.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },

    {
        "type": "function",
        "name": "get_invoice_details",
        "description": "Get invoice number, date, due date, amount and currency from an invoice PDF.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The invoice PDF filename."
                }
            },
            "required": ["filename"]
        }
    },

    {
        "type": "function",
        "name": "submit_invoice",
        "description": "Submit an invoice to the company's internal invoice system.",
        "parameters": {
            "type": "object",
            "properties": {
                "invoice": {
                    "type": "object",
                    "description": "The invoice information to submit."
                }
            },
            "required": ["invoice"]
        }
    },

    {
        "type": "function",
        "name": "verify_invoice",
        "description": "Verify whether a specific invoice number exists in the company's invoice system.",
        "parameters": {
            "type": "object",
            "properties": {
                "invoice_number": {
                    "type": "string",
                    "description": "The invoice number to verify."
                }
            },
            "required": ["invoice_number"]
        }
    }
]


def run_agent(task):

    response = client.responses.create(
        model="gpt-6-luna",
        input=task,
        tools=tools
    )

    while True:

        tool_outputs = []

        for item in response.output:

            if item.type != "function_call":
                continue

            if item.name == "list_files":

                result = list_files()

                print("\nTool used: list_files")
                print("Result:", result)

            elif item.name == "get_invoice_details":

                arguments = json.loads(item.arguments)
                filename = arguments["filename"]

                result = get_invoice_details(filename)

                print("\nTool used: get_invoice_details")
                print("Reading:", filename)
                print("Details:", result)

            elif item.name == "submit_invoice":

                arguments = json.loads(item.arguments)
                invoice = arguments["invoice"]

                result = submit_invoice(invoice)

                print("\nTool used: submit_invoice")
                print("Result:", result)

            elif item.name == "verify_invoice":

                arguments = json.loads(item.arguments)
                invoice_number = arguments["invoice_number"]

                result = verify_invoice(invoice_number)

                print("\nTool used: verify_invoice")
                print("Checking:", invoice_number)
                print("Result:", result)

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": [
                    {
                        "type": "input_text",
                        "text": str(result)
                    }
                ]
            })

        if not tool_outputs:
            break

        response = client.responses.create(
            model="gpt-6-luna",
            input=tool_outputs,
            previous_response_id=response.id,
            tools=tools
        )

    print("\nAI:", response.output_text)

    return response