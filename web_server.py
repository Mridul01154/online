from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import datetime

app = Flask(__name__)
CORS(app)

# === Blockchain Logic ===
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = self.create_block("System", "Genesis Block", "0")
        self.chain.append(genesis)

    def create_block(self, sender, message, prev_hash):
        index = len(self.chain)
        timestamp = str(datetime.datetime.now())
        block_data = {
            'index': index,
            'timestamp': timestamp,
            'sender': sender,
            'message': message,  # already encrypted
            'previous_hash': prev_hash
        }
        block_data['hash'] = self.calculate_hash(block_data)
        return block_data

    def calculate_hash(self, data):
        block_str = f"{data['index']}{data['timestamp']}{data['sender']}{data['message']}{data['previous_hash']}"
        return hashlib.sha256(block_str.encode()).hexdigest()

    def add_block(self, sender, message):
        last_hash = self.chain[-1]['hash']
        new_block = self.create_block(sender, message, last_hash)
        self.chain.append(new_block)

    def get_chain(self):
        return self.chain

blockchain = Blockchain()

# === API Routes ===

@app.route("/send", methods=["POST"])
def send_message():
    data = request.get_json()
    sender = data.get("sender")
    message = data.get("message")  # already encrypted from client

    if not sender or not message:
        return jsonify({"error": "Missing sender or message"}), 400

    try:
        blockchain.add_block(sender, message)
        return jsonify(blockchain.get_chain()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chain", methods=["GET"])
def get_chain():
    return jsonify(blockchain.get_chain()), 200

# === Entry Point ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
