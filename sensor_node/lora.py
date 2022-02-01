import serial
import io
import time
import json_handler as json_handler
import message_format
import os

ANSWER_TIMEOUT = 1.2
JOINING_TIMEOUT = 20
MESSAGE_TIMEOUT = 10
MIN_PERIOD = 20




########## SUPPORT FUNCTIONS ############

def __push_command(ser, command):
    """ 
    Add \n, reset input buffer, write and flush command to LoRa module.
    Parameters: ser - LoRa module object; command - str
    """
    command = command + '\n'
    ser.reset_input_buffer()
    ser.write(command.encode())
    ser.flush()



########## SETTINGS FUNCTIONS ############

def change_appkey(ser, new_appkey): # need error handling
    """ 
    Set new APPKEY.
    Parameters: ser - LoRa module object, new_appkey [str]
    Returns: nothing
    """
    __push_command(ser, f'AT+KEY=APPKEY, "{new_appkey}"')
    time.sleep(ANSWER_TIMEOUT)


def get_device_id(ser): # TO DO
    """ 
    Get device and app ID. [TO DO]
    Parameters: ser - LoRa module object
    Returns: nothing, prints ID
    """
    __push_command(ser, 'AT+ID') 
    time.sleep(ANSWER_TIMEOUT)
    while ser.inWaiting() > 0:  
        ans = ser.readline().decode('ascii')
        print(ans)



########## GENERAL (DEVICE) FUNCTIONS ############

def init_object():
    """ 
    Initialize USB connection with LoRa-E5 mini device
    Returns: LoRa module object
    """
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
    print("USB: Connected to: ", ser.name)
    return ser


def test_device(ser):
    """ 
    Test LoRa module (send AT).
    Parameters: ser - LoRa module object
    Returns: "OK" or "Device isn't working"
    """
    __push_command(ser, 'AT')
    time.sleep(ANSWER_TIMEOUT)
    while ser.inWaiting() > 0:  
        ans = ser.readline().decode('ascii')
        if "+AT: OK" in ans:
            ser.reset_input_buffer()
            return "OK"
    return "Device isn't working"



########## CONNECTION FUNCTIONS ############

def join_network(ser):
    """ 
    Join to LoRaWAN network.
    Parameters: ser - LoRa module object
    Returns: 0 (failed), 1 (success), 2 (joined_already) -1 (timeout)
    """
    print("JOINING TO NETWORK...")

    __push_command(ser, 'AT+JOIN')

    start = time.time()
    
    while (time.time() - start < JOINING_TIMEOUT):
        while ser.inWaiting() > 0:
            ans = ser.readline().decode('ascii')
            if "Join failed" in ans:
                print("JOIN FAILED")
                return 0
            elif "Start" in ans:
                print("STARTING...")
            elif "joined" in ans:
                print("Joined network")
            elif "NetID" in ans:
                print(ans)
                return 1
            elif "Done" in ans:
                return 1
            elif "Joined already" in ans:
                print("Joined already")
                return 2
    
    print("Timeout joining network.")
    return -1


def hard_join_network(ser):
    """ 
    Join to LoRaWAN network (guaranteed connection).
    Parameters: ser - LoRa module object
    Returns: 1 (success), 2 (joined_already)
    """
    while(1):
        r = join_network(ser)

        if r==2 or r==1:
            return r
        else:
            time.sleep(JOINING_TIMEOUT)
  


def reconnect_network(ser):
    """ 
    Disconnect from and connect to network.
    Parameters: ser - LoRa module object
    Returns: nothing
    """
    __push_command(ser, 'AT+JOIN=FORCE')
    time.sleep(ANSWER_TIMEOUT)
    if hard_join_network(ser) == 2:
        print('hard_joined is 2 in reconnect') # issue #7
        # disconnect_network(ser)
        # time.sleep(JOINING_TIMEOUT)
        # reconnect_network(ser)



########## MESSAGE FUNCTIONS ############

