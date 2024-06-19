import paho.mqtt.client as mqtt
from pymongo import MongoClient
import mysql.connector
from neo4j import GraphDatabase
import json

# Database connections
mongo_conn = MongoClient("mongodb://localhost:27017/")
print("Connected to MongoDB")

mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="vehicles_data")
print("Connected to MySQL")

neo4j_conn = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))
print("Connected to Neo4j")



# MQTT Broker credentials
broker = 'f49c06be6ca74b46a7b2ef18270fc1d7.s1.eu.hivemq.cloud'
port = 8883
username = 'Hodis7ag'
password = 'Fatima1967'

# MQTT topic
TOPIC_LOCATION = 'vehicles/location'
TOPIC_SPEED = 'vehicles/speed'
TOPIC_CONDITION = 'vehicles/condition'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe([(TOPIC_LOCATION, 0), (TOPIC_SPEED, 0), (TOPIC_CONDITION, 0)])
    else:
        print("Connection failed")

# function to insert data into MySQL
cursor = mysql_conn.cursor()
def mysql_insert(cursor,data):
    # create table if not exists
    cursor.execute("CREATE TABLE IF NOT EXISTS speeds(id INT AUTO_INCREMENT PRIMARY KEY, vehicle_id INT, timestamp VARCHAR(50), speed FLOAT)")
    # insert data
    cursor.execute("INSERT INTO speeds (vehicle_id, timestamp, speed) VALUES (%s, %s, %s)",
                   (data["vehicle_id"], data["timestamp"], data["speed"]))
    mysql_conn.commit()
    
# function to insert location data into Neo4j
neo4j_session = neo4j_conn.session()
def neo4j_insert(data):
    neo4j_session.run("MERGE (v:Vehicle {vehicle_id: $vehicle_id}) "
                      "MERGE (l:Location {latitude: $latitude, longitude: $longitude}) "
                      "MERGE (v)-[:LOCATCED_AT{timestamp: $time}]->(l)",
                      vehicle_id=data["vehicle_id"], latitude=data["location"]["latitude"], longitude=data["location"]["longitude"], time=data["timestamp"])
    
    
# function to insert all the data into MongoDB
def mongo_insert(collection,data):
    mongo_conn['vehicles_data'][collection].insert_one(data)
    


# function to handle incoming messages
def on_message(client, userdata, msg):
    print(f"Received message: {msg.topic} -> {msg.payload.decode()}")
    data = json.loads(msg.payload)
    if msg.topic == TOPIC_LOCATION:
        mongo_insert("locations",data)
        neo4j_insert(data)
    elif msg.topic == TOPIC_SPEED:
        mysql_insert(cursor,data)
        mongo_insert("speeds",data)
    elif msg.topic == TOPIC_CONDITION:
        mongo_insert("conditions",data)

# MQTT client
client = mqtt.Client()
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set()  # Enable TLS

client.connect(broker, port, 60)
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Subscriber stopped")
    client.disconnect()
    cursor.close()
    mysql_conn.close()
    neo4j_session.close()
    mongo_conn.close()

