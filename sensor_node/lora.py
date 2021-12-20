import serial
import io
import time
import json_handler as json_conf

ANSWER_TIMEOUT = 1.2
JOINING_TIMEOUT = 20
MESSAGE_TIMEOUT = 10



########## FUNCTIONS ############

def __push_command(ser, command):
    """ 
    Add \n, reset input buffer, write and flush command to LoRa module.
    Parameters: ser - LoRa module object; command - str
    """
    command = command + '\n'
    ser.reset_input_buffer()
    ser.write(command.encode())
    ser.flush()


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


def get_device_id(ser): # TO DO
    """ 
    Get device and app ID. [TO DO]
    Parameters: ser - LoRa module object
    Returns: nothing, prints ID
    """
    ser.reset_input_buffer()
    ser.write(b'AT+ID\n')
    ser.flush() 
    time.sleep(ANSWER_TIMEOUT)
    while ser.inWaiting() > 0:  
        ans = ser.readline().decode('ascii')
        print(ans)


def join_network(ser):
    """ 
    Join to LoRaWAN network.
    Parameters: ser - LoRa module object
    Returns: 0 (failed), 1 (success), -1 (timeout)
    """
    print("JOINING TO NETWORK...")
    ser.reset_input_buffer()
    ser.write(b'AT+JOIN\n')
    ser.flush()

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
            elif "Joined already" in ans:
                print("Joined already")
                return 1                    # TO DO tutaj dać inny kod
    
    print("Timeout joining network.")
    return -1


def analyze_downlink(mess):
    """ 
    To use only inside this library.
    Analyze downlink message and save new configuration to file. [only period - TO DO other configuration]
    Parameters: ser - LoRa module object
    Returns: True (saved new configuration), False (wrong format)
    """
    x = mess.find("RX:")
    payload = mess[x+5:] # RX: "payload"  ->  payload
    x = payload.find('"')
    payload = payload[0:x]
    print("DOWNLINK PAYLOAD: ", payload)
    if len(payload) != 4:
        print("Wrong format of downlink message!")
        return False
    else:
        x = int(payload, 16)
        json_conf.configuration_save('PERIOD', x)

    return True


def send_mess_string(ser, mess):
    """ 
    Send string message via LoRa.
    Parameters: ser - LoRa module object, mess - message in string format
    Returns: 0 - error, 1 - OK, -1 timeout, 2 - ok and downlink
    """
    print("SENDING MESSAGE {mess}...")
    mess = str(mess)
    command = 'AT+MSG='+mess+'\n'
    ser.reset_input_buffer()
    ser.write(command.encode())
    ser.flush()

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
                resp = analyze_downlink(ans) # We want True
    
    print("Timeout sending message.")
    return -1 if resp != True else 2


def send_mess_hex(ser, mess):
    """ 
    Send hex message via LoRa. [TO DO - checking mess format]
    Parameters: ser - LoRa module object, mess - message in string-hex format
    Returns: 0 - error, 1 - OK, -1 timeout, 2 - ok and downlink
    """
    print(f"SENDING MESSAGE {mess}...")
    mess = str(mess)
    command = 'AT+MSGHEX='+mess+'\n'
    ser.reset_input_buffer()
    ser.write(command.encode())
    ser.flush()

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
                resp = analyze_downlink(ans) # We want True
    
    print("Timeout sending message.")
    return -1 if resp != True else 2



############ EXAMPLE ############

if __name__ == '__main__':

    with init_object() as ser:
        try:
            print(test_device(ser))
            get_device_id(ser)

            while join_network(ser) != 1:
                print(test_device(ser))
                time.sleep(3)

            num = 1

            while True:

                send_mess_string(ser, "hejka_"+str(num))
                num = num + 1
                print("idle")
                time.sleep(60)
                
        except:
                print("Disconnected")
                ser.close()
