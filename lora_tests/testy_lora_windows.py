import serial
import io
import time

with serial.Serial('COM7', 9600, timeout=None) as ser:

    while True:
        try:
            ser.write(b'AT')
            ser.flush()    
            time.sleep(0.2)      
            stm = ser.readline().decode('ascii')
            print(stm)
            time.sleep(1)


        except:
                print("or STM32 board was disconnected, Data successfully saved")
                ser.close()
                break