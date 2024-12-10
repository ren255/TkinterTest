import tkinter as tk
from tkinter import filedialog, ttk
from modules.interface import page_interface
import os
from PIL import Image, ImageTk
import sqlite3

from modules.myTkObject import Scalable_Frame
import time

class FileExplorerGUI(page_interface):
    def __init__(self, parent_frame):
        super().__init__(parent_frame)
        self.inputs_db = DBManager("modules/inputs.sqlite")
        self.folder_path = tk.StringVar()
        self.folder_path.set(self.inputs_db.get_folder_name())
        self.image_processor = ImageProcessor()
        self.thumbnails = {}
        self.images_per_row = tk.IntVar(value=3)
        
        self.update_images()

    def create_content(self):
        super().create_content()
        self.create_sidebar()
        self.create_image_grid()

    def create_image_grid(self):
        self.image_grid = Scalable_Frame(self.frame_content)
        self.frame_content.update()
        self.update_imageGUI()

    def create_sidebar(self):
        self.sidebar = tk.Frame(self.frame_content)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.file_listbox = tk.Listbox(self.sidebar, width=30)
        self.file_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
        self.file_listbox.bind("<<ListboxSelect>>", self.on_select_file)

        control_frame = tk.Frame(self.sidebar)
        control_frame.pack(fill=tk.X, pady=5)

        tk.Button(
            control_frame, text="フォルダを選択", command=self.select_folder
        ).pack(side=tk.LEFT, padx=5)

        self.images_per_row_slider = ttk.Scale(
            self.sidebar,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            variable=self.images_per_row,
            command=self.display_grid_images,
        )
        self.images_per_row_slider.pack(fill=tk.X, pady=5)

        self.folder_label = tk.Label(
            self.sidebar, text=self.folder_path.get(), wraplength=200
        )
        self.folder_label.pack(pady=5)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            self.inputs_db.set_folder_name(folder)
            self.folder_label.config(text=folder)
            self.update_images()
            self.update_imageGUI()

    def update_images(self):
        self.thumbnails.clear()
        files = self.image_processor.get_image_files(self.folder_path.get())
        
        for filename in files:
            file_path = os.path.join(self.folder_path.get(), filename)
            # サムネイルを生成し、辞書に保存
            thumbnail = self.image_processor.load_image(file_path, (100, 100))
            self.thumbnails[filename] = thumbnail

    def update_imageGUI(self):
        self.file_listbox.delete(0, tk.END)
        for image in self.thumbnails:
            self.file_listbox.insert(tk.END, image)
        self.display_grid_images()
        
    def on_select_file(self, event):
        if self.file_listbox.curselection():
            file_name = self.file_listbox.get(self.file_listbox.curselection())
            # 画像表示機能を削除しました

    def display_grid_images(self,event=None):
        for widget in self.image_grid.winfo_children():
            widget.destroy()

        grid_width = self.image_grid.winfo_width()
        images_per_row = max(1, self.images_per_row.get())
        image_size = max(1, grid_width // images_per_row)

        row = 0
        col = 0
        for filename, img in self.thumbnails.items():
            resized_img = img.copy()
            resized_img.thumbnail((image_size, image_size), Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_img)

            # ボタンのスタイルを調整し、凹み風にしない
            button_style = {
                "borderwidth": 0,
                "highlightthickness": 0,
                "bg": "white",  
                "activebackground": "white", 
            }

            button = tk.Button(
                self.image_grid,
                width=image_size,
                height=image_size,
                image=photo,
                **button_style
            )

            button.image = photo  # 参照を保持
            button.grid(row=row, column=col, padx=2, pady=2)

            col += 1
            if col >= images_per_row:
                col = 0
                row += 1


class ImageProcessor:
    SUPPORTED_FORMATS = (".png", ".jpg", ".jpeg", ".gif", ".bmp")

    @staticmethod
    def is_image_file(filename):
        return filename.lower().endswith(ImageProcessor.SUPPORTED_FORMATS)

    @staticmethod
    def get_image_files(folder_path):
        return [f for f in os.listdir(folder_path) if ImageProcessor.is_image_file(f)]

    @staticmethod
    def load_image(image_path, max_size=None):
        with Image.open(image_path) as img:
            if max_size:
                img.thumbnail(max_size, Image.LANCZOS)
            return img  # PIL Imageオブジェクトを返す


class DBManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def query(self, query_string, parameters=()):
        self.cursor.execute(query_string, parameters)
        self.conn.commit()
        return self.cursor.fetchall()

    def get_folder_name(self):
        result = self.query("SELECT data FROM inputs WHERE name = 'foldername'")
        return result[0][0] if result else ""

    def set_folder_name(self, folder_name):
        self.query(
            "UPDATE inputs SET data = ? WHERE name = 'foldername'", (folder_name,)
        )

    def __del__(self):
        self.conn.close()


class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        """タイマーを開始します。"""
        self.start_time = time.time()

    def end(self):
        """タイマーを終了します。"""
        if self.start_time is None:
            print("Timer has not been started.")
            return
        self.end_time = time.time()

    def printT(self):
        """経過時間を表示します。"""
        if self.start_time is None:
            print("Timer has not been started.")
            return
        if self.end_time is None:
            print("Timer is still running.")
            elapsed_time = time.time() - self.start_time
        else:
            elapsed_time = self.end_time - self.start_time
        
        print(f"Elapsed time: {elapsed_time:.2f} seconds")