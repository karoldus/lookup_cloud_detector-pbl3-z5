import sensors
import time

ir_obj = sensors.ir_init()
temp_obj = sensors.temp_init()

while True:
    # t1 = sensors.ir_read(ir_obj)
    # t2 = sensors.temp_read(temp_obj)
    # print(f"IR: {t1}, DS18B20: {t2}")
    time.sleep(1)
    print("Values: ", sensors.get_all(ir_obj, temp_obj))

# bus.close()