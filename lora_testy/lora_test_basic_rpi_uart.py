# NIE DZIAŁA
# działa zapis, ale odczyt nie... 





import serial
import io
import time

with serial.Serial('/dev/ttyS0', 9600, timeout=None) as ser:
    print(ser.name)
    print(ser)

    while True:
        try:
            print("cp1")
            ser.write(b'AT+ID')
            print("cp2")
            ser.flush()   
            print("cp3") 

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
            else:
                print("error oooo")
            print("cp4")
            time.sleep(0.03)
            data_left = ser.inWaiting()             #check for remaining byte
            received_data += ser.read(data_left)
            print (received_data)
            time.sleep(0.1)



        except:
                print("board is disconnected")
                ser.close()
                break