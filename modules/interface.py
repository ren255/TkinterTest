from abc import ABC, abstractmethod
import tkinter as tk


class page_interface(ABC):
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame

    @abstractmethod
    def create_content(self,pad=0):
        self.frame_content = tk.Frame(self.parent_frame)
        self.frame_content.pack(
            expand=True,
            fill=tk.BOTH,
            padx=pad,
            pady=pad,
        )

    # Todo まだ使えない
    def built(self):
        self.destroyView()
        self.createView()
        return 

    def createView(self):
        # frameを消し、作成する。
        self.destroyView()
        self.create_content()

    def destroyView(self):
        # frameを消す
        if hasattr(self, "frame_content"):
            self.frame_content.destroy()

