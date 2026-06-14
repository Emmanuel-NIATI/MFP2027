from microbit import *

# Code in a 'while True:' loop repeats forever
# while True:
    # display.show(Image.HEART)
    # sleep(1000)
    # display.scroll('Hello')

while True:
    pin8.write_digital(True)
    sleep(200)
    pin8.write_digital(False)
    sleep(200)
