import os
import re
import requests

from pypdf import PdfReader


FOLDER = "data/invoices"


def list_files():
    files = os.listdir(FOLDER)

    pdf_files = []

    for file in files:
        if file.endswith(".pdf"):
            pdf_files.append(file)

    return pdf_files


def read_pdf(filename):
    path = os.path.join(FOLDER, filename)

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


def extract_invoice_details(text):
    invoice_number = re.search(
        r"Invoice Number:\s*(.*)", text
    ).group(1)

    invoice_date = re.search(
        r"Invoice Date:\s*(.*)", text
    ).group(1)

    due_date = re.search(
        r"Due Date:\s*(.*)", text
    ).group(1)

    amount_match = re.search(
        r"Total:\s*(INR)\s*([\d.]+)", text
    )

    currency = amount_match.group(1)
    amount = amount_match.group(2)

    return {
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "due_date": due_date,
        "amount": amount,
        "currency": currency
    }


def get_invoice_details(filename):
    text = read_pdf(filename)

    details = extract_invoice_details(text)

    return details


def submit_invoice(invoice):
    try:
        response = requests.post(
            "http://127.0.0.1:5000/invoices",
            json=invoice,
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as e:
        print("Submission failed. Retrying...")

        try:
            response = requests.post(
                "http://127.0.0.1:5000/invoices",
                json=invoice,
                timeout=5
            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException:
            return {
                "success": False,
                "error": str(e)
            }


def get_submitted_invoices():
    response = requests.get(
        "http://127.0.0.1:5000/invoices"
    )

    return response.json()


def verify_invoice(invoice_number):
    invoices = get_submitted_invoices()

    for invoice in invoices:

        if invoice.get("invoice_number") == invoice_number:

            return {
                "verified": True,
                "invoice": invoice
            }

    return {
        "verified": False,
        "message": "Invoice not found"
    }