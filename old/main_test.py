from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS



if __name__ == "__main__":
	table = "Io3_Test1"
	# You can generate an API token from the "API Tokens Tab" in the UI
	token = "udWmqLWgGiyk23GWaZ-e5kzsCtmTEhBFUhCBITJ218c6Xoo4-28OoJLpLmktZAbhMtMu3yl6XXKjzFEtnuEs-w=="
	org = "Polito"
	bucket = table

	with InfluxDBClient(url="http://olgyay.polito.it:8090", token=token, org=org) as client:
		write_api = client.write_api(write_options=SYNCHRONOUS)

		data = "ciccio, host=host2 used_percent=23.43234543"
		write_api.write(bucket, org, data)

		query = f'from(bucket: "{table}") |> range(start: -1h)'
		tables = client.query_api().query(query, org=org)
		for table in tables:
			for record in table.records:
				print(record["_value"])
				#print(record)
	a = 1


