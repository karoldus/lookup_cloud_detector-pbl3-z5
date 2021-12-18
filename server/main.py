import signal
import mqtt_client
from signal_handler import signal_handler
from functools import partial
import logging
import time

# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger("main")  # Logger for this module
logger.setLevel(logging.INFO) # Debugging for this file.

if __name__ == "__main__":
    client = mqtt_client.init_mqtt()
    signal.signal(signal.SIGINT, partial(signal_handler, client, logger))  # Capture Control + C
    while(1):
        print("hello")
        mqtt_client.publish(client, 'v3/clouds-flow-control@ttn/devices/eui-70b3d57ed00486b4/down/replace', '123456', 2)
        time.sleep(10)