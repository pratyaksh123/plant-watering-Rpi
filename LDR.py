import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create an ADS1115 ADC (analog to digital converter) instance on the bus
ads = ADS.ADS1115(i2c)

# Create an analog input channel on pin 1 (P1)
ldr_channel = AnalogIn(ads, ADS.P1)

# Continuously read and print the voltage across the LDR
try:
    while True:
        voltage = ldr_channel.voltage
        print(f"Voltage across LDR: {voltage:.2f}V")
        time.sleep(1)
except KeyboardInterrupt:
    print("Measurement stopped by user")
