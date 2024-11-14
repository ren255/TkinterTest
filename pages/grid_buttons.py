import tkinter as tk
from modules.interface import page_interface

class grid_buttons(page_interface):
    def __init__(self,parent_frame):
        super().__init__(parent_frame)
        
    def create_content(self):
        super().create_content()
        FrameRight = tk.Frame(
            self.parent_frame,
            padx=50,
            pady=10
        )
        FrameRight.place(
            relwidth=0.4,
            relx=0,
        )
        
        FrameLeft = tk.Frame(
            self.parent_frame,
            padx=50,
            pady=10,
        )
        FrameLeft.place(
            relwidth=.6,
            relx=.4,
        )
        
        tk.Label(
            FrameRight,
            text="frame_content page 2",
        ).pack()
        
        for i in range(25):
            tk.Label(
                FrameRight,
                text=f"Label{i**5//3-i*10}",
                bg="light yellow"
            ).pack(fill=tk.X,pady=5)
        
        for i in range(20):
            frameButton = tk.Frame(
                FrameLeft,
            )
            frameButton.pack(side="top",pady=5)
            for i in range (5):
                tk.Button(
                    frameButton,
                    text=f"Button {i}",
                ).pack(fill=tk.Y,side="left",padx=5)

    def text(self):
        self.frame_text = tk.Frame(
            self.frame_body,
        )
        self.frame_text.pack(expand=True)
        
        for i in range(10):
            tk.Label(
                text=f"label {i}",
                bg="green"
            ).pack(anchor="w")