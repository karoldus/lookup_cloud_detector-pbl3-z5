import logging
import signal
import json
import json_handler
from time import sleep
import paho.mqtt.client as mqtt
import base64



# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger("main")  # Logger for this module
logger.setLevel(logging.INFO) # Debugging for this file.


######################## Analyze messeges ######################

def analyze_message(msg):
    topic = msg.topic
    payload = json.loads(msg.payload)

######################## MQTT Subscribe Callbacks ######################

def on_connect(client, user_data, flags, connection_result_code):
    """on_connect is called when our program connects to the MQTT Broker."""

    if connection_result_code == 0: # 0 = successful connection
        logger.info("Connected to MQTT Broker")
    else:
        logger.error("Failed to connect to MQTT Broker: " + mqtt.connack_string(connection_result_code)) # connack_string() gives us a user friendly string for a connection code.

    # Subscribe to the topic(s))
    TOPICS = json_handler.configuration_read('SUB_TOPICS')

    for topic in TOPICS.keys():
        client.subscribe(topic, qos=TOPICS[topic]) 

    logger.info("Listening for messages on {topic(s): QoS} '" + str(TOPICS))



def on_disconnect(client, user_data, disconnection_result_code):
    """on_disconnect is called when our program disconnects from the MQTT Broker."""
    logger.error("Disconnected from MQTT Broker")



def on_message(client, userdata, msg):
    """Callback called when a message is received on a subscribed topic."""
    logger.debug("Received message for topic {}: {}".format( msg.topic, msg.payload))

    data = None
    print(f"\n\n")
    print("TOPIC: ", msg.topic)

    analyze_message(msg)
    
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
        logger.error("JSON Decode Error: " + e)




######################## MQTT Publishing ######################
#https://www.thethingsindustries.com/docs/integrations/mqtt/

def publish(client, topic, data, qos=0, retain=False): # TO DO: topic -> id of device
    
    data_64 = base64.b64encode(data.encode()).decode('ascii')

    payload = '''{
        "downlinks": [{
            "f_port": 1,
            "frm_payload": "''' + data_64 + '''",
            "priority": "NORMAL"
        }]
        }'''
    client.publish(topic, payload, qos, retain)
    

    
######################## MQTT initialization ######################

def init_mqtt():
    """ 
    Initialize MQTT connection to broker and run loop handling messages.
    Returns: MQTT Client object
    """

    BROKER_HOST = json_handler.configuration_read('BROKER_HOST')
    BROKER_PORT = json_handler.configuration_read('BROKER_PORT')
    CLIENT_ID = json_handler.configuration_read('CLIENT_ID')

    client = mqtt.Client(
        client_id=CLIENT_ID,
        clean_session=False)

    client.username_pw_set(
        username=json_handler.keys_read("USERNAME"),
        password=json_handler.keys_read("PASSWORD"))

    # Route Paho logging to Python logging.
    client.enable_logger()

    # Setup callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to Broker.
    client.connect(BROKER_HOST, BROKER_PORT)

    # run client in loop - The loop_start() starts a new thread, that calls the loop method at regular intervals for you. It also handles re-connects automatically.
    client.loop_start()

    return client


######################## Example ######################

if __name__ == "__main__":
    client = init_mqtt()
    from signal_handler import signal_handler
    from functools import partial
    
    
    signal.signal(signal.SIGINT, partial(signal_handler, client, logger))  # Capture Control + C
    
    while(1):
        print("hello")
        sleep(10)
