from machine import Pin
import utime

SLAVE_ADRESSE = 0x41

CMD_LED_AN  = 0x01
CMD_LED_AUS = 0x00

CLK  = Pin(12, Pin.IN, Pin.PULL_UP)
DATA = Pin(13, Pin.IN, Pin.PULL_DOWN)

led = Pin("LED", Pin.OUT)
led.off()

_TIMEOUT_US = 5_000

def _warte_flanke(pin, zielwert: int) -> bool:
    t = _TIMEOUT_US
    while pin.value() != zielwert:
        t -= 1
        if t == 0:
            return False
        utime.sleep_us(1)
    return True

def _warte_start() -> bool:
    if not _warte_flanke(CLK, 0):
        return False
    utime.sleep_us(300)
    return CLK.value() == 0 and DATA.value() == 0

def _byte_lesen():
    byte = 0
    for _ in range(8):
        if not _warte_flanke(CLK, 1):   # warte CLK HIGH
            return None
        utime.sleep_us(10)              # kurz stabilisieren
        byte = (byte << 1) | DATA.value()
        if not _warte_flanke(CLK, 0):   # warte CLK LOW
            return None
    return byte

print(f"Slave bereit – Adresse: 0x{SLAVE_ADRESSE:02X}")

while True:
    if not _warte_start():
        continue

    adresse = _byte_lesen()
    if adresse is None:
        print("Timeout beim Adress-Byte – Reset")
        continue

    befehl = _byte_lesen()
    if befehl is None:
        print("Timeout beim Befehls-Byte – Reset")
        continue

    if adresse != SLAVE_ADRESSE:
        continue

    print(f"Adresse 0x{adresse:02X}  Befehl 0x{befehl:02X}")

    if befehl == CMD_LED_AN:
        led.on()
        print("LED AN")
    elif befehl == CMD_LED_AUS:
        led.off()
        print("LED AUS")
    else:
        print("Unbekannter Befehl")