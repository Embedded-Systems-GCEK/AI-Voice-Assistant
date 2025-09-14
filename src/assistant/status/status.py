
import urllib.request
import threading


        
class Status:
    def __init__(self):
        self.connected = False
        thread = threading.Thread(target=self.update_is_connected)
        thread.daemon = True
        thread.start()
        self._available = False

    """TODO: Implement a way to check if the assistant is available
    It should be available if it does not talking to a user and is initialized
    2. Not Available only when its speaking.
    """    
 
    @property
    def available(self) -> bool:
        return self._available
    @available.setter
    def available(self, value: bool) -> None:
        self._available = value
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
            

class newStatus(Status):
    def __init__(self):
        super().__init__()
        self.battery_level = 100  # Placeholder for battery level
    @property
    def battery(self) -> int:
        return self.battery_level
    @battery.setter
    def battery(self, value: int) -> None:
        self.battery_level = value