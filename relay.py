import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)

try:
    GPIO.output(26, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(26, GPIO.LOW)
    time.sleep(5)
except KeyboardInterrupt:
    print("Program stopped")
finally:
    GPIO.cleanup()