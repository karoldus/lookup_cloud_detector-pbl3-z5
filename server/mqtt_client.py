import logging
import signal
import sys
import json
import json_handler
from time import sleep
import paho.mqtt.client as mqtt
import base64


# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger("main")  # Logger for this module
logger.setLevel(logging.INFO) # Debugging for this file.


# Global Variables
BROKER_HOST = json_handler.configuration_read('BROKER_HOST')
BROKER_PORT = json_handler.configuration_read('BROKER_PORT')
CLIENT_ID = json_handler.configuration_read('CLIENT_ID')
TOPIC = json_handler.configuration_read('TOPIC')
client = None  # MQTT client instance. See init_mqtt()                                          # (5)





"""
MQTT Related Functions and Callbacks
"""
def on_connect(client, user_data, flags, connection_result_code):                              # (7)
    """on_connect is called when our program connects to the MQTT Broker."""

    if connection_result_code == 0:                                                            # (8)
        # 0 = successful connection
        logger.info("Connected to MQTT Broker")
    else:
        # connack_string() gives us a user friendly string for a connection code.
        logger.error("Failed to connect to MQTT Broker: " + mqtt.connack_string(connection_result_code))

    # Subscribe to the topic for LED level changes.
    client.subscribe(TOPIC, qos=2)                                                             # (9)



def on_disconnect(client, user_data, disconnection_result_code):                               # (10)
    """Called disconnects from MQTT Broker."""
    logger.error("Disconnected from MQTT Broker")



def on_message(client, userdata, msg):                                                         # (11)
    """Callback called when a message is received on a subscribed topic."""
    logger.debug("Received message for topic {}: {}".format( msg.topic, msg.payload))

    data = None
    print(f"\n\n")
    print("TOPIC: ", msg.topic)


    try:
        data = json.loads(msg.payload)  
        print('PAYLOAD:', data)
        raw_m = data['uplink_message']['frm_payload']
        print('DANE PRZED ZDEKODOWANIEM:', raw_m)
        ascii_m = base64.b64decode(raw_m.encode('ascii')).decode('ascii')
        print('DANE ASCII:', ascii_m)
        hex_m = [hex(ord(x)) for x in ascii_m]
        print('DANE HEX:', hex_m)
    except json.JSONDecodeError as e:
        logger.error("JSON Decode Error: ")

    # if msg.topic == TOPIC:                                                                     # (13)
    #     print("DZIAŁA:", data)                                                                    # (14)

    # else:
    #     logger.error("Unhandled message topic {} with payload " + str(msg.topic, msg.payload))



def signal_handler(sig, frame):
    """Capture Control+C and disconnect from Broker."""

    logger.info("You pressed Control + C. Shutting down, please wait...")

    client.disconnect() # Graceful disconnection.
    sys.exit(0)



def init_mqtt():
    global client

    # Our MQTT Client. See PAHO documentation for all configurable options.
    # "clean_session=True" means we don"t want Broker to retain QoS 1 and 2 messages
    # for us when we"re offline. You"ll see the "{"session present": 0}" logged when
    # connected.
    client = mqtt.Client(                                                                      # (15)
        client_id=CLIENT_ID,
        clean_session=False)

    client.username_pw_set(username=json_handler.keys_read("USERNAME"),password=json_handler.keys_read("PASSWORD"))

    # Route Paho logging to Python logging.
    client.enable_logger()                                                                     # (16)

    # Setup callbacks
    client.on_connect = on_connect                                                             # (17)
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to Broker.
    client.connect(BROKER_HOST, BROKER_PORT)                                                   # (18)



# Initialise Module

init_mqtt()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  # Capture Control + C                        # (19)
    logger.info("Listening for messages on topic '" + TOPIC + "'. Press Control + C to exit.")

    client.loop_start()
    
    while(1):
        print("hello")
        sleep(10)
    # signal.pause()
