import tkinter as tk
from modules.interface import page_interface


class Frame_textlist(page_interface):
    def __init__(self, parent_frame):
        super().__init__(parent_frame)
        
        self.page_model = Model_textlist(self)

    def create_content(self):
        super().create_content()
        
        self.text_list_frame()
        self.links_frame()

    def text_list_frame(self, pagei=1):

        self.pagei = pagei

        self.frame_textList = tk.Frame(self.frame_content, padx=20, pady=10)
        self.frame_textList.place(
            relwidth=0.8, relheight=1
        )

        label = tk.Label(self.frame_textList, text=f"This is sub-page {self.pagei}")
        label.pack(anchor="w", pady=10)

        v = tk.Scrollbar(self.frame_textList)
        v.pack(side=tk.RIGHT, fill=tk.Y)

        # main text list
        text = tk.Text(
            self.frame_textList, bg="light blue", wrap=tk.NONE, yscrollcommand=v.set
        )

        for i in range(50000):
            text.insert(tk.END, f"Widget {i*self.pagei}\n")

        text.pack(fill=tk.BOTH, expand=True)

        v.config(command=text.yview)

        # Page navigation buttons
        nav_frame = tk.Frame(self.frame_textList)
        nav_frame.pack(fill=tk.X, pady=10)

        tk.Button(
            nav_frame,
            text="Previous",
            command=lambda: self.page_model.change_textnum(self.pagei - 1),
        ).pack(side=tk.LEFT)

        tk.Button(
            nav_frame,
            text="Next",
            command=lambda: self.page_model.change_textnum(self.pagei + 1),
        ).pack(side=tk.RIGHT)

    def links_frame(self):
        frame_links = tk.Frame(self.frame_content, padx=5, pady=20)

        frame_links.place(
            relx=0.8,
            relwidth=0.2,
        )
        
        self.Buttons = []
        for i in range(25):
            button = tk.Button(
                frame_links,
                text=f"buttons {i+1}",
                anchor="w",
                command=lambda i=i + 1: self.page_model.change_textnum(i),
            )

            button.pack(fill=tk.X, pady=5)
            self.Buttons.append(button)
            
class Model_textlist:
    def __init__(self,page):
        self.page = page
    
    def change_textnum(self,i):
        self.page.text_list_frame(i)

