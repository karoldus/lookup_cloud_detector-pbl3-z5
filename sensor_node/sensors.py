# TO DO: w jakich jednostkach jest temperatura? Format danych. Requirements.

from smbus2 import SMBus
from mlx90614 import MLX90614
from w1thermsensor import W1ThermSensor, Unit


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
    return round(sensor.get_obj_temp()+273.15, 1)



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
    return round(sensor.get_temperature(Unit.KELVIN), 1)



##### GETTING AND PREPARING DATA FROM ALL SENSORS #####

def get_all(ir_sensor, temp_sensor):
    """ 
    Read temperature from IR and ds18b20 sensors and prepare it to transmission.
    Parameters: ir_sensor, temp_sensor - sensor objects
    Returns: coded value of temperatures ready to transmission
    """
    ir_val = int(ir_read(ir_sensor) * 10)
    temp_val = int(temp_read(temp_sensor) * 10) # TO DO: filtering, etc...

    return str([ir_val,temp_val])
