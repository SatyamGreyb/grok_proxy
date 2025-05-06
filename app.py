from flask import Flask, request, jsonify, send_file
import requests
import os
import logging

app = Flask(__name__)

# Load API key from Render environment variable
GROK_API_KEY = os.environ.get("GROK_API_KEY")

# Enable logs
logging.basicConfig(level=logging.INFO)

@app.route("/")
def home():
    return "Grok Proxy API is live!"

@app.route("/grok", methods=["POST"])
def call_grok():
    data = request.json
    user_prompt = data.get("prompt", "")
    logging.info(f"[Prompt Received] {user_prompt}")

    payload = {
        "model": "grok-3-latest",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False,
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        logging.info(f"[Grok Reply] {reply}")
        return jsonify({"reply": reply})
    except Exception as e:
        logging.error(f"[ERROR] {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/openapi.json")
def serve_openapi():
    return send_file("openapi.json", mimetype="application/json")
