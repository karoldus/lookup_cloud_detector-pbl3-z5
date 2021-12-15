import sensors
import lora
import time
import json

if __name__ == '__main__':
    with lora.init_object() as ser:
        try:
            print(lora.test_device(ser))
            lora.get_device_id(ser)

            while lora.join_network(ser) != 1:
                print(lora.test_device(ser))
                time.sleep(3)

            ir_sensor = sensors.ir_init()
            temp_sensor = sensors.temp_init()

            PERIOD = 600

            with open("configuration.json", "r") as read_file:
                data = json.load(read_file)
                PERIOD = data['PERIOD']


            while True:
                lora.send_mess_hex(ser, sensors.get_all(ir_sensor,temp_sensor))
                print("idle")
                time.sleep(PERIOD)
                
        except:
                print("Disconnected")
                ser.close()