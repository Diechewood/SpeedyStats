# Utilities/UtilityFunctions.py
import json
import jsonschema
from datetime import datetime
import pytz
from haversine import haversine

class AppError(Exception):
    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

def validate_json(schema, json_data):
    try:
        jsonschema.validate(instance=json_data, schema=schema)
    except jsonschema.ValidationError as e:
        raise AppError(f"Invalid JSON data: {e}", status_code=400)

def calculate_speed(gps_data):
    if len(gps_data) < 2:
        raise AppError("Insufficient GPS data for speed calculation.", 400)

    total_distance = 0
    total_time = 0
    for i in range(1, len(gps_data)):
        point1, point2 = gps_data[i - 1], gps_data[i]
        
        # Validate each point's data
        if not all(isinstance(x, (int, float)) for x in point1 + point2):
            raise AppError("GPS data contains invalid values.", 400)

        distance = haversine((point1[0], point1[1]), (point2[0], point2[1]))
        time_diff = point2[2] - point1[2]  # Assuming timestamp is in seconds

        # Check for realistic time and distance values
        if time_diff <= 0 or distance < 0:
            raise AppError("GPS data contains unrealistic time or distance values.", 400)

        total_distance += distance
        total_time += time_diff

    if total_time > 0:
        speed = (total_distance / total_time) * 3600  # Speed in km/h
        return speed
    else:
        return 0

def format_timestamp(timestamp):
    try:
        formatted_time = datetime.fromtimestamp(timestamp, pytz.UTC)
        return formatted_time.strftime('%Y-%m-%d %H:%M:%S %Z')
    except ValueError:
        raise AppError("Invalid timestamp value.", 400)

gps_data_schema = {
    "type": "object",
    "properties": {
        "latitude": {"type": "number"},
        "longitude": {"type": "number"},
        "timestamp": {"type": "number"}
    },
    "required": ["latitude", "longitude", "timestamp"]
}

def parse_gps_data(gps_data):
    validate_json(gps_data_schema, gps_data)
    return {
        "latitude": gps_data["latitude"],
        "longitude": gps_data["longitude"],
        "timestamp": gps_data["timestamp"]
    }
