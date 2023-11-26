import paho.mqtt.client as mqtt
import threading
import time
import json
import random

def on_publish(client, userdata, mid):
    print("Message published!")

def publish_message():
    # Set up MQTT connection for publishing
    client_pub = mqtt.Client()
    client_pub.on_publish = on_publish
    client_pub.connect("test.mosquitto.org", 1883)  # Change to your MQTT broker address

    def subscribe():
        # Set up MQTT connection for subscribing
        client_sub = mqtt.Client()
        client_sub.on_message = on_message
        client_sub.connect("test.mosquitto.org", 1883)  # Change to your MQTT broker address
        client_sub.subscribe("other_topic")  # Subscribe to another topic

        # Start a loop to listen for messages on the subscribed topic
        client_sub.loop_forever()

    # Start the subscribe function in a separate thread
    subscribe_thread = threading.Thread(target=subscribe)
    subscribe_thread.start()

    voltage = 6.0  # Starting voltage
    while voltage > 0:
        # Simulate battery discharging
        sleep_duration = random.uniform(0.5, 2.0)  # Random sleep duration between 0.5 and 2.0 seconds
        voltage_decrement = random.uniform(0.05, 0.2)  # Random voltage decrement between 0.05 and 0.2
        time.sleep(sleep_duration)
        voltage -= voltage_decrement

        # Create a dictionary with battery information
        battery_data = {
            "voltage": round(voltage, 2),
            "time": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Serialize the data to JSON
        json_data = json.dumps(battery_data)

        # Publish the serialized data to the "battery" topic
        client_pub.publish("battery", json_data, retain=True)

    client_pub.loop_stop()  # Stop the publisher client

if __name__ == "__main__":
    publish_message()
