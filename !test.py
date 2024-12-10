import tkinter as tk


class ScrollableFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # Canvasの作成
        self.canvas = tk.Canvas(self)
        self.scrollable_frame = tk.Frame(self.canvas)

        # スクロールバーの作成
        self.scrollbar = tk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # スクロール可能なフレームをCanvasに追加
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # Canvasとフレームをウィジェットとして配置
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # ウィジェットの配置
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def add_widget(self, widget):
        widget.pack(pady=10)  # ウィジェットをフレームに追加


# メインウィンドウの作成
root = tk.Tk()
root.title("Scrollable Frame Example")

# スクロール可能なフレームのインスタンスを作成
scrollable_frame = ScrollableFrame(root)
scrollable_frame.pack(fill=tk.BOTH, expand=True)

# サンプルウィジェットを追加
for i in range(30):
    label = tk.Label(scrollable_frame.scrollable_frame, text=f"Label {i+1}")
    scrollable_frame.add_widget(label)

# メインループの開始
root.mainloop()
