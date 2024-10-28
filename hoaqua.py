import tkinter as tk
import random
from tkinter import messagebox
from PIL import Image, ImageTk

class FruitCatcherGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Fruit Catcher Game")

        # Biến trạng thái
        self.score = 0
        self.lives = 3
        self.fruit_speed = 5
        self.fruit_interval = 1500
        self.fruits = []
        self.game_over = False
        self.paused = False

        # Tải hình ảnh hoa quả
        self.load_images()

        # Giao diện chính
        self.create_main_menu()

    def load_images(self):
        """Load ảnh của hoa quả và các nút, dùng hình dạng thay thế nếu ảnh không tải được"""
        try:
            self.bg_image = ImageTk.PhotoImage(Image.open("data/background.png").resize((600, 400)))
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.bg_image = None  # Không dùng ảnh nền nếu không tải được

        try:
            self.basket_image = ImageTk.PhotoImage(Image.open("data/basket.png").resize((100, 30)))
        except Exception as e:
            print(f"Error loading basket image: {e}")
            self.basket_image = None  # Không dùng giỏ nếu không tải được

        # Tải ảnh các loại hoa quả
        self.fruit_images = {}
        fruit_types = ["apple", "orange", "banana", "grapes", "blueberry"]
        for fruit in fruit_types:
            try:
                self.fruit_images[fruit] = ImageTk.PhotoImage(Image.open(f"data/{fruit}.png").resize((30, 30)))
            except Exception as e:
                print(f"Error loading {fruit} image: {e}")
                self.fruit_images[fruit] = None  # Không dùng ảnh nếu không tải được

    def create_main_menu(self):
        """Tạo giao diện menu chính"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=100)

        title_label = tk.Label(self.main_frame, text="Fruit Catcher Game", font=("Arial", 24, "bold"))
        title_label.pack(pady=10)

        play_button = tk.Button(self.main_frame, text="Chơi Game", font=("Arial", 16),
                                command=self.create_difficulty_selection)
        play_button.pack(pady=5)

        exit_button = tk.Button(self.main_frame, text="Thoát", font=("Arial", 16), command=self.root.quit)
        exit_button.pack(pady=5)

    def create_difficulty_selection(self):
        """Giao diện chọn mức độ khó"""
        self.main_frame.pack_forget()
        self.difficulty_frame = tk.Frame(self.root)
        self.difficulty_frame.pack(pady=50)

        label = tk.Label(self.difficulty_frame, text="Chọn mức độ khó:", font=("Arial", 16))
        label.pack(pady=10)

        # Nút chọn độ khó
        easy_button = tk.Button(self.difficulty_frame, text="Dễ", command=lambda: self.start_game("easy"), width=10)
        easy_button.pack(side=tk.LEFT, padx=5)

        medium_button = tk.Button(self.difficulty_frame, text="Trung Bình", command=lambda: self.start_game("medium"),
                                  width=10)
        medium_button.pack(side=tk.LEFT, padx=5)

        hard_button = tk.Button(self.difficulty_frame, text="Khó", command=lambda: self.start_game("hard"), width=10)
        hard_button.pack(side=tk.LEFT, padx=5)

    def start_game(self, difficulty):
        """Bắt đầu game với độ khó đã chọn"""
        self.difficulty_frame.pack_forget()

        # Thiết lập mức độ khó
        if difficulty == "easy":
            self.fruit_speed = 3
            self.fruit_interval = 2000
        elif difficulty == "medium":
            self.fruit_speed = 5
            self.fruit_interval = 1500
        elif difficulty == "hard":
            self.fruit_speed = 8
            self.fruit_interval = 1000

        # Tạo giao diện chơi game
        self.create_game_canvas()

        # Bắt đầu tạo quả
        self.spawn_fruit()

        # Cập nhật game liên tục
        self.update_game()

    def create_game_canvas(self):
        """Tạo giao diện chính của trò chơi"""
        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack()

        # Nền và giỏ bắt quả
        if self.bg_image:
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        else:
            self.canvas.create_rectangle(0, 0, 600, 400, fill="lightblue")

        if self.basket_image:
            self.basket = self.canvas.create_image(300, 370, image=self.basket_image)
        else:
            self.basket = self.canvas.create_rectangle(250, 370, 350, 400, fill="brown")

        # Điểm và số mạng
        self.score_text = self.canvas.create_text(50, 30, text="Score: 0", font=("Arial", 16), fill="black")
        self.lives_text = self.canvas.create_text(550, 30, text="Lives: 3", font=("Arial", 16), fill="red")

        # Điều khiển game
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

        # Tạo nút điều khiển
        self.create_game_controls()

    def create_game_controls(self):
        """Tạo bảng điều khiển cho game"""
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.BOTTOM, pady=10)

        self.pause_button = tk.Button(self.control_frame, text="Tạm dừng", command=self.pause_game, width=10)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.resume_button = tk.Button(self.control_frame, text="Tiếp tục", command=self.resume_game, width=10, state=tk.DISABLED)
        self.resume_button.pack(side=tk.LEFT, padx=5)

        restart_button = tk.Button(self.control_frame, text="Chơi lại", command=self.restart_game, width=10)
        restart_button.pack(side=tk.LEFT, padx=5)

        main_menu_button = tk.Button(self.control_frame, text="Menu chính", command=self.return_to_menu, width=10)
        main_menu_button.pack(side=tk.LEFT, padx=5)

    def move_left(self, event):
        """Di chuyển giỏ sang trái"""
        self.canvas.move(self.basket, -20, 0)

    def move_right(self, event):
        """Di chuyển giỏ sang phải"""
        self.canvas.move(self.basket, 20, 0)

    def spawn_fruit(self):
        """Tạo hoa quả ngẫu nhiên"""
        if not self.game_over and not self.paused:
            fruit_type = random.choice(list(self.fruit_images.keys()))
            x_position = random.randint(50, 550)
            if self.fruit_images[fruit_type]:
                fruit = self.canvas.create_image(x_position, 50, image=self.fruit_images[fruit_type])
            else:
                fruit = self.canvas.create_oval(x_position, 50, x_position + 30, 80, fill="grey")  # Hoa quả không có ảnh
            self.fruits.append((fruit, fruit_type))
            self.root.after(self.fruit_interval, self.spawn_fruit)

    def update_game(self):
        """Cập nhật trò chơi liên tục"""
        if not self.paused and not self.game_over:
            self.move_fruits()
            self.check_collisions()

        if not self.game_over:
            self.root.after(50, self.update_game)

    def move_fruits(self):
        """Di chuyển hoa quả"""
        for fruit, fruit_type in self.fruits:
            self.canvas.move(fruit, 0, self.fruit_speed)
            if self.canvas.coords(fruit)[1] > 400:  # Rơi ra khỏi màn hình
                self.miss_fruit(fruit, fruit_type)

    def check_collisions(self):
        """Kiểm tra va chạm giữa giỏ và trái cây"""
        basket_coords = self.canvas.coords(self.basket)
        basket_x1 = basket_coords[0] - 50  # Giỏ nằm giữa (50 pixel bên trái)
        basket_x2 = basket_coords[0] + 50  # Giỏ nằm giữa (50 pixel bên phải)
        basket_y1 = basket_coords[1]  # Y tọa độ giỏ
        basket_y2 = basket_coords[1] + 30  # Chiều cao của giỏ

        for fruit, fruit_type in self.fruits:
            fruit_coords = self.canvas.coords(fruit)
            if not fruit_coords:  # Đảm bảo trái cây còn tồn tại
                continue

            fruit_x1 = fruit_coords[0] - 15  # Trái cây nằm giữa (15 pixel bên trái)
            fruit_x2 = fruit_coords[0] + 15  # Trái cây nằm giữa (15 pixel bên phải)
            fruit_y1 = fruit_coords[1]
            fruit_y2 = fruit_coords[1] + 30  # Chiều cao của trái cây

            # Kiểm tra va chạm
            if (basket_x1 < fruit_x2 and basket_x2 > fruit_x1 and
                    basket_y1 < fruit_y2 and basket_y2 > fruit_y1):
                self.catch_fruit(fruit, fruit_type)

    def catch_fruit(self, fruit, fruit_type):
        """Xử lý khi giỏ bắt được trái cây"""
        self.canvas.delete(fruit)
        self.fruits.remove((fruit, fruit_type))
        self.score += 1
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

    def miss_fruit(self, fruit, fruit_type):
        """Xử lý khi trái cây rơi xuống mà không được bắt"""
        self.canvas.delete(fruit)
        self.fruits.remove((fruit, fruit_type))
        self.lives -= 1
        self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")
        if self.lives <= 0:
            self.game_over = True
            messagebox.showinfo("Game Over", f"Điểm số của bạn: {self.score}")
            self.return_to_menu()

    def pause_game(self):
        """Tạm dừng game"""
        self.paused = True
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.NORMAL)

    def resume_game(self):
        """Tiếp tục game"""
        self.paused = False
        self.pause_button.config(state=tk.NORMAL)
        self.resume_button.config(state=tk.DISABLED)

    def restart_game(self):
        """Khởi động lại game"""
        self.score = 0
        self.lives = 3
        self.fruits.clear()
        self.game_over = False
        self.canvas.delete("all")  # Xóa tất cả đối tượng trên canvas
        self.create_game_canvas()
        self.spawn_fruit()
        self.update_game()

    def return_to_menu(self):
        """Quay lại menu chính"""
        self.score = 0
        self.lives = 3
        self.fruits.clear()
        self.game_over = False
        self.paused = False
        self.create_main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    game = FruitCatcherGame(root)
    root.mainloop()
