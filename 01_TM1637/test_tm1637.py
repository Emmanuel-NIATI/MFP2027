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



tm = TM1637(clk=pin1, dio=pin2, brightness=2)

tm.show_binary([0b11111111,0b11111111,0b11111111,0b11111111,0b11111111,0b11111111])

while True:
    pin8.write_digital(True)
    sleep(200)
    pin8.write_digital(False)
    sleep(200)
