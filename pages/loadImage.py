import tkinter as tk
from modules.interface import page_interface

from tkinter import ttk

from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2


class loadImage(page_interface):
    def __init__(self, parent_frame):
        super().__init__(parent_frame)

    def create_content(self):
        super().create_content()
        self.create_widgets()
        if hasattr(self, "image_PIL"):
            self.image_tk = ImageTk.PhotoImage(
                self.image_PIL
            )  # ImageTkフォーマットへ変換
            self.canvas1.create_image(320, 240, image=self.image_tk)

    def create_widgets(self):
        # Canvas
        self.canvas1 = tk.Canvas(self.frame_content)
        self.canvas1.configure(width=640-5, height=480-5, bg="orange")
        self.canvas1.create_rectangle(0, 0, 120, 70, fill="green")
        self.canvas1.grid(column=1, row=0)
        self.canvas1.grid(padx=5, pady=5)

        # Frame
        self.frame_button = ttk.LabelFrame(self.frame_content)
        self.frame_button.configure(text=" Button Frame ")
        self.frame_button.grid(column=1, row=1)
        self.frame_button.grid(padx=5, pady=5)

        # File open and Load Image
        self.button_open = ttk.Button(self.frame_button)
        self.button_open.configure(text="Load Image")
        self.button_open.grid(column=0, row=1)
        self.button_open.configure(command=self.loadImage)

        # Clear Button
        self.button_clear = ttk.Button(self.frame_button)
        self.button_clear.configure(text="Clear Image")
        self.button_clear.grid(column=1, row=1)
        self.button_clear.configure(command=self.clearImage)

        # Quit Button
        self.button_quit = ttk.Button(self.frame_button)
        self.button_quit.config(text="Quit")
        self.button_quit.grid(column=2, row=1)
        self.button_quit.configure(command=self.quit_app)

    # Event Call Back
    def loadImage(self):

        # self.folder_name = filedialog.askdirectory()
        self.filename = filedialog.askopenfilename()
        # print(self.folder_name)
        print(self.filename)

        self.image_bgr = cv2.imread(self.filename)
        self.height, self.width = self.image_bgr.shape[:2]
        print(self.height, self.width)
        if self.width > self.height:
            self.new_size = (640, 480)
        else:
            self.new_size = (480, 480)

        self.image_bgr_resize = cv2.resize(
            self.image_bgr, self.new_size, interpolation=cv2.INTER_AREA
        )
        self.image_rgb = cv2.cvtColor(
            self.image_bgr_resize, cv2.COLOR_BGR2RGB
        )  # imreadはBGRなのでRGBに変換

        # self.image_rgb = cv2.cvtColor(self.image_bgr, cv2.COLOR_BGR2RGB) # imreadはBGRなのでRGBに変換
        self.image_PIL = Image.fromarray(self.image_rgb)  # RGBからPILフォーマットへ変換
        self.image_tk = ImageTk.PhotoImage(self.image_PIL)  # ImageTkフォーマットへ変換
        self.canvas1.create_image(320, 240, image=self.image_tk)

    def clearImage(self):
        self.canvas1.delete("all")

    def quit_app(self):
        self.Msgbox = tk.messagebox.askquestion(
            "Exit Applictaion", "Are you sure?", icon="warning"
        )
        if self.Msgbox == "yes":
            self.master.destroy()
        else:
            tk.messagebox.showinfo(
                "Return", "you will now return to application screen"
            )
