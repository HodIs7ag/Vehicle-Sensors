# Vehicle Sensors


This project simulates the movement of a vehicle using a graphical interface (GUI) and generates vehicle data such as location, speed, and condition. The generated data is then published to an MQTT broker. Another script subscribes to the MQTT topics and stores the data into MongoDB, MySQL, and Neo4j databases.


## Components

1. **Sensors**: `sensors.py `Functioins to Generate data for vehicle location, speed, and condition.
2. **Publisher**: `publisher.py` This file creates the GUI and publishes the generated data to the MQTT broker
3. **Subscriber**: `subscriber.py` Subscribes to MQTT topics, receives data, and stores it in databases.
4. **Databases**:
   - MySQL: Stores vehicle speed data.
   - Neo4j: Stores vehicle location data.
   - MongoDB: Stores vehicle condition, speed and location data.

## Installation and Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/DatabaseUnime/MahmoudAbdelrahim
    cd MahmoudAbdelrahim
    ```

2. Set up a Python virtual environment and install dependencies:

    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Set up databases using Docker:
   
   Ensure Docker is installed on your system. Use the following Docker commands to run the MongoDB, MySQL, and Neo4j containers.

    ```bash
    # MongoDB
    docker run -d --name mongodb -p 27017:27017 mongo

    # MySQL
    docker run -d -p 3306:3306 --name mysqldb -e MYSQL_ROOT_PASSWORD=123456 -e MYSQL_DATABASE=vehicles_data mysql

    # Neo4j
    docker run -d --name neo4jdb -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/12345678 neo4j
    ```


4. Run the system:
   - Start the MQTT subscriber by running `subscriber.py`:

    ```bash
    python subscriber.py
    ```

   - Start the MQTT publisher by running `publisher.py`:

    ```bash
    python publisher.py
    ```
   - Insert vehicle_id
   - use arrow keys to move the car on the screen

