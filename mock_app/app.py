from flask import Flask, request, jsonify

app = Flask(__name__)

invoices = []


@app.route("/invoices", methods=["POST"])
def add_invoice():
    invoice = request.json

    invoices.append(invoice)

    return jsonify({
        "message": "Invoice added successfully",
        "invoice": invoice
    })


@app.route("/invoices", methods=["GET"])
def get_invoices():
    return jsonify(invoices)


if __name__ == "__main__":
    app.run(port=5000)