import time
from machine import Pin
from dfplayer import DFPlayer
from accesspoint import AccessPoint

# Create WLAN Access Point
wap = AccessPoint(password="kicker1234", essid="Kicker-TFF")
wap.wap_create()
wap.server_start()

# Hardware & Kommunikation
CLK  = Pin(12, Pin.OUT)
DATA = Pin(13, Pin.OUT)
CLK.high()
DATA.low()

led = Pin("LED", Pin.OUT)
led.off()

player_vl = DFPlayer(uart_id=0, tx=16, rx=17)
player_hl = DFPlayer(uart_id=1, tx=4, rx=5)   
player_vl.volume(20)
player_hl.volume(20)

SLAVE_1 = 0x41
SLAVE_2 = 0x42
HALB = 200

# Befehle
CMD_ANPFIFF   = 0x10
CMD_JUBEL     = 0x11
CMD_AWWW      = 0x12
CMD_GOAL      = 0x13
CMD_HYMNE_GER = 0x20
CMD_HYMNE_FCB = 0x21
CMD_LAOLA_HR  = 0x31
CMD_LAOLA_VR  = 0x32
CMD_SCHIRI    = 0x40
CMD_BOO       = 0x41
CMD_GRILLEN   = 0x42

def _bit_senden(bit: int):
    DATA.value(bit)
    time.sleep_us(HALB)
    CLK.high()
    time.sleep_us(HALB)
    CLK.low()
    time.sleep_us(HALB)

def _byte_senden(byte: int):
    for i in range(7, -1, -1):
        _bit_senden((byte >> i) & 1)

def sende(adresse: int, befehl: int):
    CLK.low()
    DATA.low()
    time.sleep_us(500)
    _byte_senden(adresse)
    _byte_senden(befehl)
    DATA.low()
    CLK.high()
    time.sleep_us(300)

# Sound Steuerung
# Ordner 1
def spiele_anpfiff():
    player_vl.play_folder(1, 1)
    player_hl.play_folder(1, 1)
    sende(SLAVE_1, CMD_ANPFIFF)
    sende(SLAVE_2, CMD_ANPFIFF)

def spiele_jubel():
    player_vl.play_folder(1, 2)
    player_hl.play_folder(1, 2)
    sende(SLAVE_1, CMD_JUBEL)
    sende(SLAVE_2, CMD_JUBEL)

def spiele_awww():
    player_vl.play_folder(1, 3)
    player_hl.play_folder(1, 3)
    sende(SLAVE_1, CMD_AWWW)
    sende(SLAVE_2, CMD_AWWW)

def spiele_goal():
    player_vl.play_folder(1, 4)
    player_hl.play_folder(1, 4)
    sende(SLAVE_1, CMD_GOAL)
    sende(SLAVE_2, CMD_GOAL)

# Ordner 2
def spiele_hymne_ger():
    player_vl.play_folder(2, 1)
    player_hl.play_folder(2, 1)
    sende(SLAVE_1, CMD_HYMNE_GER)
    sende(SLAVE_2, CMD_HYMNE_GER)

def spiele_hymne_fcb():
    player_vl.play_folder(2, 2)
    player_hl.play_folder(2, 2)
    sende(SLAVE_1, CMD_HYMNE_FCB)
    sende(SLAVE_2, CMD_HYMNE_FCB)

# Ordner 3
def spiele_laola_welle():
    player_vl.play_folder(3, 1)
    time.sleep_ms(300)
    player_hl.play_folder(3, 1)
    time.sleep_ms(300)
    sende(SLAVE_1, CMD_LAOLA_HR)
    time.sleep_ms(300)
    sende(SLAVE_1, CMD_LAOLA_VR)
    time.sleep_ms(300)
    sende(SLAVE_2, CMD_LAOLA_HR)
    time.sleep_ms(300)
    sende(SLAVE_2, CMD_LAOLA_VR)

# Ordner 4
def spiele_boo():
    player_vl.play_folder(4, 1)
    player_hl.play_folder(4, 1)
    sende(SLAVE_1, CMD_BOO)
    sende(SLAVE_2, CMD_BOO)

def spiele_grillen():
    player_vl.play_folder(4, 2)
    player_hl.play_folder(4, 2)
    sende(SLAVE_1, CMD_GRILLEN)
    sende(SLAVE_2, CMD_GRILLEN)

def spiele_schiri():
    player_vl.play_folder(4, 3)
    player_hl.play_folder(4, 3)
    sende(SLAVE_1, CMD_SCHIRI)
    sende(SLAVE_2, CMD_SCHIRI)


time.sleep(2) 
print("System bereit. Warte auf Eingabe...")

while True:
    conn, request = wap.handle_request()
    if request:
        led.on()
        print("Anfrage erhalten:")
        print(request)

        wap.send_response(conn)
        led.off()