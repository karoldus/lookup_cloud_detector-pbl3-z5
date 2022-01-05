DOWN_ORDER = {1: ['period', 2], 2: ['sensors', 1], 3: ['appkey', 16], 8: ["binary", 1]}  # order : {name, size} # <------- this could be in json !
BINARY_ORDER = {1 : "device-restart", 2 : "send-battery", 3 : "network-restart"}
UP_ORDER = {1: ['ambient_temp', 1], 2: ['sky_temp', 1]}

class Downlink():
    def __init__(self, payload):
        self.triggered = 0
        self.values = {}
        self.binary = None
        if len(payload) >= 2:
            self.triggered = int(payload[0:2], 16)
            payload = payload[2:]
            if len(payload) >= 2:
                for i in range(1,9):
                    if self.triggered & (1<<(i-1)):     # if i' value was triggered
                        if i in DOWN_ORDER.keys():
                            le = DOWN_ORDER[i][1]*2     # B -> hex chars
                            if le > 0:
                                if len(payload) >= le:
                                    v = payload[0:le]
                                    payload = payload[le:]
                                    self.values[DOWN_ORDER[i][0]] = int(v,16)
                                else:
                                    print('ERROR: Wrong payload format - too short')
                            elif le == 0:
                                self.values[DOWN_ORDER[i][0]] = None
                        else:
                            print("error - this value shouldn't be triggered")
        if "binary" in self.values.keys():
            for i in range(1,9):
                if i in BINARY_ORDER.keys():
                    if self.values['binary']  & (1<<(i-1)):
                        self.values[BINARY_ORDER[i]] = True
                else:
                    print("error - this binary value shouldn't be triggered")

    def get_key_value(self, key):
        """ 
        Get value for key from downlink payload.
        Parameters: key [str]
        Returns: value [int]
        """
        if key in self.values:
            return self.values[key]
        else:
            return False

    def get_triggered_keys(self):
        """ 
        Get list of all keys in downlink payload.
        Parameters: nothing
        Returns: list
        """
        return list(self.values.keys())



class Uplink():
    def __init__(self):
        self.values = {}    # {'name' : 'value_hex', 'ambient_temp' : '5a'}
        self.sensors = {}   # {'name': [order, length]}
        for i in UP_ORDER.keys():
            self.sensors[UP_ORDER[i][0]] = [i, UP_ORDER[i][1]] 

    def add_value(self, sensor_name, value:int):
        """ 
        Add value from sensor to payload.
        Parameters: sensor_name {ambient_temp, sky_temp}, value
        Returns: nothing
        """
        if sensor_name in self.sensors.keys():
            value_hex = hex(value)[2:]
            if len(value_hex) == self.sensors[sensor_name][1]*2:
                self.values[sensor_name] = value_hex
            elif len(value_hex) < self.sensors[sensor_name][1]*2:       # add zeros if length is too short
                while len(value_hex) < self.sensors[sensor_name][1]*2:
                    value_hex = '0' + value_hex
                self.values[sensor_name] = value_hex
            else:                                                       #length is too long
                print(f'This sensor ({sensor_name}) has defined other payload length')
        else:
            print(f'This sensor ({sensor_name}) is not defined in format standard.')

    def format_payload(self):
        """ 
        Format payload from preverious added values.
        Parameters: nothing
        Returns: formatted value [hex in str]
        """
        if bool(self.values) != False:          #is not empty
            header = 0
            payload = ''
            for k in self.values.keys():        # k is sensor name
                header = header | 1 << (self.sensors[k][0]-1)
            
            for place in range(1,9):
                if place in UP_ORDER.keys():
                    if UP_ORDER[place][0] in self.values.keys():        # UP_ORDER[place][0] is sensor name
                        header = (header | (1 << (place-1)))
                        payload = payload + self.values[UP_ORDER[place][0]]

            header_hex = hex(header)[2:]
            if len(header_hex) == 1:
                header_hex = '0' + header_hex   # make header 1 byte length
            payload = header_hex + payload
            return payload
        else:
            return None



# obj = Uplink()
# obj.add_value('ambient_temp', 123)
# obj.add_value('sky_tempdvf', 123)
# print(obj.values)
# print(obj.format_payload())