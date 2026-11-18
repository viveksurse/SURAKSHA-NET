def classify_risk(water_distance_cm, rainfall_percent):
    # Prototype rules only; not official or validated emergency thresholds.
    water, rain = float(water_distance_cm), float(rainfall_percent)
    if water <= 20 or rain >= 80:
        return "CRITICAL"
    if water <= 40 or rain >= 60:
        return "WARNING"
    return "NORMAL"
