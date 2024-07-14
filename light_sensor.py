import time
import board
import busio
import os
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

load_dotenv()

# InfluxDB settings
token = os.environ.get("INFLUXDB_TOKEN")
org = "Home"
bucket = "plant_monitoring"
url = "http://192.168.0.214:8086"

# Setup InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c, address=0x48)
light_sensor = AnalogIn(ads, ADS.P1)

# Read sensor
light_voltage = light_sensor.voltage
timestamp = time.time_ns()

# Create data point
light_point = Point("Sensor_Readings").tag("sensor", "Light").field("voltage", light_voltage).time(timestamp, WritePrecision.NS)

# Write data to InfluxDB
write_api.write(bucket=bucket, record=light_point)

print(f"Timestamp: {timestamp}, Light Voltage: {light_voltage:.2f}V")

client.close()
