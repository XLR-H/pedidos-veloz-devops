from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "pagamentos"}), 200


@app.route("/pagar", methods=["POST"])
def pagar():
    data = request.get_json()

    pedido_id = data.get("pedido_id")
    valor = data.get("valor")

    if not pedido_id or valor is None:
        return jsonify({"erro": "Campos pedido_id e valor são obrigatórios"}), 400

    return jsonify({
        "pedido_id": pedido_id,
        "valor": valor,
        "status_pagamento": "aprovado"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
