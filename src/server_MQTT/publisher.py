import time
import argparse

import psutil
import paho.mqtt.client as mqtt

def send(text):
    # Establish connection to mqtt broker
    client = mqtt.Client()
    client.connect(host = "localhost", port = 1883)
    client.loop_start()
    
    client.publish(topic = "history", payload = text)

    client.loop_stop()

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--ip",
#                         default="localhost",
#                         help="service ip of MQTT broker")
#     parser.add_argument("--port",
#                         default=1883,
#                         type=int,
#                         help="service port of MQTT broker")
#     parser.add_argument("--topic",
#                         default="cpu",
#                         choices=['cpu', 'mem'],
#                         help="Availabel information to publish")
#     args = vars(parser.parse_args())
#     send(args)
