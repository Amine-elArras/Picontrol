import serial
import time

arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)

arduino.write(b"LED1_ON\n")
time.sleep(2)

arduino.write(b"LED1_OFF\n")
