from flask import Flask, jsonify
from flask_cors import CORS
from garminconnect import Garmin
import os
from datetime import date

app = Flask(__name__)
CORS(app)

# Login einmal beim Start
client = None

def get_client():
    global client
    if client is None:
        email = os.environ.get("GARMIN_EMAIL")
        password = os.environ.get("GARMIN_PASSWORD")
        client = Garmin(email, password)
        client.login()
    return client

@app.route("/")
def index():
    return jsonify({"status": "Athlete OS Garmin API läuft!"})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/activities")
def activities():
    try:
        data = get_client().get_activities(0, 30)
        return jsonify(data)
    except Exception as e:
        global client
        client = None
        return jsonify({"error": str(e)}), 500

@app.route("/sleep")
def sleep():
    try:
        today = date.today().isoformat()
        data = get_client().get_sleep_data(today)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/hrv")
def hrv():
    try:
        today = date.today().isoformat()
        data = get_client().get_hrv_data(today)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/stats")
def stats():
    try:
        today = date.today().isoformat()
        data = get_client().get_stats(today)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
