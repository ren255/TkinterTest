import tkinter as tk
from modules.interface import page_interface
from modules.mouse import mouse


class test(page_interface):
    def __init__(self, parent_frame):
        super().__init__(parent_frame)

    def create_content(self):
        super().create_content()
        self.make_canvas()
        self.CnvMgr = canvasM(self.canvas)
        self.rects()

        # 範囲選択
        self.canvas.bind("<ButtonPress-1>", self.CnvMgr.start_point_get)
        self.canvas.bind("<Button1-Motion>", self.CnvMgr.rect_drawing)

    def make_canvas(self):
        # キャンバス作成
        self.canvas = tk.Canvas(
            self.frame_content,
            width=500,
            height=300,
            highlightthickness=0,
            bg="white",
        )
        self.canvas.pack(anchor="center")

    def rects(self):
        # 色を用意
        colors = ("red", "green", "yellow", "blue", "purple", "pink", "orange")

        #  四角の数だけ適当に位置をずらしながら長方形（正方形）を描画
        for i, color in enumerate(colors):
            rect = self.canvas.create_rectangle(
                i * 60 + 20,
                20,
                i * 60 + 70,
                70,
                fill=color,
            )
            # 図形ドラッグ
            self.canvas.tag_bind(rect, "<ButtonPress-1>", self.CnvMgr.click)
            self.canvas.tag_bind(rect, "<Button1-Motion>", self.CnvMgr.drag)


class canvasM:
    def __init__(self, canvas):
        self.canvas = canvas
        self.mouse = mouse()

    def click(self, event):
        # クリックされた位置に一番近い図形のID取得
        self.selected = self.canvas.find_closest(
            *self.mouse.setpos(event),
        )

    def drag(self, event):
        # 前回からのマウスの移動量の分だけ図形も移動
        self.canvas.move(
            self.selected,
            *self.mouse.getdiff(event),
        )
        self.mouse.setpos(event)

    def start_point_get(self,event):
        self.canvas.delete("rect1")
        self.mouse.setpos(event)

    # ドラッグ中のイベント - - - - - - - - - - - - - - - - - - - - - - - - - -
    def rect_drawing(self, event):
        if self.canvas.find_withtag("rect1"):
            # "rect1"タグの画像を再描画
            self.canvas.coords(
                "rect1",
                *self.mouse.getPpos(),
                *self.mouse.getpos(event),
            )
        else:
            # canvas上に四角形を描画（rectangleは矩形の意味）
            self.canvas.create_rectangle(
                *self.mouse.getPpos(),
                *self.mouse.getpos(event),
                outline="blue",
                tag="rect1",
            )