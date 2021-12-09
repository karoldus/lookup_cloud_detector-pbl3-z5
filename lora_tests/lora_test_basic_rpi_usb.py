import serial
import io
import time

with serial.Serial('/dev/ttyUSB0', 9600, timeout=None) as ser:
    print(ser.name)
    print(ser)

    while True:
        try:
            ser.write(b'AT+ID\n')
            ser.flush()   

            # v1:
            time.sleep(1.2)
            while ser.inWaiting() > 0:  
                stm = ser.readline().decode('ascii')
                print(stm)

            #v2 - działa, ale ma problem z oczekiwaniem
            # time.sleep(1.5)
            # if ser.inWaiting() > 0:
            #     received_data = ser.read()              #read serial port
            #     time.sleep(0.03)
            #     data_left = ser.inWaiting()             #check for remaining byte
            #     received_data += ser.read(data_left)
            #     print (received_data)
            # else:
            #     print("error oooo")

            
            time.sleep(0.1)



        except:
                print("board is disconnected")
                ser.close()
                break