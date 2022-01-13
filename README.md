# Gesture_Recognition
## How to Run
#### Run the eclipse mosquitto docker container
```bash
$ cd server_MQTT && sudo docker run -d -it -p 1883:1883 -p 9001:9001 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
$ sudo docker run -d -it --net mynet123 --ip 140.112.25.46 -p 1883:1883 -p 9001:9001 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
```
#### Run Main Program
```bash
$ python3 server.py
```
#### Listen to  Main Program
```bash
$ python3 subscriber.py --ip localhost --port 1883
```