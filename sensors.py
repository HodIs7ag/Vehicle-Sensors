import time
import random

# current time in the format of "2024-05-23 14:00:00"
format_string = "%Y-%m-%d %H:%M:%S"

# Initial location
current_latitude = 0.0
current_longitude = 0.0

def get_time():
    return time.strftime(format_string, time.localtime(time.time()))

def generate_location_data(vehicle_id):
    global current_latitude, current_longitude
    data = {
        "vehicle_id": vehicle_id,
        "timestamp": get_time(),
        "location": {
            "latitude": round(current_latitude, 6),
            "longitude": round(current_longitude, 6)
        }
    }
    return data

def update_location(direction):
    global current_latitude, current_longitude
    step = 0.01
    if direction == 'Up':
        current_latitude = min(90, current_latitude + step)
    elif direction == 'Down':
        current_latitude = max(-90, current_latitude - step)
    elif direction == 'Left':
        current_longitude = max(-180, current_longitude - step)
    elif direction == 'Right':
        current_longitude = min(180, current_longitude + step)

def generate_speed_data(vehicle_id):
    data = {
        "vehicle_id": vehicle_id,
        "timestamp": get_time(),
        "speed": round(random.uniform(0, 120), 2)  # Speed in km/h
    }
    return data

def generate_condition_data(vehicle_id):
    data = {
        "vehicle_id": vehicle_id,
        "timestamp": get_time(),
        "engine_temperature": round(random.uniform(0, 800), 2),  # Temperature in Celsius
        "fuel_level": round(random.uniform(0, 100), 2)     # Fuel level in percentage
    }
    return data

if __name__ == '__main__':
    print(generate_condition_data(1))
    print(generate_location_data(1))
    print(generate_speed_data(1))
