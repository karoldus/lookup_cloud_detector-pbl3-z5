DOWN_ORDER = {1: ['period', 2], 2: ['sensors', 1], 3: ['appkey', 16], 8: ["binary", 1]}  # order : {name, size} # <------- this could be in json !
BINARY_ORDER = {1 : "device-restart", 2 : "send-battery", 3 : "network-restart"}

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
                    if self.triggered & (1<<(i-1)): # if i' value was triggered
                        if i in DOWN_ORDER.keys():
                            le = DOWN_ORDER[i][1]*2 # B -> hex chars
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
        if key in self.values:
            return self.values[key]
        else:
            return False

    def get_triggered_keys(self):
        return list(self.values.keys())




obj = Downlink('8311112203')
print(obj.get_triggered_keys(), obj.values, obj.get_key_value('sensors'), obj.get_key_value('appkey'))