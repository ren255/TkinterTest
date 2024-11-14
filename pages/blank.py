import tkinter as tk
from modules.interface import page_interface

class blank(page_interface):
    def __init__(self,parent_frame):
        super().__init__(parent_frame)
        self.callback = callback()
        
    def create_content(self):
        super().create_content()

class callback(blank):
    def __init__(self):
        pass