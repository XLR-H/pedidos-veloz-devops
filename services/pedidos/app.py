from flask import Flask, request, jsonify
import os
import time
import psycopg2

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "pedidosdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def init_db():
    max_retries = 10
    retry_interval = 3

    for attempt in range(1, max_retries + 1):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS pedidos (
                    id SERIAL PRIMARY KEY,
                    cliente VARCHAR(100) NOT NULL,
                    item VARCHAR(100) NOT NULL,
                    quantidade INT NOT NULL
                );
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("Banco inicializado com sucesso.")
            return
        except psycopg2.OperationalError as e:
            print(f"Tentativa {attempt}/{max_retries}: banco ainda não está pronto. Erro: {e}")
            time.sleep(retry_interval)

    raise Exception("Não foi possível conectar ao banco após várias tentativas.")



@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "pedidos"}), 200


@app.route("/pedido", methods=["POST"])
def criar_pedido():
    data = request.get_json()

    cliente = data.get("cliente")
    item = data.get("item")
    quantidade = data.get("quantidade")

    if not cliente or not item or not quantidade:
        return jsonify({"erro": "Campos cliente, item e quantidade são obrigatórios"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO pedidos (cliente, item, quantidade) VALUES (%s, %s, %s) RETURNING id;",
        (cliente, item, quantidade)
    )
    pedido_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "id": pedido_id,
        "cliente": cliente,
        "item": item,
        "quantidade": quantidade
    }), 201


@app.route("/pedido/<int:pedido_id>", methods=["GET"])
def consultar_pedido(pedido_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, cliente, item, quantidade FROM pedidos WHERE id = %s;",
        (pedido_id,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"erro": "Pedido não encontrado"}), 404

    return jsonify({
        "id": row[0],
        "cliente": row[1],
        "item": row[2],
        "quantidade": row[3]
    }), 200


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
