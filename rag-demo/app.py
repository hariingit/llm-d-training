from flask import Flask, jsonify, request, send_from_directory

import rag_core

app = Flask(__name__, static_folder="static")


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/ask", methods=["POST"])
def api_ask():
    question = (request.get_json(force=True) or {}).get("question", "").strip()
    if not question:
        return jsonify({"error": "question is required"}), 400
    try:
        result = rag_core.ask(question)
        return jsonify(result)
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": str(exc)}), 502


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=False)
