"""
This module is used to communicate with the UI components.

"""

from assistant.status.status import Status


        
class UI:
    def __init__(self, status: Status):
        self.status = status
    
    def Run(self):
        """
        What it should do ,
        1. Start the flask server
        2. Initialize the UI components
        3. Handle user interactions
        """
        print("UI is running...")