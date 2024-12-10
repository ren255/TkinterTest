import tkinter as tk
from modules.interface import page_interface
from modules.myTkObject import Scalable_Frame

class ScalableCanvas(page_interface):
    def __init__(self, parent_frame):
        super().__init__(parent_frame)

    def create_content(self):
        super().create_content()

        # スクロール可能なコンテンツを追加
        scrollable_frame = Scalable_Frame(self.frame_content)
        
        for i in range(50):  # 例として50個のラベルを追加
            label = tk.Label(scrollable_frame, text=f"Label {i+1}")
            label.pack(pady=5)
        
        