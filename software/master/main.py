from dfplayer import DFPlayer
import time

player = DFPlayer(
    uart_id=0,
    tx=16,   # GP16 = physischer Pin 21
    rx=17,   # GP17 = physischer Pin 22
)

player.volume(30)         
time.sleep_ms(200)

print("Play")
player.play_folder(1, 1)
print("Ready")
