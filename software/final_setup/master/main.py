import time
from machine import Pin
from dfplayer import DFPlayer
from access_point import AccessPoint
from master_comm import MasterComm

# Create WLAN Access Point
wap = AccessPoint(password="kicker1234", essid="Kicker-TFF")
wap.wap_create()
wap.server_start()

# Communication with Slaves
master = MasterComm(clk_pin=12, data_pin=13)
SLAVES = [0x41, 0x42]                           # Adjust here the slave addresses

# Build-in LED
led = Pin("LED", Pin.OUT)
led.off()

# DFPlayer
player_1 = DFPlayer(uart_id=0, tx=16, rx=17)
player_1.volume(20)
player_2 = DFPlayer(uart_id=1, tx=4, rx=5)   
player_2.volume(20)

# Commands
CMD = {
    'ANPFIFF':      0x10,
    'JUBEL':        0x11,
    'AWWW':         0x12,
    'GOAL':         0x13,
    'HYMNE_GER':    0x20,
    'HYMNE_FCB':    0x21,
    'LAOLA_HR':     0x31,
    'LAOLA_VR':     0x32,
    'SCHIRI':       0x40,
    'BOO':          0x41,
    'GRILLEN':      0x42,
    'VOLUME_5':     0x60,
    'VOLUME_10':    0x61,
    'VOLUME_15':    0x62,
    'VOLUME_20':    0x63,
    'VOLUME_25':    0x64,
    'VOLUME_30':    0x65
}



# Sound Steuerung
# Ordner 1
def spiele_anpfiff():
    player_1.play_folder(1, 1)
    player_2.play_folder(1, 1)
    for slave in SLAVES:
        master.send(slave, CMD['ANPFIFF'])

def spiele_jubel():
    player_1.play_folder(1, 2)
    player_2.play_folder(1, 2)
    for slave in SLAVES:
        master.send(slave, CMD['JUBEL'])

def spiele_awww():
    player_1.play_folder(1, 3)
    player_2.play_folder(1, 3)
    for slave in SLAVES:
        master.send(slave, CMD['AWWW'])

def spiele_goal():
    player_1.play_folder(1, 4)
    player_2.play_folder(1, 4)
    for slave in SLAVES:
        master.send(slave, CMD['GOAL'])

# Ordner 2
def spiele_hymne_ger():
    player_1.play_folder(2, 1)
    player_2.play_folder(2, 1)
    for slave in SLAVES:
        master.send(slave, CMD['HYMNE_GER'])

def spiele_hymne_fcb():
    player_1.play_folder(2, 2)
    player_2.play_folder(2, 2)
    for slave in SLAVES:
        master.send(slave, CMD['HYMNE_FCB'])

# Ordner 3
def spiele_laola_welle():
    player_1.play_folder(3, 1)
    time.sleep_ms(300)
    player_2.play_folder(3, 1)
    time.sleep_ms(300)
    for slave in SLAVES:
        master.send(slave, CMD['LAOLA_HR'])
    time.sleep_ms(300)
    for slave in SLAVES:
        master.send(slave, CMD['LAOLA_VR'])
    time.sleep_ms(300)
    for slave in SLAVES:
        master.send(slave, CMD['LAOLA_HR'])
    time.sleep_ms(300)
    for slave in SLAVES:
        master.send(slave, CMD['LAOLA_VR'])

# Ordner 4
def spiele_boo():
    player_1.play_folder(4, 1)
    player_2.play_folder(4, 1)
    for slave in SLAVES:
        master.send(slave, CMD['BOO'])

def spiele_grillen():
    player_1.play_folder(4, 2)
    player_2.play_folder(4, 2)
    for slave in SLAVES:
        master.send(slave, CMD['GRILLEN'])

def spiele_schiri():
    player_1.play_folder(4, 3)
    player_2.play_folder(4, 3)
    for slave in SLAVES:
        master.send(slave, CMD['SCHIRI'])


def set_volume(level: int):
    if level not in [5, 10, 15, 20, 25, 30]:
        return
    print(f"Set volume to {level}")
    wap.set_volume(level)
    player_1.volume(level)
    player_2.volume(level)
    for slave in SLAVES:
        master.send(slave, CMD[f'VOLUME_{level}'])


# Loop
time.sleep(2) 
print("System bereit. Warte auf Eingabe...")

while True:
    conn, request = wap.handle_request()
    if request:
        led.on()

        if '/anpfiff' in request: spiele_anpfiff()
        elif '/jubel' in request: spiele_jubel()
        elif '/awww' in request: spiele_awww()
        elif '/goal' in request: spiele_goal()
        elif '/ger' in request: spiele_hymne_ger()
        elif '/fcb' in request: spiele_hymne_fcb()
        elif '/laola' in request: spiele_laola_welle()
        elif '/schiri' in request: spiele_schiri()
        elif '/boo' in request: spiele_boo()
        elif '/grillen' in request: spiele_grillen()
        elif '/volume' in request:
            try:
                v = int(request.split('v=')[1].split(' ')[0])
                set_volume(v)
            except:
                pass

        wap.send_response(conn)
        led.off()