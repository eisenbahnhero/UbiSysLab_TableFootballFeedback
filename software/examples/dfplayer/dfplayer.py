import time
from machine import UART, Pin

class DFPlayer:
    START  = 0x7E
    END    = 0xEF
    VER    = 0xFF
    LEN    = 0x06

    def __init__(self, uart_id=1, tx=4, rx=5, busy_pin=None):
        self.uart = UART(uart_id, baudrate=9600,
                         tx=Pin(tx), rx=Pin(rx))
        self.busy = Pin(busy_pin, Pin.IN) if busy_pin else None
        time.sleep_ms(1000) 

    def _cmd(self, cmd, param1=0, param2=0):
        buf = bytearray([
            self.START, self.VER, self.LEN,
            cmd, 0x00,         
            param1, param2,
            0x00, 0x00,         
            self.END
        ])
        chk = 0
        for b in buf[1:7]: chk += b
        chk = (-chk) & 0xFFFF
        buf[7] = (chk >> 8) & 0xFF
        buf[8] = chk & 0xFF
        self.uart.write(buf)
        time.sleep_ms(30)

    def play_track(self, track):
        #Spiele Track 1-2999
        self._cmd(0x03, 0, track)

    def play_folder(self, folder, track):
        #Spiele Ordner 1-99, Track 1-255
        self._cmd(0x0F, folder, track)

    def volume(self, vol):
        #Lautstärke 0-30
        self._cmd(0x06, 0, max(0, min(30, vol)))

    def pause(self):  self._cmd(0x0E)
    def resume(self): self._cmd(0x0D)
    def next(self):   self._cmd(0x01)
    def prev(self):   self._cmd(0x02)
    def stop(self):   self._cmd(0x16)

    def is_playing(self):
        #Busy-Pin: LOW = spielt gerade
        if self.busy: return self.busy.value() == 0
        return None