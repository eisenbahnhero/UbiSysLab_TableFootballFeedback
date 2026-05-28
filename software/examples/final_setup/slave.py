from machine import Pin
import time
from dfplayer import DFPlayer

# richtige Slave Adresse muss entsprechend auskommentiert werden, jenachdem auf welchem Pico sich die Datei befindet
SLAVE_ADRESSE = 0x41
# SLAVE_ADRESSE = 0x42

CMD_ANPFIFF   = 0x10
CMD_JUBEL     = 0x11
CMD_AWWW      = 0x12
CMD_GOAL      = 0x13
CMD_HYMNE_GER = 0x20
CMD_HYMNE_FCB = 0x21
CMD_SCHIRI    = 0x40
CMD_BOO       = 0x41
CMD_GRILLEN   = 0x42
CMD_LAOLA_HR  = 0x31
CMD_LAOLA_VR  = 0x32

# Hardware setup
CLK  = Pin(12, Pin.IN, Pin.PULL_UP)
DATA = Pin(13, Pin.IN, Pin.PULL_DOWN)

led = Pin("LED", Pin.OUT)
led.off()

player_hr = DFPlayer(uart_id=0, tx=16, rx=17)
player_vr = DFPlayer(uart_id=1, tx=4, rx=5)
player_hr.volume(25)
player_vr.volume(25)

# Kommunikation
_TIMEOUT_US = 5_000

def _warte_flanke(pin, zielwert: int) -> bool:
    t = _TIMEOUT_US
    while pin.value() != zielwert:
        t -= 1
        if t == 0: return False
        time.sleep_us(1)
    return True

def _warte_start() -> bool:
    if not _warte_flanke(CLK, 0): return False
    time.sleep_us(300)
    return CLK.value() == 0 and DATA.value() == 0

def _byte_lesen():
    byte = 0
    for _ in range(8):
        if not _warte_flanke(CLK, 1): return None
        time.sleep_us(10)              
        byte = (byte << 1) | DATA.value()
        if not _warte_flanke(CLK, 0): return None
    return byte

def spiele_alle(ordner, track):
    player_hr.play_folder(ordner, track)
    player_vr.play_folder(ordner, track)

# main loop
print(f"Slave bereit – Adresse: 0x{SLAVE_ADRESSE:02X}")

while True:
    if not _warte_start():
        continue

    adresse = _byte_lesen()
    if adresse is None or adresse != SLAVE_ADRESSE:
        continue

    befehl = _byte_lesen()
    if befehl is None:
        continue

    print(f"Befehl erhalten: 0x{befehl:02X}")
    led.on()
    
    if befehl == CMD_ANPFIFF: spiele_alle(1, 1)
    elif befehl == CMD_JUBEL: spiele_alle(1, 2)
    elif befehl == CMD_AWWW: spiele_alle(1, 3)
    elif befehl == CMD_GOAL: spiele_alle(1, 4)
    elif befehl == CMD_HYMNE_GER: spiele_alle(2, 1)
    elif befehl == CMD_HYMNE_FCB: spiele_alle(2, 2)
    elif befehl == CMD_SCHIRI: spiele_alle(4, 1)
    elif befehl == CMD_BOO: spiele_alle(4, 2)
    elif befehl == CMD_GRILLEN: spiele_alle(4, 3)
    
    elif befehl == CMD_LAOLA_HR: 
        player_hr.play_folder(3, 1)
    elif befehl == CMD_LAOLA_VR: 
        player_vr.play_folder(3, 1)
        
    led.off()