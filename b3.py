import numpy as np
import pandas as pd
from numpy import array
from sklearn.model_selection import train_test_split
from sklearn import neighbors
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Initialize the Tkinter window
root = tk.Tk()
root.title("Dự đoán Kết quả Học tập")
root.geometry("500x700")

# Global variables for data and model
df = None
models = {}
X_train, X_test, y_train, y_test = None, None, None, None


# Function to load the dataset
def load_data():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path)
        messagebox.showinfo("Thông báo", "Dữ liệu đã được tải thành công!")
    else:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn file dữ liệu.")

# Function to train the model
def train_model():
    global models, X_train, X_test, y_train, y_test
    if df is None:
        messagebox.showwarning("Cảnh báo", "Vui lòng tải dữ liệu trước.")
        return

    # Select features and target variable
    x = array(df.iloc[:, 0:5]).astype(np.float64)
    y = array(df.iloc[:, 5]).astype(np.float64)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

    # Các thuật toán để huấn luyện
    models = {
        "KNN": neighbors.KNeighborsRegressor(n_neighbors=3, p=2),
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(random_state=1),
        "SVR": SVR(kernel='linear')
    }

    # Lưu trữ thời gian và hiển thị độ chính xác cho mỗi mô hình
    training_times = {}
    accuracy_scores = {}

    for name, model in models.items():
        start_time = time.time()  # Ghi nhận thời gian bắt đầu
        model.fit(X_train, y_train)  # Huấn luyện mô hình
        end_time = time.time()  # Ghi nhận thời gian kết thúc

        # Tính thời gian huấn luyện
        training_times[name] = end_time - start_time

        # Tính toán độ chính xác R-squared
        r2 = model.score(X_test, y_test)
        accuracy_scores[name] = r2

    # Hiển thị thời gian huấn luyện và độ chính xác
    results_text = ""
    for name in models:
        results_text += f"Mô hình: {name}\n"
        results_text += f"Thời gian huấn luyện: {training_times[name]:.4f} giây\n"
        results_text += f"Độ chính xác (R²): {accuracy_scores[name]:.4f}\n\n"

    messagebox.showinfo("Kết quả Huấn luyện", results_text)


# Function to test the model and show errors
def test_model():
    if not models:
        messagebox.showwarning("Cảnh báo", "Vui lòng huấn luyện mô hình trước.")
        return

    errors = {"MSE": [], "MAE": [], "RMSE": []}
    model_names = list(models.keys())

    # Màu sắc khác nhau cho mỗi mô hình
    colors = ['blue', 'green', 'red', 'orange']

    for name, model in models.items():
        # Dự đoán
        y_predict = model.predict(X_test)

        # Tính toán sai số
        mse = mean_squared_error(y_test, y_predict)
        mae = mean_absolute_error(y_test, y_predict)
        rmse = np.sqrt(mse)

        # Thêm sai số vào danh sách
        errors["MSE"].append(mse)
        errors["MAE"].append(mae)
        errors["RMSE"].append(rmse)

    # Vẽ biểu đồ so sánh sai số
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    metrics = ["MSE", "MAE", "RMSE"]

    for i, metric in enumerate(metrics):
        ax[i].bar(model_names, errors[metric], color=colors[:len(model_names)])
        ax[i].set_title(f"So sánh {metric}")
        ax[i].set_ylabel(metric)

    plt.tight_layout()
    plt.show()

    messagebox.showinfo("Kết quả", "Đã kiểm tra mô hình và vẽ biểu đồ so sánh sai số.")



# Function to predict a new student's score
def predict_score():
    if not models:
        messagebox.showwarning("Cảnh báo", "Vui lòng huấn luyện mô hình trước.")
        return
    try:
        # Get input values
        hours = float(entry_hours.get())
        scores = float(entry_scores.get())
        activities = float(entry_activities.get())
        sleep = float(entry_sleep.get())
        papers = float(entry_papers.get())

        # Ensure no negative values
        if any(v < 0 for v in [hours, scores, activities, sleep, papers]):
            raise ValueError("Giá trị nhập vào không được âm.")

        # Kiểm tra tổng thời gian không vượt quá 24 giờ
        total_hours = hours + activities + sleep + papers
        if total_hours > 24:
            raise ValueError(
                f"Tổng giờ học, hoạt động ngoại khóa, giờ ngủ và chỉ số hiệu suất không được vượt quá 24 giờ. Tổng hiện tại: {total_hours:.2f} giờ.")

        # Prepare input data
        input_data = np.array([[hours, scores, activities, sleep, papers]])

        # Predict using the selected model
        selected_model = algorithm_combobox.get()
        prediction = models[selected_model].predict(input_data)[0]
        prediction = max(0, min(100, prediction))  # Limit between 0 and 100

        result_label.config(text=f"Điểm dự đoán: {prediction:.2f}")

        # Clear inputs
        clear_inputs()

    except ValueError as e:
        messagebox.showerror("Lỗi", str(e))


# Clear inputs after prediction
def clear_inputs():
    entry_hours.delete(0, tk.END)
    entry_scores.delete(0, tk.END)
    entry_activities.delete(0, tk.END)
    entry_sleep.delete(0, tk.END)
    entry_papers.delete(0, tk.END)


# UI for loading data
load_button = tk.Button(root, text="Tải dữ liệu CSV", command=load_data)
load_button.pack(pady=10)

# UI for selecting algorithm for prediction
algorithm_label = tk.Label(root, text="Chọn thuật toán cho dự đoán:")
algorithm_label.pack(pady=5)
algorithm_combobox = ttk.Combobox(root, values=["KNN", "Linear Regression", "Decision Tree", "SVR"])
algorithm_combobox.pack(pady=5)
algorithm_combobox.current(0)  # Set default selection

# UI for training the model
train_button = tk.Button(root, text="Huấn luyện mô hình", command=train_model)
train_button.pack(pady=10)

# UI for testing the model
test_button = tk.Button(root, text="Kiểm tra mô hình", command=test_model)
test_button.pack(pady=10)

# UI for entering new student data and predicting
label_hours = tk.Label(root, text="Giờ học:")
label_hours.pack(pady=5)
entry_hours = tk.Entry(root)
entry_hours.pack(pady=5)

label_scores = tk.Label(root, text="Điểm trước:")
label_scores.pack(pady=5)
entry_scores = tk.Entry(root)
entry_scores.pack(pady=5)

label_activities = tk.Label(root, text="Hoạt động ngoại khóa:")
label_activities.pack(pady=5)
entry_activities = tk.Entry(root)
entry_activities.pack(pady=5)

label_sleep = tk.Label(root, text="Giờ ngủ:")
label_sleep.pack(pady=5)
entry_sleep = tk.Entry(root)
entry_sleep.pack(pady=5)

label_papers = tk.Label(root, text="Chỉ số hiệu suất:")
label_papers.pack(pady=5)
entry_papers = tk.Entry(root)
entry_papers.pack(pady=5)

# Button to predict score
predict_button = tk.Button(root, text="Dự đoán kết quả", command=predict_score)
predict_button.pack(pady=20)

# Label to display prediction result
result_label = tk.Label(root, text="", font=("Helvetica", 16))
result_label.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
