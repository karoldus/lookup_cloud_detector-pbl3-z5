# Adding devices locations to InfulxDB

import influx_bridge as db

def add_loc_to_influxdb(data):
    json_body = [
        {
            'measurement': "locations",
            'tags': {
                'dev_id': data["dev_id"],          
            },
            'fields': {
                'latitude' : data["lat"],
                'longitude': data["long"]               
            }
        }
    ]
    db.influxdb_client.write_points(json_body)


if __name__ == "__main__":
    db.init_influxdb_database()
    # add_loc_to_influxdb({"dev_id" : "fake-1", "lat": 52.203230, "long": 20.962188})
    # add_loc_to_influxdb({"dev_id" : "eui-70b3d57ed00486b4", "lat": 52.218688, "long": 21.010844})
    # add_loc_to_influxdb({"dev_id" : "eui-2cf7f12032304959", "lat": 52.230688, "long": 21.01197})
