from influxdb_client import InfluxDBClient
import csv

bucket = "plant_monitoring"

client = InfluxDBClient(url="http://localhost:8086", token="qhksOuIwj3B8JO5uogENGEyoeJU4h0RAJceFU7HjQsPJPpOKozrgYeBBCX1yG-VRc6_4WYn8_aHvKBA7zbzYEg==", org="Home")

query_api = client.query_api()

# Query the database and get the results in CSV format
csv_result = query_api.query_csv('from(bucket:"plant_monitoring") |> range(start: -30d)')

# Open a CSV file to write the results
with open('influxdb_query_results.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write each row to the CSV file
    for row in csv_result:
        writer.writerow(row)

print("Data has been written to influxdb_query_results.csv")