'''
To Do:
- timeout
- write_timeout
'''
import serial
import io
import time

ANSWER_TIMEOUT = 1.2
JOINING_TIMEOUT = 20
MESSAGE_TIMEOUT = 10

def test_device(ser):
    ser.reset_input_buffer()
    ser.write(b'AT\n')
    ser.flush() 
    time.sleep(ANSWER_TIMEOUT)
    while ser.inWaiting() > 0:  
        ans = ser.readline().decode('ascii')
        # print(ans)
        if "+AT: OK" in ans:
            ser.reset_input_buffer()
            return "Device is working"
    return "Device isn't working"


def get_device_id(ser): # TO DO
    ser.reset_input_buffer()
    ser.write(b'AT+ID\n')
    ser.flush() 
    time.sleep(ANSWER_TIMEOUT)
    while ser.inWaiting() > 0:  
        ans = ser.readline().decode('ascii')
        print(ans)


def join_network(ser):                      # co w przypadku, gdy już jest dołączony?
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
    
    print("Timeout joining network.")
    return -1


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
                return 0
            elif "Start" in ans:
                print("STARTING...")
            elif "Done" in ans:
                print("SENT")
                return 1
            elif "RX" in ans:
                print("DOWNLINK PAYLOAD: ", ans) # TO DO - analyze payload
                return 1
    
    print("Timeout sending message.")
    return -1





if __name__ == '__main__':

    with serial.Serial('/dev/ttyUSB0', 9600, timeout=None) as ser:
        try:
            print("CONNECTED TO: ", ser.name)
            print(ser)
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