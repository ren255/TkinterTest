import tkinter as tk
from modules.interface import page_interface

from modules.ImageConverter import ImageConverter as imgCon

class image_grid(page_interface):
    def __init__(self,parent_frame):
        super().__init__(parent_frame)
        
    def create_content(self):
        super().create_content()
        
        self.canvas_image = tk.Canvas(
            self.frame_content
        )
        self.canvas_image.pack()
        
        img1 = imgCon.to_pil("images/foldericon.png")
        size = (500,500)
        img1 = imgCon.resize(img1,size)
        img1 = imgCon.to_tk(img1)
        
        self.canvas_image.create_image(
            *size,
            image=img1
        )