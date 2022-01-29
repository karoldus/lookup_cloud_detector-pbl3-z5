from influxdb import InfluxDBClient

INFLUXDB_ADDRESS = '192.168.0.109'
INFLUXDB_USER = 'chmury'
INFLUXDB_PASSWORD = 'chmury4all'
INFLUXDB_DATABASE = 'lookup'

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

def send_data_to_influxdb(data):
    json_body = [
        {
            'measurement': "uplink",
            'tags': {
                'dev_id': data["dev_id"]
            },
            'fields': {
                'status': data['status'],
                'sky': data["sky_temp"],
                'ambient' : data["ambient_temp"],
                'delta' : data["delta_temp"]                
            }
        }
    ]
    influxdb_client.write_points(json_body)

def init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)


#EXAMPLE

# init_influxdb_database()
# data = influxdb_client.query('SELECT "status" FROM "uplink" WHERE time > now() - 7d  GROUP BY "dev_id" ORDER BY DESC LIMIT 1')
# ret = []
# for s in data.raw['series']:
#     ret.append([s['tags']['dev_id'], s['values'][0][1], s['values'][0][0]])

# print(ret)


# for point in data.get_points():
#     print(point)