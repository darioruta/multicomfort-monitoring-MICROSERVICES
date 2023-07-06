from datetime import datetime

from influxdb_client import InfluxDBClient,Point,WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

import matplotlib.pyplot as plt
import random
if __name__ == "__main__":
	table = "Io3_Test1"
	# You can generate an API token from the "API Tokens Tab" in the UI
	token = "udWmqLWgGiyk23GWaZ-e5kzsCtmTEhBFUhCBITJ218c6Xoo4-28OoJLpLmktZAbhMtMu3yl6XXKjzFEtnuEs-w=="
	org = "Polito"
	bucket = table

	client = InfluxDBClient(url="http://olgyay.polito.it:8090", token=token, org=org)
	write_api = client.write_api(write_options=SYNCHRONOUS)

	#random.seed(1)
	nn = float(20 + random.randrange(-3, 3))
	nn2 = float(20 + random.randrange(-3, 3))
	point = Point("Io3_multiconfort") \
            .tag("host", "host13") \
            .field("co2", nn) \
			.field("temp",nn2) \
            .time(datetime.utcnow(), WritePrecision.NS)
	#print(point)

	write_api.write(bucket, org, point)

	query = f'from(bucket: "{table}") |> range(start: -3d)'
	tables = client.query_api().query(query, org=org)
	co2_values = []
	temp_values = []
	for table in tables:
		#print(table.columns)
		for record in table.records:
			if record["_field"] == "co2":
				co2_values.append(record["_value"])
			elif record["_field"] == "temp":
				temp_values.append(record["_value"])
			else:
				pass
			#print(record)
			#print(record["_value"])
			#print(record)
	print(f"co2: {co2_values}")
	print(f"temp: {temp_values}")
	
	plt.plot(co2_values)
	plt.ylabel('some numbers')
	plt.show()
	a = 1
