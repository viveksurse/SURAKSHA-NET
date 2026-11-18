# SURAKSHA-NET complete starter

## Run
Open a terminal in this folder:
```powershell
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py app.py
```
Open http://127.0.0.1:5000. SQLite database is created automatically.
Use the three demo buttons to test the interface, chart and alert history.

## Wokwi wiring
DHT22: VCC->3V3, GND->GND, DATA->GPIO15.
HC-SR04: VCC->5V, GND->GND, TRIG->GPIO5, ECHO->GPIO18.
Potentiometer: outer pins->3V3/GND, middle->GPIO34 (rainfall demonstration input).
For physical ESP32 hardware, never connect a 5V HC-SR04 ECHO directly to an ESP32 GPIO; use a voltage divider or level shifter.

## Connect Wokwi
Open `wokwi/sketch.ino` in your ESP32 project, install the listed libraries, then replace SERVER_URL with a public HTTPS tunnel URL ending in `/api/sensor`. Set the same API key in the Flask environment and sketch. PowerShell:
```powershell
$env:SURAKSHA_API_KEY="replace-with-a-long-random-key"
py app.py
```
A remote Wokwi simulator cannot reach your laptop using localhost/127.0.0.1. You need a secure public HTTPS tunnel or hosted server. Do not expose Flask debug mode directly to the internet.

## Safety and accuracy
The water/rain thresholds are illustrative software-test values only, not scientifically validated or official disaster-warning thresholds. The map stations and coordinates are demonstration data. Do not use this academic prototype for real emergency decisions. Leaflet tiles and Chart.js load from CDNs and require browser internet access.
