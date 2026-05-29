import time
from machine import Pin

class MasterComm:

    def __init__(self, clk_pin: int, data_pin: int, halb_us: int = 200):
        self.CLK  = Pin(12, Pin.OUT)
        self.DATA = Pin(13, Pin.OUT)
        self.CLK.high()
        self.DATA.low()
        self.HALB = 200

    def _bit_send(self, bit: int):
        self.DATA.value(bit)
        time.sleep_us(self.HALB)
        self.CLK.high()
        time.sleep_us(self.HALB)
        self.CLK.low()
        time.sleep_us(self.HALB)

    def _byte_send(self, byte: int):
        for i in range(7, -1, -1):
            self._bit_send((byte >> i) & 1)

    def send(self, adresse: int, befehl: int):
        self.CLK.low()
        self.DATA.low()
        time.sleep_us(500)
        self._byte_send(adresse)
        self._byte_send(befehl)
        self.DATA.low()
        self.CLK.high()
        time.sleep_us(300)