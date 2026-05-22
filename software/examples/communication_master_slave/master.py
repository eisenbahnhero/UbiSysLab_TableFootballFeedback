from machine import Pin
import utime

CLK  = Pin(12, Pin.OUT)
DATA = Pin(13, Pin.OUT)
CLK.high()
DATA.low()

SLAVE_1 = 0x41
SLAVE_2 = 0x42

CMD_LED_AN  = 0x01
CMD_LED_AUS = 0x00

HALB = 200   # Halbperiode in µs

def _bit_senden(bit: int):
    DATA.value(bit)
    utime.sleep_us(HALB)
    CLK.high()
    utime.sleep_us(HALB)
    CLK.low()
    utime.sleep_us(HALB)

def _byte_senden(byte: int):
    for i in range(7, -1, -1):      # MSB an anfang
        _bit_senden((byte >> i) & 1)

def sende(adresse: int, befehl: int):
    # trigger start
    CLK.low()
    DATA.low()
    utime.sleep_us(500)

    _byte_senden(adresse)
    _byte_senden(befehl)

    # trigger stop
    DATA.low()
    CLK.high()
    utime.sleep_us(300)


while True:
    sende(SLAVE_1, CMD_LED_AN)
    sende(SLAVE_2, CMD_LED_AN)
    utime.sleep(2)

    sende(SLAVE_1, CMD_LED_AUS)
    sende(SLAVE_2, CMD_LED_AUS)
    utime.sleep(2)
