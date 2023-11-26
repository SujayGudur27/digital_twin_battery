import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
from datetime import datetime
from threading import Lock

def on_message(client, userdata, msg):
    # Get the message payload (serialized JSON data)
    json_data = msg.payload.decode()

    # Deserialize the JSON data
    battery_data = json.loads(json_data)

    # Extract voltage and time information
    voltage = battery_data["voltage"]
    timestamp = datetime.strptime(battery_data["time"], "%Y-%m-%d %H:%M:%S")

    # Update the plot data
    update_plot(timestamp, voltage)

def update_plot(timestamp, voltage):
    # Acquire a lock to prevent simultaneous access to the plot data
    with lock:
        timestamps.append(timestamp)
        voltages.append(voltage)

def animate_plot(frame):
    # Update the plot with the latest data
    with lock:
        ax.clear()
        ax.plot(timestamps, voltages, marker='o', linestyle='-')
        ax.set_title('Battery Discharge Over Time')
        ax.set_xlabel('Time')
        ax.set_ylabel('Voltage (V)')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax.xaxis.set_major_locator(mdates.SecondLocator(interval=10))
        fig.autofmt_xdate()

if __name__ == "__main__":
    # Set up MQTT connection for subscribing
    client_sub = mqtt.Client()
    client_sub.on_message = on_message
    client_sub.connect("test.mosquitto.org", 1883)  # Change to your MQTT broker address
    client_sub.subscribe("battery")  # Subscribe to the "battery" topic

    # Lists to store data for plotting
    timestamps = []
    voltages = []
    lock = Lock()

    # Set up the initial plot
    fig, ax = plt.subplots()
    ani = animation.FuncAnimation(fig, animate_plot, interval=1000)  # Update every 1000 milliseconds

    # Start a loop to listen for messages on the subscribed topic
    client_sub.loop_start()

    try:
        plt.show()
    except KeyboardInterrupt:
        print("Exiting the program.")
        client_sub.loop_stop()  # Stop the subscriber client
