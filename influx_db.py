import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("INFLUXDB_TOKEN")
org = "Home"
url = "http://192.168.0.214:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket="Plant_monitoring"

write_api = client.write_api(write_options=SYNCHRONOUS)
   
for value in range(5):
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue1")
    .field("field1", value)
  )
  write_api.write(bucket=bucket, org="Home", record=point)
  time.sleep(1) # separate points by 1 second

query_api = client.query_api()

query = """from(bucket: "Plant_monitoring")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "measurement1")
  |> mean()"""
tables = query_api.query(query, org="Home")

for table in tables:
    for record in table.records:
        print(record)