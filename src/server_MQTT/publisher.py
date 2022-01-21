import time
import argparse

import psutil
import paho.mqtt.client as mqtt
from settings import HOST_IP

client = None

def connect():
	try:
		global client
		client = mqtt.Client()
		client.connect(host = HOST_IP, port = 1883)
	except:
		print( "Error: Connection Failed" )


def send( topic, text ):
	# Establish connection to mqtt broker
	try:

		client.loop_start()
		client.publish( topic = topic , payload = text )
		client.loop_stop()

	except:
		print( "Error: Connection Failed" )

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
