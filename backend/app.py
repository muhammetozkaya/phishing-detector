import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import analyze_url

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for the frontend to access API

LOGS_FILE = os.path.join(os.path.dirname(__file__), "logs.json")

def log_result(result):
    """Saves the analysis result into a JSON log file."""
    logs = []
    if os.path.exists(LOGS_FILE):
        try:
            with open(LOGS_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []  # If file is corrupted or empty

    logs.append(result)

    with open(LOGS_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=4)


@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Geçerli bir JSON gövdesinde 'url' alanı bulunamadı."}), 400

    url = data.get("url", "").strip()
    if not url:
        return jsonify({"error": "URL boş olamaz."}), 400

    # Analyze URL
    result = analyze_url(url)
    
    # Save to JSON log
    log_result(result)

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
