import network
import rp2
import socket

class AccessPoint:
    def __init__(self, password=None, essid=None):
        self.password = password
        self.essid = essid
        self._socket = None
        self._volume = "20"

    def get_html_page(self):
        with open("page.html", "r") as f:
            html = f.read()
            html = html.replace("{{VOLUME}}", self._volume)
            return html

    def set_volume(self, volume: int):
        self._volume = str(volume)

    def wap_create(self):
        rp2.country('DE')
        wap = network.WLAN(network.AP_IF)
        wap.config(essid=self.essid, password=self.password)
        wap.active(True)
        netConfig = wap.ifconfig()
        print('WLAN AP Aktiv')
        print(f'Verbinde dich mit "{self.essid}" (PW: {self.password})')
        print(f'Öffne im Browser: http://{netConfig[0]}')

    def server_start(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(('', 80))
        self._socket.listen(5)
        self._socket.settimeout(0.2)

    def handle_request(self):
        try:
            conn, addr = self._socket.accept()
            request = conn.recv(1024).decode('utf-8')
            return conn, request
        except OSError:
            return None, None

    def send_response(self, conn):
        response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n' + self.get_html_page()
        conn.sendall(response.encode('utf-8'))
        conn.close()