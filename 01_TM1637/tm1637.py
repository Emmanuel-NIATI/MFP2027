from microbit import *
from time import sleep_us

"""

    Micro:bit

    Pin Type    Function

    0   Touch   Pad 0
    1   Touch   Pad 1
    2   Touch   Pad 2
    3   Analog  Column 1
    4   Analog  Column 2
    5   Digital Button A
    6   Digital Column 9
    7   Digital Column 8
    8   Digital
    9   Digital Column 7
    10  Analog  Column 3
    11  Digital Button B
    12  Digital
    13  Digital SPI SCK
    14  Digital SPI MISO
    15  Digital SPI MOSI
    16  Digital
    19  Digital I2C SCL
    20  Digital I2C SDA

"""

"""

    Afficheur 7 segments

     ---A---             ---A---             ---A---             ---A---
    |       |           |       |           |       |           |       |
    | F     | B         | F     | B         | F     | B         | F     | B
    |       |           |       |     O     |       |           |       |
     ---G---             ---G---      H(5)   ---G---             ---G---
    |       |           |       |     O     |       |           |       |
    | E     | C         | E     | C   H(6)  | E     | C         | E     | C
    |       |           |       |           |       |           |       |
     ---D---    O        ---D---    O        ---D---    O        ---D---    O
                H                   H                   H                   H 
     
    data[i] = 0bHGFEDCBA
    i ! 0 -> 6

"""

