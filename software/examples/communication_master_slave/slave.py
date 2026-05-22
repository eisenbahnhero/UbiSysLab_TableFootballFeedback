from machine import Pin
import utime

SLAVE_ADRESSE = 0x41   # für Slave 2 auf 0x42 setzen

CMD_LED_AN  = 0x01
CMD_LED_AUS = 0x00

CLK  = Pin(6, Pin.IN, Pin.PULL_UP)
DATA = Pin(7, Pin.IN, Pin.PULL_DOWN)

led = Pin("LED", Pin.OUT)
led.off()

def _warte_start() -> bool:
    # Warte bis CLK LOW geht
    timeout = 50_000
    while CLK.value() == 1:
        timeout -= 1
        if timeout == 0:
            return False
        utime.sleep_us(1)

    utime.sleep_us(300)
    return CLK.value() == 0 and DATA.value() == 0

def _byte_lesen() -> int:
    byte = 0
    for _ in range(8):
        while CLK.value() == 0:
            pass
        # Bit lesen wenn CLK HIGH
        utime.sleep_us(100)
        bit = DATA.value()
        byte = (byte << 1) | bit
        while CLK.value() == 1:
            pass
    return byte


print(f"Slave bereit – Adresse: 0x{SLAVE_ADRESSE:02X}")

while True:
    if not _warte_start():
        continue

    adresse = _byte_lesen()
    befehl  = _byte_lesen()

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
