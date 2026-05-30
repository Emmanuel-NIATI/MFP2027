from microbit import *
from tm1637 import TM1637

# Code in a 'while True:' loop repeats forever
# while True:
    # display.show(Image.HEART)
    # sleep(1000)
    # display.scroll('Hello')

tm = TM1637(clk=pin0, dio=pin1, brightness=2)

while True:
    pin8.write_digital(True)
    sleep(200)
    pin8.write_digital(False)
    sleep(200)
