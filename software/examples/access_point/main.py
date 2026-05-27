import network
import rp2

# WLAN Access Point einrichten
def wapCreate():
    rp2.country('DE')
    wap = network.WLAN(network.AP_IF)
    wap.config(essid='Kicker-TFF', password='kicker')
    wap.active(True)
    netConfig = wap.ifconfig()
    print('WLAN AP Aktiv')
    print('Verbinde dich mit "Kicker-TFF" (PW: kicker)')
    print('Öffne im Browser: http://' + netConfig[0])

ip_adresse = wapCreate()