class TM1637(object):

    NUMBER_TO_HEX = {

        -1: 0x00,
        0: 0x3f,
        1: 0x06,
        2: 0x5b,
        3: 0x4f,
        4: 0x66,
        5: 0x6d,
        6: 0x7d,
        7: 0x07,
        8: 0x7f,
        9: 0x6f,

    }

    DIGIT_TO_HEX = {

        ' ': 0x00,
        '0': 0x3f,
        '1': 0x06,
        '2': 0x5b,
        '3': 0x4f,
        '4': 0x66,
        '5': 0x6d,
        '6': 0x7d,
        '7': 0x07,
        '8': 0x7f,
        '9': 0x6f,
        'a': 0x77,
        'b': 0x7C,
        'c': 0x58,
        'd': 0x5E,
        'h': 0x74,
        'I': 0x06,
        'l': 0x06,
        'n': 0x54,
        'o': 0x5c,
        'r': 0x50,
        'A': 0x77,
        'B': 0x7f,
        'C': 0x39,
        'D': 0x3f,
        'E': 0x79,
        'F': 0x71,
        'G': 0x7d,
        'H': 0x76,
        'I': 0x06,
        'J': 0x1f,
        'K': 0x76,
        'L': 0x38,
        'n': 0x54,
        'O': 0x3f,
        'P': 0x73,
        'S': 0x6d,
        'T': 0x00,
        'U': 0x3e,
        'V': 0x3e,
        'Y': 0x66,
        'Z': 0x5b,

    }

    DIGIT_TO_SEGMENT = [
        0b00111111,  # 0
        0b00000110,  # 1
        0b01011011,  # 2
        0b01001111,  # 3
        0b01100110,  # 4
        0b01101101,  # 5
        0b01111101,  # 6
        0b00000111,  # 7
        0b01111111,  # 8
        0b01101111,  # 9
        0b01110111,  # A
        0b01111100,  # b
        0b00111001,  # C
        0b01011110,  # d
        0b01111001,  # E
        0b01110001   # F
    ]

    COMMAND_DATA = 0x40                 # command data
    COMMAND_ADDRESS = 0xC0              # command address
    COMMAND_DISPLAY_CONTROL = 0x80      # command display control
    COMMAND_DISPLAY_BRIGHTNESS = 0x88   # command display brightness

    TM1637_DSP_ON = 0x08                # display on
    TM1637_DSP_OFF = 0x00               # display off

    TM1637_DELAY = 10                   # 10us delay between clk/dio pulses

    NONE_SEGMENT = 0x00
    DIGIT_SPACE = ' '
    NUMBER_NULL = -1

    DATA_CLEAR = (NONE_SEGMENT, NONE_SEGMENT, NONE_SEGMENT, NONE_SEGMENT, NONE_SEGMENT, NONE_SEGMENT)

    def __init__(self, clk, dio, brightness):

        assert 0 <= brightness <= 7

        self._clk = clk
        self._dio = dio
        self._brightness = brightness
                        
        self._display_status = self.TM1637_DSP_ON
        self._current_data = self.DATA_CLEAR
        
        sleep_us(self.TM1637_DELAY)

        # self._start()
        # self._stop()
        # self._cmd_data()
        # self._dsp_ctrl()
        # self._refresh()
        # self._enable()
        # self._disable()
        # self._write_byte()
        # self.set_brightness()
        # self.show_data()
        # self.show_double_point()
        # self.hide_double_point()
        # self.show_digit()
        # self.clear()
        # self.scroll_digit()
        # self.show_number()
        # self.show_binary()


    def _start(self):

        self._clk.write_digital(True)
        self._dio.write_digital(True)
        self._clk.write_digital(False)
        self._dio.write_digital(False)


    def _stop(self):
            
        self._clk.write_digital(False)
        self._dio.write_digital(False)
        self._clk.write_digital(True)
        self._dio.write_digital(True)


    def _cmd_data(self):

        self._start()
        self._write_byte(self.COMMAND_DATA)
        self._stop()


    def _dsp_ctrl(self):

        self._start()
        self._write_byte(self.COMMAND_DISPLAY_BRIGHTNESS | self._brightness)
        self._stop()


    def _refresh(self):

        self.show_data(self._current_data)

        
    def _enable(self):

        self._display_status = self.TM1637_DSP_ON
        self._refresh()

    def _disable(self):
            
        self._display_status = self.TM1637_DSP_OFF
        self._refresh()


    def set_brightness(self, brightness):

        assert 0 <= brightness <= 7
        self._brightness = brightness
        self._refresh()

    def _write_byte(self, byte):

        for i in range(0, 8):

            if byte & 0x01:
                self._dio.write_digital(True)
            else:
                self._dio.write_digital(False)
                
            byte >> i
            
            sleep_us(self.TM1637_DELAY)
            self._clk.write_digital(True)
            sleep_us(self.TM1637_DELAY)
            self._clk.write_digital(False)
            sleep_us(self.TM1637_DELAY)

        self._clk.write_digital(False)
        sleep_us(self.TM1637_DELAY)
        self._clk.write_digital(True)
        sleep_us(self.TM1637_DELAY)
        self._clk.write_digital(False)
        sleep_us(self.TM1637_DELAY)


    def show_data(self, data):
            
        self._current_data = tuple(data)
        self._cmd_data()

        self._start()
        self._write_byte(self.COMMAND_ADDRESS)
            
        for i in range(6):
            self._write_byte(data[i])
        
        self._stop()

        self._start()
        self._write_byte(self.COMMAND_DISPLAY_CONTROL | self.TM1637_DSP_ON | self._brightness)
        self._stop()
        
        
    def show_double_point(self):
            
        double_point_show_data = 0b10000000
            
        self._current_data = (  self._current_data[0],
                                self._current_data[1],
                                self._current_data[2],
                                self._current_data[3],
                                self._current_data[4] | double_point_show_data,
                                self._current_data[5] | double_point_show_data)
        self._refresh()


    def hide_double_point(self):
            
        double_point_hide_data = 0b01111111
        self._current_data = (  self._current_data[0],
                                self._current_data[1],
                                self._current_data[2],
                                self._current_data[3],
                                self._current_data[4] & double_point_hide_data,
                                self._current_data[5] & double_point_hide_data )
        self._refresh()


    def show_digit(self, data):

        data_0 = ' '
        data_1 = ' '
        data_2 = ' '
        data_3 = ' '
        data_4 = ' '
        data_5 = ' '
            
        if data[0] in self.DIGIT_TO_HEX:
            data_0 = data[0]

        if data[1] in self.DIGIT_TO_HEX:
            data_1 = data[1]

        if data[2] in self.DIGIT_TO_HEX:
            data_2 = data[2]

        if data[3] in self.DIGIT_TO_HEX:
            data_3 = data[3]

        encoded_data = (    self.DIGIT_TO_HEX[data_0],
                            self.DIGIT_TO_HEX[data_1],
                            self.DIGIT_TO_HEX[data_2],
                            self.DIGIT_TO_HEX[data_3],
                            self.DIGIT_TO_HEX[data_4],
                            self.DIGIT_TO_HEX[data_5] )

        self.show_data(encoded_data)


    def clear(self):

        self.show_digit(self.DATA_CLEAR)


    def scroll_digit(self, data, delay):

        str_data = str(data)
        k = len(str_data)


    def show_number(self, data):

        data_0 = -1
        data_1 = -1
        data_2 = -1
        data_3 = -1
        data_4 = -1
        data_5 = -1

        if data[0] in self.NUMBER_TO_HEX:
            data_0 = data[0]

        if data[1] in self.NUMBER_TO_HEX:
            data_1 = data[1]

        if data[2] in self.NUMBER_TO_HEX:
            data_2 = data[2]

        if data[3] in self.NUMBER_TO_HEX:
            data_3 = data[3]

        encoded_data = (    self.NUMBER_TO_HEX[data_0],
                            self.NUMBER_TO_HEX[data_1],
                            self.NUMBER_TO_HEX[data_2],
                            self.NUMBER_TO_HEX[data_3],
                            self.NUMBER_TO_HEX[data_4],
                            self.NUMBER_TO_HEX[data_5] )

        self.show_data(encoded_data)


    def show_binary(self, data):

        data_0 = 0b00000000
        data_1 = 0b00000000
        data_2 = 0b00000000
        data_3 = 0b00000000
        data_4 = 0b00000000
        data_5 = 0b00000000

        data_0 = data[0]
        data_1 = data[1]
        data_2 = data[2]
        data_3 = data[3]
        data_4 = data[4]
        data_5 = data[5]

        encoded_data = (    data_0,
                            data_1,
                            data_2,
                            data_3,
                            data_4,
                            data_5 )

        self.show_data(encoded_data)

