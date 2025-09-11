
import urllib.request
import threading
class Status:
    def __init__(self):
        self.connected = False
        thread = threading.Thread(target=self.update_is_connected)
        thread.daemon = True
        thread.start()
    @property
    def is_connected(self) -> bool:
        return self.connected
    @is_connected.setter
    def is_connected(self, value: bool) -> None:
        self.connected = value
    def update_is_connected(self) -> None:
        try:
            urllib.request.urlopen("https://www.google.com", timeout=3)
            print("Internet connection detected.")
            self.is_connected = True
        except:
            print("No internet connection.")
            self.is_connected = False