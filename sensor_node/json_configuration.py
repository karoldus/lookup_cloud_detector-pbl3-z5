import json

def save(key, value):
    with open("configuration.json", "r") as read_file:
        data = json.load(read_file)
    with open("configuration.json", "w") as write_file:
        data[key] = value
        json.dump(data, write_file)
    
def read(key):
    with open("configuration.json", "r") as read_file:
        data = json.load(read_file)
        return data[key]
