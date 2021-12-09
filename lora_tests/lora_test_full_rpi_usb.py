'''
To Do:
- timeout
- write_timeout
'''


import serial
import io
import time

def test_device(ser):
    ser.write(b'AT+ID\n')
    ser.flush() 


with serial.Serial('/dev/ttyUSB0', 9600, timeout=None) as ser:
    # print(ser.name)
    # print(ser)

    while True:
        try:
            ser.write(b'AT+ID')
            ser.flush()   

            # v1 - nwm czy działa:
            # time.sleep(0.2) 
            # print(ser.is_open)     
            # stm = ser.readline().decode('ascii')
            # print("cp4")
            # print(stm)

            #v2 - działa, ale ma problem z oczekiwaniem
            time.sleep(1.5)
            if ser.inWaiting() > 0:
                received_data = ser.read()              #read serial port
                time.sleep(0.03)
                data_left = ser.inWaiting()             #check for remaining byte
                received_data += ser.read(data_left)
                print (received_data)
            else:
                print("error oooo")

            
            time.sleep(0.1)



        except:
                print("board is disconnected")
                ser.close()
                break