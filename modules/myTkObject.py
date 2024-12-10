
import tkinter as tk

class Scalable_Frame(tk.Frame):
    def __init__(self, parent_frame, **kwargs):
        # Canvasの作成
        self.baseframe = tk.Frame(parent_frame)
        self.baseframe.pack(side=tk.TOP,expand=True,fill=tk.BOTH)
        self.canvas = tk.Canvas(self.baseframe)
        self.scrollbar = tk.Scrollbar(self.baseframe, orient="vertical", command=self.canvas.yview)

        # tk.Frameの初期化
        super().__init__(self.canvas,**kwargs)
        self.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        
        # CanvasとScrollbarの配置
        self.canvas.create_window((0, 0), window=self, anchor="nw")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # スクロール可能なフレームの設定
        self.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # スクロールバーの設定
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # マウスホイールでのスクロール設定
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

    def on_mouse_wheel(self, event):
        """マウスホイールでのスクロール処理"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        print(f"MouseWheel {int(-1 * (event.delta / 120))}")