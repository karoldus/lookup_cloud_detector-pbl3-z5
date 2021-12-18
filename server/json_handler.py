import json

def configuration_save(key, value):
    with open("configuration.json", "r") as read_file:
        data = json.load(read_file)
    with open("configuration.json", "w") as write_file:
        data[key] = value
        json.dump(data, write_file)
    
def configuration_read(key):
    with open("configuration.json", "r") as read_file:
        data = json.load(read_file)
        return data[key]

def keys_read(key):
    with open("keys.json", "r") as read_file:
        data = json.load(read_file)
        return data[key]
