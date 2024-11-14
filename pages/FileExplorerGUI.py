import tkinter as tk
from tkinter import filedialog, ttk
from modules.interface import page_interface
import os
from PIL import Image, ImageTk
import sqlite3
import math

class FileExplorerGUI(page_interface):
    def __init__(self, parent_frame):
        super().__init__(parent_frame)
        self.inputs_db = DBManager("modules/inputs.sqlite")
        self.folder_path = tk.StringVar()
        self.folder_path.set(self.inputs_db.get_folder_name())
        self.image_processor = ImageProcessor()
        self.thumbnails = {}
        self.current_image = None
        self.grid_mode = tk.BooleanVar(value=True)
        self.images_per_row = tk.IntVar(value=3)
        self.grid_photos = []
        self.original_image = None

    def create_content(self):
        super().create_content()
        self.frame_content.pack(fill=tk.BOTH, expand=True)

        self.paned_window = tk.PanedWindow(self.frame_content, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        lframe = tk.Frame(self.paned_window)
        self.paned_window.add(lframe)

        self.file_listbox = tk.Listbox(lframe, width=30)
        self.file_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
        self.file_listbox.bind('<<ListboxSelect>>', self.on_select_file)

        button_frame = tk.Frame(lframe)
        button_frame.pack(fill=tk.X, pady=5)

        tk.Button(button_frame, text="フォルダを選択", command=self.select_folder).pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(button_frame, text="Grid表示", variable=self.grid_mode, command=self.toggle_display_mode).pack(side=tk.LEFT)

        self.slider = ttk.Scale(lframe, from_=1, to=10, orient=tk.HORIZONTAL, variable=self.images_per_row, command=self.update_grid)
        self.slider.pack(fill=tk.X, pady=5)

        self.folder_label = tk.Label(lframe, text=self.folder_path.get())
        self.folder_label.pack(pady=5)

        self.image_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.image_frame)

        self.image_canvas = tk.Canvas(self.image_frame)
        self.image_canvas.pack(fill=tk.BOTH, expand=True)

        self.update_file_list()
        self.frame_content.bind('<Configure>', self.on_resize)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            self.inputs_db.set_folder_name(folder)
            self.folder_label.config(text=folder)
            self.update_file_list()

    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        self.thumbnails.clear()
        if self.folder_path.get():
            files = self.image_processor.get_image_files(self.folder_path.get())
            for file in files:
                self.file_listbox.insert(tk.END, file)
            
            def load_thumbnails(index=0):
                if index < len(files):
                    self.load_thumbnail(files[index])
                    self.frame_content.after(10, lambda: load_thumbnails(index + 1))
                else:
                    self.display_images()
            
            load_thumbnails()

    def load_thumbnail(self, filename):
        if filename not in self.thumbnails:
            file_path = os.path.join(self.folder_path.get(), filename)
            self.thumbnails[filename] = self.image_processor.load_image(file_path, (100, 100))

    def on_select_file(self, event):
        if self.file_listbox.curselection():
            file_name = self.file_listbox.get(self.file_listbox.curselection())
            if not self.grid_mode.get():
                self.show_image(file_name)

    def show_image(self, file_name):
        file_path = os.path.join(self.folder_path.get(), file_name)
        self.original_image = Image.open(file_path)
        self.display_image()

    def display_image(self):
        if self.original_image:
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()

            img_width, img_height = self.original_image.size
            ratio = min(canvas_width/img_width, canvas_height/img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)

            resized_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
            self.current_image = ImageTk.PhotoImage(resized_image)

            self.image_canvas.delete("all")
            x = canvas_width // 2
            y = canvas_height // 2
            self.image_canvas.create_image(x, y, anchor=tk.CENTER, image=self.current_image)

    def display_images(self):
        self.image_canvas.delete("all")
        if self.grid_mode.get():
            self.display_grid_images()
        else:
            self.display_image()

    def display_grid_images(self):
        canvas_width = max(1, self.image_canvas.winfo_width())
        canvas_height = max(1, self.image_canvas.winfo_height())
        images_per_row = max(1, self.images_per_row.get())
        image_size = max(1, canvas_width // images_per_row)

        self.grid_photos = []  # 画像の参照を保持するリスト
        x, y = 0, 0
        for filename, img in self.thumbnails.items():
            resized_img = img.copy()
            resized_img.thumbnail((image_size, image_size), Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_img)
            self.grid_photos.append(photo)  # 参照を保持
            self.image_canvas.create_image(x, y, anchor=tk.NW, image=photo)

            x += image_size
            if x + image_size > canvas_width:
                x = 0
                y += image_size
            
            if y > canvas_height:
                break  # キャンバスが縦に埋まったら停止

        x, y = 0, 0
        for filename, img in self.thumbnails.items():
            resized_img = img.copy()
            resized_img.thumbnail((image_size, image_size), Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_img)
            self.image_canvas.create_image(x, y, anchor=tk.NW, image=photo)
            self.image_canvas.image = photo

            x += image_size
            if x + image_size > canvas_width:
                x = 0
                y += image_size
            
            if y > canvas_height:
                break  # Stop if we've filled the canvas vertically

    def toggle_display_mode(self):
        self.display_images()

    def update_grid(self, event=None):
        if self.grid_mode.get():
            self.display_grid_images()

    def on_resize(self, event):
        self.display_images()

class ImageProcessor:
    SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')

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
        self.query("UPDATE inputs SET data = ? WHERE name = 'foldername'", (folder_name,))

    def __del__(self):
        self.conn.close() 
        
        
