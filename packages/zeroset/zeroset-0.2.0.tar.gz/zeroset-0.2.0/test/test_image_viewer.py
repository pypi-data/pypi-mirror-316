import tkinter as tk
from zeroset import cv0
from PIL import ImageTk, Image
from tkinter import font as tkfont
import screeninfo
import numpy as np


class ImageViewer():

    def __init__(self, title: str = "Viewer", images: list[np.ndarray] | None = None, width: int | None = None, height: int | None = None):
        if images is None:
            raise Exception("The 'images' parameter must be a list[np.ndarray]")
        monitor = [m for m in screeninfo.get_monitors() if m.is_primary == True][0]
        if width is None:
            width = int(monitor.width * 0.8)
        if height is None:
            height = int(monitor.height * 0.8)

        self.window = tk.Tk()
        self.window.title(title)
        self.window.iconbitmap('logo.ico')
        self.window.resizable(False, False)
        self.background_color = "#ffffff"
        self.primary_color = "#05d686"
        self.window_width = width
        self.window_height = height
        self.window.configure(bg=self.background_color)
        self.canvas = tk.Canvas(self.window, width=width, height=height)
        self.canvas.grid(row=0, column=0)
        self.images = images

        button_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
        button_style = {
            "font"            : button_font,
            "bg"              : self.primary_color,  # 배경색
            "fg"              : "black",  # 텍스트 색
            "activebackground": self.primary_color,  # 클릭 시 배경색
            "activeforeground": "white",  # 클릭 시 텍스트 색
            "relief"          : tk.RAISED,
            "borderwidth"     : 2,
            "padx"            : 20,
            "pady"            : 10,
        }

        self.button_prev = tk.Button(self.window, text="◀◀◀", command=self.on_button_clicked_prev, **button_style)
        self.button_prev.grid(row=1, column=0, sticky="w", padx=(0, 10))

        self.button_next = tk.Button(self.window, text="▶▶▶", command=self.on_button_clicked_next, **button_style)
        self.button_next.grid(row=1, column=0, sticky="e", padx=(10, 0))

        self.index_label = tk.Label(self.window, text="", font=button_font, bg=self.background_color, fg="Black")
        self.index_label.grid(row=1, column=0)

        self.button_prev.bind("<Enter>", self.on_enter)
        self.button_prev.bind("<Leave>", self.on_leave)
        self.button_next.bind("<Enter>", self.on_enter)
        self.button_next.bind("<Leave>", self.on_leave)
        self.window.bind('<Escape>', self.close_window)
        self.window.bind('<q>', self.close_window)
        self.window.bind('<Left>', self.on_button_clicked_prev)
        self.window.bind('<Right>', self.on_button_clicked_next)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW)
        self.image_idx = 0
        self.img = images[self.image_idx]

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"+{x}+{y}")

        self.on_button_clicked()

    def resize_image(self, img, width=None, height=None):
        img_ratio = img.width / img.height
        window_ratio = self.window_width / self.window_height

        if img_ratio > window_ratio:
            new_width = self.window_width
            new_height = int(self.window_width / img_ratio)
        else:
            new_height = self.window_height
            new_width = int(self.window_height * img_ratio)

        resized_image = img.resize((new_width, new_height), Image.LANCZOS)

        background = Image.new('RGB', (self.window_width, self.window_height), self.background_color)

        offset = ((self.window_width - new_width) // 2, (self.window_height - new_height) // 2)
        background.paste(resized_image, offset)
        return background

    def on_enter(self, e):
        e.widget['background'] = self.primary_color
        e.widget['foreground'] = "White"

    def on_leave(self, e):
        e.widget['background'] = self.primary_color
        e.widget['foreground'] = "Black"

    def on_button_clicked(self):
        resized_image = self.resize_image(cv0.to_pil(self.images[self.image_idx]), self.window_width, self.window_height)
        self.img = ImageTk.PhotoImage(resized_image)
        width, height = self.img.width(), self.img.height()
        self.canvas.config(width=width, height=height, bd=0, highlightthickness=0)
        self.canvas.itemconfig(self.image_on_canvas, image=self.img)
        self.update_index_label()

    def update_index_label(self):
        index_text = f"({self.image_idx + 1}/{len(self.images)})"
        shape = self.images[self.image_idx].shape
        if len(shape) == 2:
            channel = "2"
        else:
            channel = str(shape[2])
        height, width = shape[:2]
        info = f'{width} x {height} x {channel}'
        self.index_label.config(text=f'{info} {index_text}')

    def on_button_clicked_next(self, event=None):
        self.image_idx = (self.image_idx + 1) % len(self.images)
        self.on_button_clicked()

    def on_button_clicked_prev(self, event=None):
        self.image_idx = (self.image_idx - 1 + len(self.images)) % len(self.images)
        self.on_button_clicked()

    def close_window(self, event=None):
        self.window.quit()
        self.window.destroy()


files = cv0.glob("../data/", ["*.jpg", "*.png"])
images = cv0.imreads(files)
viewer = ImageViewer(title="ZeroSet", images=images)
viewer.window.mainloop()

print("Hello")
