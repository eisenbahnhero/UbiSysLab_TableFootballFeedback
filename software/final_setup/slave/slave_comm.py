import time
from machine import Pin

class SlaveComm:

    def __init__(self, clk_pin: int, data_pin: int):
        CLK  = Pin(12, Pin.IN, Pin.PULL_UP)
        DATA = Pin(13, Pin.IN, Pin.PULL_DOWN)
        self.CLK = CLK
        self.DATA = DATA
        self.TIMEOUT_US = 5_000

    def _warte_flanke(self, pin, zielwert: int) -> bool:
        t = self.TIMEOUT_US
        while pin.value() != zielwert:
            t -= 1
            if t == 0: return False
            time.sleep_us(1)
        return True

    def _warte_start(self) -> bool:
        if not self._warte_flanke(self.CLK, 0): return False
        time.sleep_us(300)
        return self.CLK.value() == 0 and self.DATA.value() == 0

    def _byte_lesen(self):
        byte = 0
        for _ in range(8):
            if not self._warte_flanke(self.CLK, 1): return None
            time.sleep_us(10)              
            byte = (byte << 1) | self.DATA.value()
            if not self._warte_flanke(self.CLK, 0): return None
        return byte
    
    def handle(self, adresse: int):
        if not self._warte_start():
            return None

        recv_adresse = self._byte_lesen()
        if recv_adresse is None or recv_adresse != adresse:
            return None

        cmd = self._byte_lesen()
        if cmd is None:
            return None
        
        return cmd