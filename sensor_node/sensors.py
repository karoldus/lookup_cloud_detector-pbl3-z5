from smbus2 import SMBus
from mlx90614 import MLX90614
from w1thermsensor import W1ThermSensor, Unit
import sys


###### SEN0263 - IR SENSOR #####

def ir_init():
    """ 
    Initialize SEN0263 IR sensor.
    Returns: sensor object
    """
    bus = SMBus(1)
    sensor = MLX90614(bus, address=0x5A)
    return sensor


def ir_read(sensor):
    """ 
    Read object (sky) temperature from SEN0263 IR sensor.
    Parameters: sensor - sensor object
    Returns: temperature
    """
    try: # there are 2 versions of this library - fix it!
        return round(sensor.get_obj_temp(), 0)
    except:
        return round(sensor.get_object_1(), 0)



###### DS18B20 - TEMPERATURE SENSOR #####

def temp_init():
    """ 
    Initialize DS18B20 temperature sensor.
    Returns: sensor object
    """
    sensor = W1ThermSensor()
    return sensor


def temp_read(sensor):
    """ 
    Read ambient temperature from DS18B20 temperature sensor.
    Parameters: sensor - sensor object
    Returns: temperature
    """
    return round(sensor.get_temperature(), 0)



##### GETTING AND PREPARING DATA FROM ALL SENSORS #####

def get_all(ir_sensor, temp_sensor):
    """ 
    Read temperature from IR and ds18b20 sensors and prepare it to transmission.
    Parameters: ir_sensor, temp_sensor - sensor objects
    Returns: coded value of temperatures ready to transmission
    """
    ir_val = int((ir_read(ir_sensor) + 100) * 10)
    temp_val = int((temp_read(temp_sensor) + 100) * 10) # TO DO: filtering, etc...

    value = ((ir_val << 12) | temp_val)

    return format(value, 'X')
