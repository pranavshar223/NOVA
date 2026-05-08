from flask import Flask, request, jsonify
from assistant import Assistant
from config import Config

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "NOVA Flask backend is running"
    }), 200


@app.route("/chat", methods=["POST"])
def chat():
    try:
        if not request.is_json:
            return jsonify({
                "status": "error",
                "reply": "Request must be JSON."
            }), 400

        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "status": "error",
                "reply": "No JSON data received."
            }), 400

        user_message = str(data.get("message", "")).strip()

        if not user_message:
            return jsonify({
                "status": "error",
                "reply": "Message is required."
            }), 400

        reply = Assistant.process_message(user_message)

        return jsonify({
            "status": "success",
            "reply": reply
        }), 200

    except Exception as e:
        print(f"[ERROR] /chat failed: {e}")
        return jsonify({
            "status": "error",
            "reply": "Internal server error."
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "reply": "Route not found."
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "status": "error",
        "reply": "Method not allowed."
    }), 405


if __name__ == "__main__":
    app.run(
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        debug=Config.FLASK_DEBUG
    )