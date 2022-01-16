import time
import argparse

import psutil
import paho.mqtt.client as mqtt
import sys
import threading

from sound import speech
from settings import HOST_IP, DEFAULT_TOPIC


def on_message(client, obj, msg):
	# print("Added order in history: ", int(msg.payload))
	# history.append( int(msg.payload) )
	print("Client receive text")
	speech(msg.payload)

# def getHistory():
#     return history


def listen():
	# Establish connection to mqtt broker
	client = mqtt.Client()
	client.on_message = on_message
	client.connect(host=HOST_IP, port=1883)
	client.subscribe(args['topic'], 0)

	try:
		client.loop_forever()
	except KeyboardInterrupt as e:
		pass


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip",
						default=HOST_IP,
						help="service ip of MQTT broker")
	parser.add_argument("--port",
						default=1883,
						type=int,
						help="service port of MQTT broker")
	parser.add_argument("--topic",
						default=DEFAULT_TOPIC,
						type=str,
						help="service port of MQTT broker")
	args = vars(parser.parse_args())
print("Subscribe to topic \"%s\"" % args['topic'])
print("Start Listening...")
listen()
