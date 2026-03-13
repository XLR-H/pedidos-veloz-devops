from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "estoque"}), 200


@app.route("/reservar", methods=["POST"])
def reservar():
    data = request.get_json()

    item = data.get("item")
    quantidade = data.get("quantidade")

    if not item or quantidade is None:
        return jsonify({"erro": "Campos item e quantidade são obrigatórios"}), 400

    return jsonify({
        "item": item,
        "quantidade": quantidade,
        "status_estoque": "reservado"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
