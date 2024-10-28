import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from numpy import array
from sklearn.model_selection import train_test_split
from sklearn import neighbors, linear_model, tree
from sklearn.metrics import mean_squared_error, mean_absolute_error
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class KNNApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng dự đoán điểm")

        # Thiết lập các thành phần giao diện
        self.file_label = tk.Label(root, text="Chọn file CSV:")
        self.file_label.grid(row=0, column=0, padx=5, pady=5)
        self.file_button = tk.Button(root, text="Load Data", command=self.load_data)
        self.file_button.grid(row=0, column=1, padx=5, pady=5)

        self.algorithm_label = tk.Label(root, text="Thuật toán:")
        self.algorithm_label.grid(row=1, column=0, padx=5, pady=5)
        self.algorithm_combo = ttk.Combobox(root, values=["KNN", "Linear Regression", "Decision Tree"])
        self.algorithm_combo.current(0)
        self.algorithm_combo.grid(row=1, column=1, padx=5, pady=5)

        self.train_button = tk.Button(root, text="Train", command=self.train_model)
        self.train_button.grid(row=2, column=0, padx=5, pady=5)

        self.test_button = tk.Button(root, text="Test", command=self.test_model)
        self.test_button.grid(row=2, column=1, padx=5, pady=5)

        self.plot_button = tk.Button(root, text="Hiển thị đồ thị", command=self.plot_results)
        self.plot_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Các trường nhập liệu cho giá trị mới
        self.inputs = []
        fields = ['Hours Studied', 'Previous Scores', 'Extracurricular Activities', 'Sleep Hours', 
                  'Sample Question Papers Practiced', 'Performance Index']
        for idx, field in enumerate(fields):
            label = tk.Label(root, text=field)
            label.grid(row=4+idx, column=0, padx=5, pady=5)
            entry = tk.Entry(root)
            entry.grid(row=4+idx, column=1, padx=5, pady=5)
            self.inputs.append(entry)

        self.predict_button = tk.Button(root, text="Hiển thị kết quả dự đoán", command=self.predict_new_data)
        self.predict_button.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

        self.result_text = tk.Text(root, height=10, width=50)
        self.result_text.grid(row=11, column=0, columnspan=2, padx=5, pady=5)

        # Biến lưu dữ liệu
        self.df = None
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
        self.model = None
        self.y_predict = None

    def load_data(self):
        file_path = filedialog.askopenfilename()
        try:
            self.df = pd.read_csv(file_path)
            messagebox.showinfo("Thông báo", "Tải dữ liệu thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")

    def train_model(self):
        if self.df is not None:
            try:
                x = array(self.df.iloc[:200, 0:5]).astype(np.float64)
                y = array(self.df.iloc[:200, 4:5]).astype(np.float64)
                self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.2, random_state=1)

                selected_algorithm = self.algorithm_combo.get()

                if selected_algorithm == "KNN":
                    self.model = neighbors.KNeighborsRegressor(n_neighbors=3, p=2)
                elif selected_algorithm == "Linear Regression":
                    self.model = linear_model.LinearRegression()
                elif selected_algorithm == "Decision Tree":
                    self.model = tree.DecisionTreeRegressor()

                self.model.fit(self.X_train, self.y_train)
                messagebox.showinfo("Thông báo", "Train thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể train mô hình: {e}")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng tải dữ liệu trước khi train!")

    def test_model(self):
        if self.model is not None:
            try:
                self.y_predict = self.model.predict(self.X_test)
                mse = mean_squared_error(self.y_test, self.y_predict)
                mae = mean_absolute_error(self.y_test, self.y_predict)
                rmse = np.sqrt(mse)
                self.result_text.insert(tk.END, f"MSE: {mse:.2f}\n")
                self.result_text.insert(tk.END, f"MAE: {mae:.2f}\n")
                self.result_text.insert(tk.END, f"RMSE: {rmse:.2f}\n")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể test mô hình: {e}")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng train mô hình trước khi test!")

    def plot_results(self):
        if self.y_predict is not None:
            plt.plot(range(0, len(self.y_test)), self.y_test, 'ro', label='Original data')
            plt.plot(range(0, len(self.y_predict)), self.y_predict, 'bo', label='Fitted line')
            for i in range(0, len(self.y_test)):
                tam = [self.y_test[i], self.y_predict[i]]
                plt.plot([i, i], tam, 'Green')
            plt.title('Kết quả dự đoán')
            plt.legend()
            plt.show()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng test mô hình trước khi hiển thị đồ thị!")

    def predict_new_data(self):
        try:
            input_data = [float(entry.get()) for entry in self.inputs]
            input_data = np.array(input_data).reshape(1, -1)
            prediction = self.model.predict(input_data)
            self.result_text.insert(tk.END, f"Kết quả dự đoán: {prediction[0][0]:.2f}\n")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể dự đoán: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = KNNApp(root)
    root.mainloop()
