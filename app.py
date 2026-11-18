from flask import Flask, jsonify, render_template, request
from backend.database import init_db, save_reading, latest_readings, history, alerts, add_alert, acknowledge
from backend.risk_engine import classify_risk
from backend.sensor_api import validate_payload
from backend.config import API_KEY

app = Flask(__name__)
init_db()

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/dashboard")
def dashboard_data():
    readings = latest_readings()
    return jsonify({"readings": readings, "alerts": alerts(10),
                    "mode": "LIVE" if readings and readings[0]["source"] == "esp32" else "DEMO"})

@app.get("/api/history")
def history_data():
    return jsonify(history(request.args.get("station_id", "demo-station")))

@app.post("/api/sensor")
def sensor_data():
    if request.headers.get("X-API-Key") != API_KEY:
        return jsonify(error="Unauthorized: check X-API-Key"), 401
    payload = request.get_json(silent=True) or {}
    ok, message = validate_payload(payload)
    if not ok:
        return jsonify(error=message), 400
    item = normalize(payload, "esp32")
    previous = history(item["station_id"], limit=1)
    save_reading(item)
    if not previous or previous[-1]["risk"] != item["risk"]:
        if item["risk"] != "NORMAL":
            add_alert(item)
    return jsonify(success=True, risk=item["risk"])

@app.post("/api/demo")
def demo():
    condition = str((request.get_json(silent=True) or {}).get("condition", "NORMAL")).upper()
    samples = {"NORMAL": (29.5, 60, 60, 20), "WARNING": (31.5, 75, 35, 65),
               "CRITICAL": (34, 85, 15, 90)}
    if condition not in samples:
        return jsonify(error="Use NORMAL, WARNING or CRITICAL"), 400
    t, h, w, r = samples[condition]
    item = normalize({"station_id":"demo-station", "station_name":"Demo Station",
        "latitude":19.076, "longitude":72.8777, "temperature":t, "humidity":h,
        "water_distance_cm":w, "rainfall_percent":r}, "demo")
    previous = history(item["station_id"], limit=1)
    save_reading(item)
    if (not previous or previous[-1]["risk"] != item["risk"]) and item["risk"] != "NORMAL":
        add_alert(item)
    return jsonify(success=True, risk=item["risk"])

@app.post("/api/alerts/<int:alert_id>/acknowledge")
def ack(alert_id):
    return jsonify(success=acknowledge(alert_id))

def normalize(p, source):
    water, rain = float(p["water_distance_cm"]), float(p["rainfall_percent"])
    return {"station_id":str(p.get("station_id","station-01")),
      "station_name":str(p.get("station_name","ESP32 Station")),
      "latitude":float(p.get("latitude",19.076)),
      "longitude":float(p.get("longitude",72.8777)),
      "temperature":float(p["temperature"]), "humidity":float(p["humidity"]),
      "water_distance_cm":water, "rainfall_percent":rain,
      "risk":classify_risk(water,rain), "source":source}

if __name__ == "__main__":
    # Local development only; do not expose Flask debug server publicly.
    app.run(host="0.0.0.0", port=5000, debug=True)
