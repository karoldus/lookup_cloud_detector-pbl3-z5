import sensors
import lora
import time
import json_handler as json_conf

if __name__ == '__main__':
    with lora.init_object() as ser:
        try:
            print(lora.test_device(ser))
            lora.get_device_id(ser)

            lora.hard_join_network(ser)

            ir_sensor = sensors.ir_init()
            temp_sensor = sensors.temp_init()

            PERIOD = json_conf.configuration_read("PERIOD")


            while True:
                resp = lora.send_mess_hex(ser, sensors.get_all(ir_sensor,temp_sensor))
                    
                print("idle")
                PERIOD = json_conf.configuration_read("PERIOD")
                time.sleep(PERIOD)
                
        except Exception as e:
                print("Disconnected", str(e))
                ser.close()