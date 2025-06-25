from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

# Stores blockchain messages
blockchain = []

# Stores registered users and their public keys (username -> PEM string)
public_keys = {}

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    public_key = data.get("public_key")

    if not username or not public_key:
        return jsonify({"error": "Missing username or public key"}), 400

    public_keys[username] = public_key
    return jsonify({"message": f"User '{username}' registered successfully."}), 200

@app.route("/get_public_key/<username>", methods=["GET"])
def get_public_key(username):
    key = public_keys.get(username)
    if not key:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"public_key": key}), 200

@app.route("/send", methods=["POST"])
def send_message():
    data = request.get_json()
    sender = data.get("sender")
    recipient = data.get("recipient")
    encrypted_message = data.get("encrypted_message")

    if not sender or not recipient or not encrypted_message:
        return jsonify({"error": "Missing sender, recipient, or message"}), 400

    block = {
        "sender": sender,
        "recipient": recipient,
        "encrypted_message": encrypted_message,
        "timestamp": str(datetime.datetime.now())
    }
    blockchain.append(block)

    return jsonify(blockchain), 200

@app.route("/chain", methods=["GET"])
def get_chain():
    return jsonify(blockchain), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
