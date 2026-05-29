from machine import Pin
import time
from dfplayer import DFPlayer
from slave_comm import SlaveComm

# richtige Slave Adresse muss entsprechend auskommentiert werden, jenachdem auf welchem Pico sich die Datei befindet
SLAVE_ADRESSE = 0x41
# SLAVE_ADRESSE = 0x42

# Slave Communication
slave = SlaveComm(clk_pin=12, data_pin=13)

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



led = Pin("LED", Pin.OUT)
led.off()

player_1 = DFPlayer(uart_id=0, tx=16, rx=17)
player_2 = DFPlayer(uart_id=1, tx=4, rx=5)
player_1.volume(20)
player_2.volume(20)


def spiele_alle(ordner, track):
    player_1.play_folder(ordner, track)
    player_2.play_folder(ordner, track)

# Loop
print(f"Slave bereit – Adresse: 0x{SLAVE_ADRESSE:02X}")

while True:   
    ccmd = slave.handle(SLAVE_ADRESSE)
    if ccmd is None:
        continue

    print(f"Befehl erhalten: 0x{ccmd:02X}")
    led.on()
    
    if ccmd == CMD['ANPFIFF']: spiele_alle(1, 1)
    elif ccmd == CMD['JUBEL']: spiele_alle(1, 2)
    elif ccmd == CMD['AWWW']: spiele_alle(1, 3)
    elif ccmd == CMD['GOAL']: spiele_alle(1, 4)
    elif ccmd == CMD['HYMNE_GER']: spiele_alle(2, 1)
    elif ccmd == CMD['HYMNE_FCB']: spiele_alle(2, 2)
    elif ccmd == CMD['SCHIRI']: spiele_alle(4, 1)
    elif ccmd == CMD['BOO']: spiele_alle(4, 2)
    elif ccmd == CMD['GRILLEN']: spiele_alle(4, 3)
    
    elif ccmd == CMD['LAOLA_HR']: 
        player_1.play_folder(3, 1)
    elif ccmd == CMD['LAOLA_VR']: 
        player_2.play_folder(3, 1)

    elif ccmd == CMD['VOLUME_5']:
        player_1.volume(5)
        player_2.volume(5)
    elif ccmd == CMD['VOLUME_10']:
        player_1.volume(10)
        player_2.volume(10)
    elif ccmd == CMD['VOLUME_15']:
        player_1.volume(15)
        player_2.volume(15)
    elif ccmd == CMD['VOLUME_20']:
        player_1.volume(20)
        player_2.volume(20)
    elif ccmd == CMD['VOLUME_25']:
        player_1.volume(25)
        player_2.volume(25)
    elif ccmd == CMD['VOLUME_30']:
        player_1.volume(30)
        player_2.volume(30)
        
    led.off()