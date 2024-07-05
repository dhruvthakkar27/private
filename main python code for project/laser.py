from periphery import GPIO
from time import sleep

laser = GPIO("/dev/gpiochip4", 12, "out")


laser.write(True)
sleep(2)
laser.write(False)
sleep(2)