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
        time.sleep(10)