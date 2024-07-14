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
url = "http://192.168.0.214:8086"  # Ensure this is the correct IP for your InfluxDB instance

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create an ADS1115 ADC instance
ads = ADS.ADS1115(i2c, address=0x48)

# Create analog input channels
moisture_sensor = AnalogIn(ads, ADS.P0)
light_sensor = AnalogIn(ads, ADS.P1)

# Read sensors
moisture_voltage = moisture_sensor.voltage
light_voltage = light_sensor.voltage

timestamp = time.time_ns()  # Nanoseconds timestamp for InfluxDB

# Moisture Point
moisture_point = (
    Point("Sensor_Readings")
    .tag("sensor", "Moisture")
    .field("voltage", moisture_voltage)
    .time(timestamp, WritePrecision.NS)
)

# Light Point
light_point = (
    Point("Sensor_Readings")
    .tag("sensor", "Light")
    .field("voltage", light_voltage)
    .time(timestamp, WritePrecision.NS)
)

# Write data to InfluxDB
write_api.write(bucket=bucket, record=[moisture_point, light_point])

print(f"Timestamp: {timestamp}, Moisture Voltage: {moisture_voltage:.2f}V, Light Voltage: {light_voltage:.2f}V")

client.close()
