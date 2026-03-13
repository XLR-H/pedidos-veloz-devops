from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

PEDIDOS_URL = os.getenv("PEDIDOS_URL", "http://pedidos:5000")
PAGAMENTOS_URL = os.getenv("PAGAMENTOS_URL", "http://pagamentos:5001")
ESTOQUE_URL = os.getenv("ESTOQUE_URL", "http://estoque:5002")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "gateway"}), 200


@app.route("/pedido-completo", methods=["POST"])
def pedido_completo():
    data = request.get_json()

    cliente = data.get("cliente")
    item = data.get("item")
    quantidade = data.get("quantidade")
    valor = data.get("valor")

    if not cliente or not item or quantidade is None or valor is None:
        return jsonify({
            "erro": "Campos cliente, item, quantidade e valor são obrigatórios"
        }), 400

    estoque_response = requests.post(
        f"{ESTOQUE_URL}/reservar",
        json={"item": item, "quantidade": quantidade},
        timeout=5
    )

    if estoque_response.status_code != 200:
        return jsonify({
            "erro": "Falha ao reservar item no estoque",
            "detalhes": estoque_response.json()
        }), 502

    pedido_response = requests.post(
        f"{PEDIDOS_URL}/pedido",
        json={"cliente": cliente, "item": item, "quantidade": quantidade},
        timeout=5
    )

    if pedido_response.status_code != 201:
        return jsonify({
            "erro": "Falha ao criar pedido",
            "detalhes": pedido_response.json()
        }), 502

    pedido_data = pedido_response.json()

    pagamento_response = requests.post(
        f"{PAGAMENTOS_URL}/pagar",
        json={"pedido_id": pedido_data["id"], "valor": valor},
        timeout=5
    )

    if pagamento_response.status_code != 200:
        return jsonify({
            "erro": "Falha ao processar pagamento",
            "detalhes": pagamento_response.json()
        }), 502

    return jsonify({
        "pedido": pedido_data,
        "estoque": estoque_response.json(),
        "pagamento": pagamento_response.json(),
        "status": "pedido_processado_com_sucesso"
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
