def validate_payload(p):
    fields = ("temperature", "humidity", "water_distance_cm", "rainfall_percent")
    for field in fields:
        if field not in p:
            return False, f"Missing field: {field}"
        try:
            value = float(p[field])
        except (TypeError, ValueError):
            return False, f"{field} must be numeric"
        if not -50 <= value <= 150:
            return False, f"{field} is outside accepted prototype range"
    if not 0 <= float(p["humidity"]) <= 100:
        return False, "humidity must be between 0 and 100"
    if not 0 <= float(p["rainfall_percent"]) <= 100:
        return False, "rainfall_percent must be between 0 and 100"
    if float(p["water_distance_cm"]) < 0:
        return False, "water_distance_cm cannot be negative"
    return True, "OK"
