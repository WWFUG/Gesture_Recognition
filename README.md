# Gesture_Recognition
## How to Run
#### Run the eclipse mosquitto
```bash
$ mosquitto -c ./src/server_MQTT/mosquitto.conf -v 
```
#### Run Main Program
```bash
$ python3 ./src/server.py
```
#### Listen to  Main Program
* By terminal
```bash
$ python3 ./src/client_MQTT/subscriber.py --ip localhost --port 1883
```
* By website
https://kaowyk.github.io/ASLR-Subscriber/