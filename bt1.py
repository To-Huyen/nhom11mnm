
import tkinter as tk
from tkinter import messagebox
import numpy as np

class EquationSolverApp:
    def __init__(self, master):
        self.master = master
        master.title("Giải Hệ Phương Trình Tuyến Tính")
        self.entries = []
        self.n = 0

        # Khung nhập số lượng ẩn
        self.top_frame = tk.Frame(master)
        self.top_frame.pack(pady=10)

        self.label_n = tk.Label(self.top_frame, text="Số lượng ẩn (N):")
        self.label_n.pack(side=tk.LEFT, padx=5)

        self.entry_n = tk.Entry(self.top_frame, width=5)
        self.entry_n.pack(side=tk.LEFT, padx=5)

        self.button_set = tk.Button(self.top_frame, text="Thiết lập", command=self.set_variables)
        self.button_set.pack(side=tk.LEFT, padx=5)

        # Khung cho ma trận hệ số và hằng số
        self.matrix_frame = tk.Frame(master)
        self.matrix_frame.pack(pady=10)

        # Khung nút giải
        self.solve_frame = tk.Frame(master)
        self.solve_frame.pack(pady=10)

        self.button_solve = tk.Button(self.solve_frame, text="Giải Hệ", command=self.solve_equations)
        self.button_solve.pack()

        # Khung hiển thị kết quả
        self.result_frame = tk.Frame(master)
        self.result_frame.pack(pady=10)

        self.label_result = tk.Label(self.result_frame, text="", fg="blue")
        self.label_result.pack()

    def set_variables(self):
        try:
            n = int(self.entry_n.get())
            if n <= 0:
                raise ValueError
            self.n = n
            self.create_matrix_entries()
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên dương cho N.")

    def create_matrix_entries(self):
        # Xóa các entry cũ nếu có
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.entries = []

        # Tạo tiêu đề cho các cột ẩn và hằng số
        for i in range(self.n):
            label = tk.Label(self.matrix_frame, text=f"x{i+1}")
            label.grid(row=0, column=i, padx=5, pady=5)
        label_eq = tk.Label(self.matrix_frame, text="= b")
        label_eq.grid(row=0, column=self.n, padx=5, pady=5)

        # Tạo các ô nhập hệ số và hằng số cho từng phương trình
        for row in range(1, self.n + 1):
            row_entries = []
            for col in range(self.n + 1):
                entry = tk.Entry(self.matrix_frame, width=5)
                entry.grid(row=row, column=col, padx=5, pady=5)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def solve_equations(self):
        if self.n == 0:
            messagebox.showerror("Lỗi", "Vui lòng thiết lập số lượng ẩn trước.")
            return

        A = []
        b = []
        try:
            for row in self.entries:
                coefficients = []
                for entry in row[:-1]:
                    val = float(entry.get())
                    coefficients.append(val)
                A.append(coefficients)
                b_val = float(row[-1].get())
                b.append(b_val)
            A = np.array(A)
            b = np.array(b)

            # Kiểm tra định thức để xác định hệ có nghiệm duy nhất
            det = np.linalg.det(A)
            if det == 0:
                messagebox.showerror("Lỗi", "Hệ phương trình vô nghiệm hoặc vô số nghiệm.")
                return

            # Giải hệ phương trình
            solution = np.linalg.solve(A, b)
            solution_str = ", ".join([f"x{i+1} = {solution[i]:.4f}" for i in range(self.n)])
            self.label_result.config(text=f"Nghiệm: {solution_str}")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập các số hợp lệ.")
        except np.linalg.LinAlgError:
            messagebox.showerror("Lỗi", "Hệ phương trình vô nghiệm hoặc vô số nghiệm.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EquationSolverApp(root)
    root.mainloop()