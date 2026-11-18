import sqlite3
from datetime import datetime
from backend.config import DB_PATH

def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with db() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS readings(
        id INTEGER PRIMARY KEY, station_id TEXT, station_name TEXT,
        latitude REAL, longitude REAL, temperature REAL, humidity REAL,
        water_distance_cm REAL, rainfall_percent REAL, risk TEXT,
        source TEXT, timestamp TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS alerts(
        id INTEGER PRIMARY KEY, station_id TEXT, station_name TEXT,
        risk TEXT, message TEXT, timestamp TEXT, acknowledged INTEGER DEFAULT 0)""")

def save_reading(x):
    x = dict(x); x["timestamp"] = datetime.now().astimezone().isoformat(timespec="seconds")
    with db() as c:
        c.execute("""INSERT INTO readings(station_id,station_name,latitude,longitude,
        temperature,humidity,water_distance_cm,rainfall_percent,risk,source,timestamp)
        VALUES(:station_id,:station_name,:latitude,:longitude,:temperature,:humidity,
        :water_distance_cm,:rainfall_percent,:risk,:source,:timestamp)""", x)

def latest_readings():
    with db() as c:
        rows = c.execute("""SELECT r.* FROM readings r JOIN
        (SELECT station_id,MAX(id) mid FROM readings GROUP BY station_id) x
        ON r.id=x.mid ORDER BY r.id DESC""").fetchall()
    return [dict(r) for r in rows]

def history(station_id, limit=30):
    with db() as c:
        rows = c.execute("SELECT * FROM readings WHERE station_id=? ORDER BY id DESC LIMIT ?",
                         (station_id, limit)).fetchall()
    return [dict(r) for r in reversed(rows)]

def add_alert(x):
    msg = f'{x["station_name"]}: {x["risk"]} detected; water distance {x["water_distance_cm"]:.1f} cm, rainfall input {x["rainfall_percent"]:.1f}%.'
    with db() as c:
        c.execute("INSERT INTO alerts(station_id,station_name,risk,message,timestamp) VALUES(?,?,?,?,?)",
        (x["station_id"],x["station_name"],x["risk"],msg,datetime.now().astimezone().isoformat(timespec="seconds")))

def alerts(limit=50):
    with db() as c:
        rows = c.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT ?",(limit,)).fetchall()
    return [dict(r) for r in rows]

def acknowledge(alert_id):
    with db() as c:
        cur = c.execute("UPDATE alerts SET acknowledged=1 WHERE id=?",(alert_id,))
    return cur.rowcount > 0
