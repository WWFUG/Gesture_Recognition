# Gesture_Recognition
## How to Run
#### Run the eclipse mosquitto
```bash
$ mosquitto -c ./src/server_MQTT/mosquitto.conf -v 
```
#### Run Main Program
```bash
$ python3 ./src/main.py [topic]
```
#### Listen to  Main Program
* By terminal
```bash
$ sudo systemctl stop mosquitto.service
$ python3 ./src/client_MQTT/subscriber.py --ip localhost --port 1883 --topic <topic>
```
* By website (using Google Chrome)
    * Open "index.html" in the directory "src/website"
    * Deployed but can't use: https://kaowyk.github.io/ASLR-Subscriber/