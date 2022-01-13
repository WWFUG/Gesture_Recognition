import time
import argparse

import psutil
import paho.mqtt.client as mqtt

import threading
from sound import speech
# history = []

def on_message(client, obj, msg):
    # print("Added order in history: ", int(msg.payload))
    # history.append( int(msg.payload) )
    print("Client receive text")
    speech("mep")

# def getHistory():
#     return history

def listen():
    # Establish connection to mqtt broker
    client = mqtt.Client()
    client.on_message = on_message
    # client.connect(host = "localhost", port = 1883)
    client.connect(host = "172.20.10.5", port = 1883)
    client.subscribe('history', 0)

    try:
        client.loop_forever()
    except KeyboardInterrupt as e:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="localhost",
                        help="service ip of MQTT broker")
    parser.add_argument("--port",
                        default=1883,
                        type=int,
                        help="service port of MQTT broker")
    args = vars(parser.parse_args())
    print("Start Listening...")
    listen()
