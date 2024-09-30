import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np

class AlgebraApp:
    def __init__(self, master):
        self.master = master
        master.title("Ứng Dụng Hỗ Trợ Học Đại Số")

        self.function_frame = tk.Frame(master)
        self.function_frame.pack(pady=20)

        self.label_function = tk.Label(self.function_frame, text="Chọn chức năng:", font=("Arial", 14))
        self.label_function.pack()

        self.functions = ["Cộng ma trận", "Trừ ma trận", "Nhân ma trận", "Chia ma trận", "Tìm ma trận nghịch đảo", "Tìm hạng ma trận", "Giải hệ phương trình", "Tính định thức", "Chuyển vị ma trận"]
        self.function_combo = ttk.Combobox(self.function_frame, values=self.functions, state="readonly")
        self.function_combo.pack(pady=10)

        self.button_select = tk.Button(self.function_frame, text="Chọn", command=self.select_function)
        self.button_select.pack(pady=10)

        self.matrix_frame = tk.Frame(master)
        self.matrix_frame.pack(pady=20)

        self.label_result = tk.Label(master, text="", font=("Arial", 12), fg="blue")
        self.label_result.pack(pady=20)

    def select_function(self):
        selected_function = self.function_combo.get()
        if selected_function in ["Cộng ma trận", "Trừ ma trận", "Nhân ma trận", "Chia ma trận"]:
            self.clear_frame()
            self.create_matrix_input_fields(selected_function)
        elif selected_function == "Tìm ma trận nghịch đảo":
            self.clear_frame()
            self.find_inverse_matrix()
        elif selected_function == "Tìm hạng ma trận":
            self.clear_frame()
            self.find_matrix_rank()
        elif selected_function == "Giải hệ phương trình":
            self.clear_frame()
            self.solve_equations()
        elif selected_function == "Tính định thức":
            self.clear_frame()
            self.calculate_determinant()
        elif selected_function == "Chuyển vị ma trận":
            self.clear_frame()
            self.transpose_matrix()

    def create_matrix_input_fields(self, operation):
        self.label = tk.Label(self.matrix_frame, text=f"Thực hiện phép {operation}:")
        self.label.pack()

        # Input cho kích thước ma trận
        self.label_size = tk.Label(self.matrix_frame, text="Nhập kích thước ma trận (hàng x cột):")
        self.label_size.pack()

        self.entry_rows = tk.Entry(self.matrix_frame, width=5)
        self.entry_rows.pack(side=tk.LEFT, padx=5)
        self.label_x = tk.Label(self.matrix_frame, text="x")
        self.label_x.pack(side=tk.LEFT)
        self.entry_cols = tk.Entry(self.matrix_frame, width=5)
        self.entry_cols.pack(side=tk.LEFT, padx=5)

        self.button_create = tk.Button(self.matrix_frame, text="Tạo ma trận", command=lambda: self.create_matrix_entries(operation))
        self.button_create.pack(pady=10)

    def create_matrix_entries(self, operation):
        try:
            self.rows = int(self.entry_rows.get())
            self.cols = int(self.entry_cols.get())

            if self.rows <= 0 or self.cols <= 0:
                raise ValueError("Số hàng và số cột phải lớn hơn 0.")

            # Tạo các ô nhập cho ma trận đầu tiên
            self.label_matrix1 = tk.Label(self.matrix_frame, text="Nhập ma trận 1:")
            self.label_matrix1.pack()
            self.matrix_entries1 = []
            for i in range(self.rows):
                row_entries = []
                for j in range(self.cols):
                    entry = tk.Entry(self.matrix_frame, width=5)
                    entry.pack(side=tk.LEFT, padx=2, pady=2)
                    row_entries.append(entry)
                self.matrix_entries1.append(row_entries)
                tk.Frame(self.matrix_frame).pack()  # Để xuống dòng

            # Tạo các ô nhập cho ma trận thứ hai nếu không phải phép chia ma trận đơn
            if operation != "Tìm ma trận nghịch đảo":
                self.label_matrix2 = tk.Label(self.matrix_frame, text="Nhập ma trận 2:")
                self.label_matrix2.pack()
                self.matrix_entries2 = []
                for i in range(self.rows):
                    row_entries = []
                    for j in range(self.cols):
                        entry = tk.Entry(self.matrix_frame, width=5)
                        entry.pack(side=tk.LEFT, padx=2, pady=2)
                        row_entries.append(entry)
                    self.matrix_entries2.append(row_entries)
                    tk.Frame(self.matrix_frame).pack()  # Để xuống dòng

            self.result_button = tk.Button(self.matrix_frame, text="Tính toán", command=lambda: self.calculate_matrix_operation(operation))
            self.result_button.pack(pady=10)

        except ValueError as e:
            messagebox.showerror("Lỗi", f"Lỗi nhập liệu: {e}")

    def calculate_matrix_operation(self, operation):
        try:
            matrix1 = self.get_matrix_from_entries(self.matrix_entries1)
            if operation != "Tìm ma trận nghịch đảo":
                matrix2 = self.get_matrix_from_entries(self.matrix_entries2)

            if operation == "Cộng ma trận":
                result = np.add(matrix1, matrix2)
            elif operation == "Trừ ma trận":
                result = np.subtract(matrix1, matrix2)
            elif operation == "Nhân ma trận":
                result = np.dot(matrix1, matrix2)
            elif operation == "Chia ma trận":
                result = np.divide(matrix1, matrix2)

            self.label_result.config(text=f"Kết quả: \n{result}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def get_matrix_from_entries(self, entries):
        matrix = []
        for row_entries in entries:
            row = []
            for entry in row_entries:
                row.append(float(entry.get()))  # Lấy giá trị float từ ô nhập
            matrix.append(row)
        return np.array(matrix)

    def find_inverse_matrix(self):
        # Chức năng tìm ma trận nghịch đảo
        self.label = tk.Label(self.matrix_frame, text="Nhập ma trận để tìm nghịch đảo:")
        self.label.pack()

        self.label_size = tk.Label(self.matrix_frame, text="Nhập kích thước ma trận (n x n):")
        self.label_size.pack()

        self.entry_size = tk.Entry(self.matrix_frame)
        self.entry_size.pack()

        self.button_create = tk.Button(self.matrix_frame, text="Tạo ma trận", command=self.create_inverse_matrix_entries)
        self.button_create.pack()

    def create_inverse_matrix_entries(self):
        try:
            n = int(self.entry_size.get())
            if n <= 0:
                raise ValueError("Kích thước phải lớn hơn 0.")

            self.matrix_entries = []
            for i in range(n):
                row_entries = []
                for j in range(n):
                    entry = tk.Entry(self.matrix_frame, width=5)
                    entry.pack(side=tk.LEFT, padx=2, pady=2)
                    row_entries.append(entry)
                self.matrix_entries.append(row_entries)
                tk.Frame(self.matrix_frame).pack()

            self.result_button = tk.Button(self.matrix_frame, text="Tính", command=self.calculate_inverse_matrix)
            self.result_button.pack(pady=10)

        except ValueError as e:
            messagebox.showerror("Lỗi", f"Lỗi nhập liệu: {e}")

    def calculate_inverse_matrix(self):
        try:
            matrix = self.get_matrix_from_entries(self.matrix_entries)
            result = np.linalg.inv(matrix)
            self.label_result.config(text=f"Ma trận nghịch đảo: \n{result}")
        except np.linalg.LinAlgError:
            messagebox.showerror("Lỗi", "Ma trận không khả nghịch.")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def find_matrix_rank(self):
        # Chức năng tìm hạng ma trận
        self.label = tk.Label(self.matrix_frame, text="Nhập ma trận để tìm hạng:")
        self.label.pack()

        self.create_matrix_input_fields("Tìm hạng ma trận")

        self.result_button = tk.Button(self.matrix_frame, text="Tính", command=self.calculate_matrix_rank)
        self.result_button.pack()

    def calculate_matrix_rank(self):
        try:
            matrix = self.get_matrix_from_entries(self.matrix_entries1)
            result = np.linalg.matrix_rank(matrix)
            self.label_result.config(text=f"Hạng của ma trận: {result}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def solve_equations(self):
        # Chức năng giải hệ phương trình tuyến tính
        self.label = tk.Label(self.matrix_frame, text="Nhập ma trận hệ số và vector hằng số:")
        self.label.pack()

        self.create_matrix_input_fields("Giải hệ phương trình")

        self.vector_label = tk.Label(self.matrix_frame, text="Nhập vector hằng số:")
        self.vector_label.pack()

        self.vector_entries = []
        for i in range(self.rows):
            entry = tk.Entry(self.matrix_frame, width=5)
            entry.pack(side=tk.LEFT, padx=2, pady=2)
            self.vector_entries.append(entry)
        tk.Frame(self.matrix_frame).pack()

        self.result_button = tk.Button(self.matrix_frame, text="Giải", command=self.calculate_solutions)
        self.result_button.pack()

    def calculate_solutions(self):
        try:
            matrix = self.get_matrix_from_entries(self.matrix_entries1)
            constants = np.array([float(entry.get()) for entry in self.vector_entries])
            result = np.linalg.solve(matrix, constants)
            self.label_result.config(text=f"Nghiệm của hệ phương trình: {result}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def calculate_determinant(self):
        # Chức năng tính định thức
        self.label = tk.Label(self.matrix_frame, text="Nhập ma trận để tính định thức:")
        self.label.pack()

        self.create_matrix_input_fields("Tính định thức")

        self.result_button = tk.Button(self.matrix_frame, text="Tính", command=self.calculate_matrix_determinant)
        self.result_button.pack()

    def calculate_matrix_determinant(self):
        try:
            matrix = self.get_matrix_from_entries(self.matrix_entries1)
            result = np.linalg.det(matrix)
            self.label_result.config(text=f"Định thức của ma trận: {result}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def transpose_matrix(self):
        # Chức năng chuyển vị ma trận
        self.label = tk.Label(self.matrix_frame, text="Nhập ma trận để chuyển vị:")
        self.label.pack()

        self.create_matrix_input_fields("Chuyển vị ma trận")

        self.result_button = tk.Button(self.matrix_frame, text="Tính", command=self.calculate_transpose_matrix)
        self.result_button.pack()

    def calculate_transpose_matrix(self):
        try:
            matrix = self.get_matrix_from_entries(self.matrix_entries1)
            result = np.transpose(matrix)
            self.label_result.config(text=f"Ma trận chuyển vị: \n{result}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def clear_frame(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

root = tk.Tk()
app = AlgebraApp(root)
root.mainloop()
