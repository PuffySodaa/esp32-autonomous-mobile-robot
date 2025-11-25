from machine import I2C, Pin
import time

class LCD:
    def __init__(self, sda, scl, addr=0x27, rows=2, cols=16, freq=400000):
        self.i2c = I2C(0, scl=Pin(scl), sda=Pin(sda), freq=freq)
        self.addr = addr
        self.rows = rows
        self.cols = cols
        self.backlight = 0x08  # Backlight on
        self._init_lcd()

    def _write(self, data):
        self.i2c.writeto(self.addr, bytes([data]))

    def _pulse_enable(self, data):
        self._write(data | 0x04)  # EN = 1
        time.sleep_ms(1)
        self._write(data & ~0x04)  # EN = 0
        time.sleep_ms(1)

    def _send_nibble(self, nibble, mode):
        data = (nibble & 0xF0) | self.backlight
        if mode:
            data |= 0x01  # RS = 1 for data
        self._pulse_enable(data)

    def _send_byte(self, byte, mode=0):
        self._send_nibble(byte & 0xF0, mode)
        self._send_nibble((byte << 4) & 0xF0, mode)

    def _init_lcd(self):
        time.sleep_ms(1)
        for _ in range(3):
            self._send_nibble(0x30, 0)
            time.sleep_ms(1)
        self._send_nibble(0x20, 0)  # Set to 4-bit mode

        self._send_byte(0x28)  # Function set: 4-bit, 2 lines
        self._send_byte(0x0C)  # Display ON, cursor OFF
        self._send_byte(0x06)  # Entry mode set
        self.clear()

    def clear(self):
        self._send_byte(0x01)
        time.sleep_ms(2)

    def move_to(self, col, row):
        row_offsets = [0x00, 0x40, 0x14, 0x54]
        self._send_byte(0x80 | (col + row_offsets[row]))

    def putstr(self, string):
        for char in string:
            self._send_byte(ord(char), mode=1)
