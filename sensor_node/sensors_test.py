import sensors
import time
import datetime
import csv

ir_obj = sensors.ir_init()
temp_obj = sensors.temp_init()

tim = str(time.time())
with open('data/data_'+ tim +'.csv', 'a') as f:
    writeStr = ['timestamp', 'sky', 'ground', 'delta']
    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(writeStr)

while True:
    with open('data/data_'+ tim +'.csv', 'a') as f:
        t1 = sensors.ir_read(ir_obj)
        t2 = sensors.temp_read(temp_obj)
        now = datetime.datetime.now()
        writeStr = [now, t1, t2, t2- t1]
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(writeStr)
        time.sleep(4)

# bus.close()
