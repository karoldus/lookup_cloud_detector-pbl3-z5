# TO DO: w jakich jednostkach jest temperatura? Format danych. Requirements.

from smbus2 import SMBus
from mlx90614 import MLX90614
from w1thermsensor import W1ThermSensor


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
    return sensor.get_obj_temp()



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
    return sensor.get_temperature()