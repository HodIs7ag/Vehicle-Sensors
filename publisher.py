import turtle
import paho.mqtt.client as mqtt
import json
from sensors import generate_location_data, generate_speed_data, generate_condition_data, update_location

# MQTT Broker credentials
broker = 'f49c06be6ca74b46a7b2ef18270fc1d7.s1.eu.hivemq.cloud'
port = 8883
username = 'TestUser'
password = 'Testing1234'

# MQTT topics
TOPIC_LOCATION = 'vehicles/location'
TOPIC_SPEED = 'vehicles/speed'
TOPIC_CONDITION = 'vehicles/condition'

vehicle_id = int(input("Enter the vehicle ID: "))

# Set up the screen
screen = turtle.Screen()
screen.title("Vehicle Data Generator")
screen.setup(width=800, height=600)

# Create a turtle to represent the car
car = turtle.Turtle()
car.shape("square")
car.color("blue")
car.penup()
car.speed(1)

# Create text turtle for displaying data
data_turtle = turtle.Turtle()
data_turtle.hideturtle()
data_turtle.penup()
data_turtle.goto(-390, 260)
data_turtle.write("Use arrow keys to move the car and generate data", align="left", font=("Arial", 12, "normal"))

# Put the pen down to highlight the path
car.pendown()

# MQTT setup
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print("Connection failed")

client = mqtt.Client()
client.username_pw_set(username, password)
client.on_connect = on_connect
client.tls_set()  # Enable TLS

client.connect(broker, port, 60)
client.loop_start()

def on_key_press(direction):
    update_location(direction)
    location_data = generate_location_data(vehicle_id)
    speed_data = generate_speed_data(vehicle_id)
    condition_data = generate_condition_data(vehicle_id)
    
    # Publish data to MQTT topics
    client.publish(TOPIC_LOCATION, json.dumps(location_data))
    print(f"Published to {TOPIC_LOCATION}: {location_data}")
    client.publish(TOPIC_SPEED, json.dumps(speed_data))
    print(f"Published to {TOPIC_SPEED}: {speed_data}")
    client.publish(TOPIC_CONDITION, json.dumps(condition_data))
    print(f"Published to {TOPIC_CONDITION}: {condition_data}")
    
    # Move the car
    if direction == 'Up':
        car.sety(car.ycor() + 10)
    elif direction == 'Down':
        car.sety(car.ycor() - 10)
    elif direction == 'Left':
        car.setx(car.xcor() - 10)
    elif direction == 'Right':
        car.setx(car.xcor() + 10)
    
    # Update data display
    data_turtle.clear()
    data_turtle.write(
        f"Location Data: {location_data}\nSpeed Data: {speed_data}\nCondition Data: {condition_data}",
        align="left",
        font=("Arial", 12, "normal")
    )

# Bind arrow keys to the on_key_press function
screen.listen()
screen.onkey(lambda: on_key_press('Up'), 'Up')
screen.onkey(lambda: on_key_press('Down'), 'Down')
screen.onkey(lambda: on_key_press('Left'), 'Left')
screen.onkey(lambda: on_key_press('Right'), 'Right')

# Start the main loop
turtle.mainloop()

client.loop_stop()
client.disconnect()
