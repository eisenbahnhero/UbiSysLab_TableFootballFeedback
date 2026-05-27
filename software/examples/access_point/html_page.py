import socket

def html_page():
    return """<!DOCTYPE html>
    <html>
    <head>
        <title>Kicker TFF Interface</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial; text-align: center; margin-top: 10px; background-color: #222; color: white;}
            .btn { display: block; width: 90%; max-width: 350px; padding: 15px; margin: 8px auto; 
                   font-size: 18px; color: white; border: none; border-radius: 8px; cursor: pointer;}
            .btn:active { opacity: 0.7; }
            .btn-green { background-color: #28a745; }
            .btn-blue { background-color: #007bff; }
            .btn-red { background-color: #dc3545; }
            .btn-yellow { background-color: #ffc107; color: black; }
            .btn-purple { background-color: #6f42c1; }
        </style>
    </head>
    <body>
        <h1>TFF Controller</h1>
        <form action="/anpfiff"><button class="btn btn-green">Anpfiff Pfeife</button></form>
        <form action="/jubel"><button class="btn btn-green">Tor Jubel</button></form>
        <form action="/awww"><button class="btn btn-green">Awww (Schade)</button></form>
        <hr style="border-color: #444; width: 80%;">
        <form action="/ger"><button class="btn btn-blue">Hymne DE</button></form>
        <form action="/fcb"><button class="btn btn-blue">Hymne FC Bayern</button></form>
        <hr style="border-color: #444; width: 80%;">
        <form action="/laola"><button class="btn btn-red">Laola Welle</button></form>
        <form action="/schiri"><button class="btn btn-red">Schiri, der hat schon Gelb!</button></form>
        <form action="/boo"><button class="btn btn-red">Boo (Ausbuhen)</button></form>
        <form action="/grillen"><button class="btn btn-red">Grillen Zirpen</button></form>
    </body>
    </html>
    """

CLK  = Pin(13, Pin.OUT)  # SCL
DATA = Pin(12, Pin.OUT)  # SDA
CLK.high()
DATA.low()

player_vl = DFPlayer(uart_id=0, tx=16, rx=17)
player_hl = DFPlayer(uart_id=1, tx=4, rx=5)   
player_vl.volume(20)
player_hl.volume(20)

SLAVE_ADRESSE = 0x41
HALB = 200

CMD_ANPFIFF   = 0x10
CMD_JUBEL     = 0x11
CMD_AWWW      = 0x12
CMD_HYMNE_GER = 0x20
CMD_HYMNE_FCB = 0x21
CMD_SCHIRI    = 0x40
CMD_BOO       = 0x41
CMD_GRILLEN   = 0x42

# Spezielle Befehle für Laola
CMD_LAOLA_HR  = 0x31
CMD_LAOLA_VR  = 0x32

def spiele_anpfiff():
    player_vl.play_folder(1, 1)
    player_hl.play_folder(1, 1)
    sende(SLAVE_ADRESSE, CMD_ANPFIFF)

def spiele_jubel():
    player_vl.play_folder(1, 2)
    player_hl.play_folder(1, 2)
    sende(SLAVE_ADRESSE, CMD_JUBEL)

def spiele_awww():
    player_vl.play_folder(1, 3)
    player_hl.play_folder(1, 3)
    sende(SLAVE_ADRESSE, CMD_AWWW)

def spiele_hymne_ger():
    player_vl.play_folder(2, 1)
    player_hl.play_folder(2, 1)
    sende(SLAVE_ADRESSE, CMD_HYMNE_GER)

def spiele_hymne_fcb():
    player_vl.play_folder(2, 2)
    player_hl.play_folder(2, 2)
    sende(SLAVE_ADRESSE, CMD_HYMNE_FCB)

def spiele_schiri():
    player_vl.play_folder(4, 1)
    player_hl.play_folder(4, 1)
    sende(SLAVE_ADRESSE, CMD_SCHIRI)

def spiele_boo():
    player_vl.play_folder(4, 2)
    player_hl.play_folder(4, 2)
    sende(SLAVE_ADRESSE, CMD_BOO)

def spiele_grillen():
    player_vl.play_folder(4, 3)
    player_hl.play_folder(4, 3)
    sende(SLAVE_ADRESSE, CMD_GRILLEN)

def spiele_laola_welle():
    # Sequentielles Abspielen
    player_vl.play_folder(3, 1)
    utime.sleep_ms(300)
    player_hl.play_folder(3, 1)
    utime.sleep_ms(300)
    sende(SLAVE_ADRESSE, CMD_LAOLA_HR)
    utime.sleep_ms(300)
    sende(SLAVE_ADRESSE, CMD_LAOLA_VR)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
s.settimeout(0.2)

utime.sleep(2) 
print("System bereit. Warte auf Eingabe...")

while True:
    try:
        conn, addr = s.accept()
        request = conn.recv(1024).decode('utf-8')
        
        led.on()
        if '/anpfiff' in request:
            print("Web: Anpfiff")
            spiele_anpfiff()
            
        elif '/jubel' in request:
            print("Web: Jubel")
            spiele_jubel()
            
        elif '/awww' in request:
            print("Web: Awww")
            spiele_awww()
            
        elif '/ger' in request:
            print("Web: Hymne DE")
            spiele_hymne_ger()
            
        elif '/fcb' in request:
            print("Web: Hymne FCB")
            spiele_hymne_fcb()
            
        elif '/laola' in request:
            print("Web: Laola")
            spiele_laola_welle()
            
        elif '/schiri' in request:
            print("Web: Schiri")
            spiele_schiri()
            
        elif '/boo' in request:
            print("Web: Boo")
            spiele_boo()
            
        elif '/grillen' in request:
            print("Web: Grillen")
            spiele_grillen()
            
        response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n' + hole_html()
        conn.sendall(response.encode('utf-8'))
        conn.close()
        led.off()
        
    except OSError:
        pass