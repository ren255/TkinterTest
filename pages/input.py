import tkinter as tk
from modules.interface import page_interface

class input(page_interface):
    def __init__(self,parent_frame):
        super().__init__(parent_frame)
        self.callback = callback()
        
    def create_content(self):
        super().create_content()

        # 左右のフレームを作成
        left_frame = tk.Frame(self.frame_content)
        right_frame = tk.Frame(self.frame_content)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 左フレーム（入力用ウィジェット）
        tk.Label(left_frame, text="テキスト入力:").pack(pady=5)
        self.text_input = tk.Entry(left_frame)
        self.text_input.pack(pady=5)

        tk.Label(left_frame, text="数値入力:").pack(pady=5)
        self.number_input = tk.Spinbox(left_frame, from_=0, to=100)
        self.number_input.pack(pady=5)

        tk.Label(left_frame, text="選択:").pack(pady=5)
        self.option_var = tk.StringVar(value="オプション1")
        self.option_menu = tk.OptionMenu(left_frame, self.option_var, "オプション1", "オプション2", "オプション3")
        self.option_menu.pack(pady=5)

        tk.Label(left_frame, text="チェックボックス:").pack(pady=5)
        self.check_var = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(left_frame, text="有効にする", variable=self.check_var)
        self.checkbox.pack(pady=5)

        self.submit_button = tk.Button(left_frame, text="送信", command=self.update_output)
        self.submit_button.pack(pady=10)

        # 右フレーム（出力用ウィジェット）
        tk.Label(right_frame, text="出力:").pack(pady=5)
        self.output_text = tk.Text(right_frame, height=10, width=30)
        self.output_text.pack(pady=5)

        self.result_label = tk.Label(right_frame, text="結果:")
        self.result_label.pack(pady=5)

    def update_output(self):
        # 入力値を取得して出力を更新
        text = self.text_input.get()
        number = self.number_input.get()
        option = self.option_var.get()
        checked = "はい" if self.check_var.get() else "いいえ"

        output = f"テキスト: {text}\n数値: {number}\n選択: {option}\nチェック: {checked}"
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, output)

        # 結果ラベルを更新（例として）
        self.result_label.config(text=f"結果: 入力完了")
        

class callback(input):
    def __init__(self):
        pass