def __send_message(ser, command):
    """ 
    To use only inside this library.
    Push command that is send_mess_x command.
    Parameters: ser - LoRa module object, command [str]
    Returns: 0 - error, 1 - OK, -1 timeout, 2 - ok and downlink
    """
    __push_command(ser, command)

    start = time.time()

    resp = False
    
    while (time.time() - start < MESSAGE_TIMEOUT):
        while ser.inWaiting() > 0:
            ans = ser.readline().decode('ascii')
            if "Please join network first" in ans:
                print("Please join network first")
                join_network(ser)
                return 0
            elif "Start" in ans:
                print("STARTING...")
            elif "Done" in ans:
                print("SENT")
                return 1 if resp != True else 2
            elif "RX:" in ans:
                print("DOWNLINK MESS: ", ans) 
                resp = analyze_downlink(ser, ans) # We want True
    
    print("Timeout sending message.")
    return -1 if resp != True else 2


def send_mess_string(ser, mess):
    """ 
    Send string message via LoRa.
    Parameters: ser - LoRa module object, mess - message in string format
    Returns: 0 - error, 1 - OK, -1 timeout, 2 - ok and downlink
    """
    print(f"SENDING MESSAGE {mess}...")
    mess = str(mess)
    command = 'AT+MSG='+mess
    
    return __send_message(ser, command)


def send_mess_hex(ser, mess):
    """ 
    Send hex message via LoRa. [TO DO - checking mess format]
    Parameters: ser - LoRa module object, mess - message in string-hex format
    Returns: 0 - error, 1 - OK, -1 timeout, 2 - ok and downlink
    """
    print(f"SENDING MESSAGE {mess}...")
    mess = str(mess)
    command = 'AT+MSGHEX='+mess
    
    return __send_message(ser, command)



########## DOWNLINK REACTION FUNCTIONS ############

def downlink_period(ser, period):
    """ 
    To use only inside this library.
    Handler of "period" argument of downlink message. Save new period value to configuration.json.
    Parameters: period - new period value
    Returns: nothing
    """
    print(f"mamy period! {period}")
    if period < MIN_PERIOD:
        period = MIN_PERIOD
        
    json_handler.configuration_save('PERIOD', period)


def downlink_sensors(ser, sensors):
    print('sensors from downlink', sensors)
    json_handler.configuration_save('SENSORS_TO_READ', sensors)


def downlink_appkey(ser, appkey_hex):
    print("Zmiana apppkkeeeyyyy")
    print(appkey_hex)
    change_appkey(ser, appkey_hex)


def device_restart(*args):
    print('reboot from downlink')
    os.system('sudo reboot')


def downlink_network_restart(ser, *args):
    print('reconnect network from downlink')
    reconnect_network(ser)


# Assign functions to downlink messages
DOWNLINK_OPERATIONS = {'period': downlink_period, 'sensors': downlink_sensors, 'appkey': downlink_appkey, 'device-restart': device_restart, "network-restart": downlink_network_restart}


def analyze_downlink(ser, mess):
    """ 
    To use only inside this library.
    Analyze downlink message and save new configuration to file. [only period - TO DO other configuration]
    Parameters: ser - LoRa module object, mess - line from LoRa module with 'RX:'
    Returns: True (saved new configuration), False (wrong format)
    """
    # 1. from 'RX: "payload"'  to  'payload'
    x = mess.find("RX:")
    payload = mess[x+5:]
    x = payload.find('"')
    payload = payload[0:x]
    print("DOWNLINK PAYLOAD: ", payload)

    downlink_obj = message_format.Downlink(payload)

    for k in downlink_obj.get_triggered_keys():
        if k in DOWNLINK_OPERATIONS.keys():
            v = downlink_obj.get_key_value(k)
            DOWNLINK_OPERATIONS[k](ser, v) # run function with argument
        else:
            print(f'ERROR: function for "{k}" downlink argument is not defined!')

    return True





############ EXAMPLE ############

# if __name__ == '__main__':

#     analyze_downlink('RX: "030123ab"')

    # with init_object() as ser:
    #     try:
    #         print(test_device(ser))
    #         get_device_id(ser)

    #         while join_network(ser) != 1:
    #             print(test_device(ser))
    #             time.sleep(3)

    #         num = 1

    #         while True:

    #             send_mess_string(ser, "hejka_"+str(num))
    #             num = num + 1
    #             print("idle")
    #             time.sleep(60)
                
    #     except:
    #             print("Disconnected")
    #             ser.close()
