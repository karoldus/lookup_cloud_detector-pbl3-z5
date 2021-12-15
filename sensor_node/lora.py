import serial
import io
import time

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
    ser.reset_input_buffer()
    ser.write(b'AT+ID\n')
    ser.flush() 
    time.sleep(ANSWER_TIMEOUT)
    while ser.inWaiting() > 0:  
        ans = ser.readline().decode('ascii')
        print(ans)


def join_network(ser):
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
    x = mess.find("RX:")
    payload = mess[x+5:-1] # RX: "payload"  ->  payload # w jakim formacie jest payload???
    print("DOWNLINK PAYLOAD: ", payload)


def send_mess_string(ser, mess):
    print("SENDING MESSAGE {mess}...")
    mess = str(mess)
    command = 'AT+MSG='+mess+'\n'
    ser.reset_input_buffer()
    ser.write(command.encode())
    ser.flush()

    start = time.time()
    
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
                return 1
            elif "RX:" in ans:
                print("DOWNLINK MESS: ", ans) # TO DO - analyze payload
                analyze_downlink(ans)
    
    print("Timeout sending message.")
    return -1



def send_mess_hex(ser, mess):
    print(f"SENDING MESSAGE {mess}...")
    mess = str(mess)
    command = 'AT+MSGHEX='+mess+'\n'
    ser.reset_input_buffer()
    ser.write(command.encode())
    ser.flush()

    start = time.time()
    
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
                return 1
            elif "RX:" in ans:
                print("DOWNLINK MESS: ", ans) # TO DO - analyze payload
                analyze_downlink(ans)
    
    print("Timeout sending message.")
    return -1





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
