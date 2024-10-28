import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageFilter, ImageTk
import numpy as np
import cv2

class ImageFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng Dụng Lọc Ảnh")

        # Các widget
        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.load_button = tk.Button(root, text="Tải Ảnh", command=self.load_image)
        self.load_button.pack()

        self.filter_option = tk.StringVar(value="Gaussian Blur")
        filter_menu = tk.OptionMenu(root, self.filter_option, "Làm Mịn Gaussian", "Bộ Lọc Median")
        filter_menu.pack()

        self.smooth_button = tk.Button(root, text="Áp Dụng Lọc", command=self.apply_filter)
        self.smooth_button.pack()

        self.save_button = tk.Button(root, text="Lưu Ảnh", command=self.save_image)
        self.save_button.pack()

        self.original_image = None
        self.processed_image = None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Tập tin ảnh", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image)

    def display_image(self, image):
        self.tk_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.tk_image)
        self.image_label.image = self.tk_image

    def apply_gaussian_blur(self):
        if self.original_image:
            self.processed_image = self.original_image.filter(ImageFilter.GaussianBlur(radius=2))  # Giảm giá trị radius xuống 2
            self.display_image(self.processed_image)
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng tải một bức ảnh trước.")

    def apply_median_filter(self):
        if self.original_image:
            cv_image = cv2.cvtColor(np.array(self.original_image), cv2.COLOR_RGB2BGR)
            cv_image = cv2.medianBlur(cv_image, 5)
            self.processed_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
            self.display_image(self.processed_image)
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng tải một bức ảnh trước.")

    def apply_filter(self):
        if self.filter_option.get() == "Làm Mịn Gaussian":
            self.apply_gaussian_blur()
        elif self.filter_option.get() == "Bộ Lọc Median":
            self.apply_median_filter()

    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("Tập tin JPEG", "*.jpg"), ("Tập tin PNG", "*.png")])
            if file_path:
                self.processed_image.save(file_path)
        else:
            messagebox.showwarning("Cảnh Báo", "Không có ảnh để lưu.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageFilterApp(root)
    root.mainloop()
