# Gesture_Recognition
## How to Run
#### Run the eclipse mosquitto docker container
```bash
$ cd server_MQTT && sudo docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
```
#### Run Main Program
```bash
$ python3 server.py
```
#### Listen to  Main Program
```bash
$ python3 subscriber.py --ip localhost --port 1883
```