import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import neighbors
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Initialize the Tkinter window
root = tk.Tk()
root.title("Xác định độ an toàn của nước")
root.geometry("500x700")

# Global variables for data and model
df = None
model = None
X_train, X_test, y_train, y_test = None, None, None, None
models = {}

# Load the dataset
def load_data():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path)
        messagebox.showinfo("Thông báo", "Dữ liệu đã được tải thành công!")
    else:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn file dữ liệu.")

def train_model():
    global model, X_train, X_test, y_train, y_test, models
    if df is None:
        messagebox.showwarning("Cảnh báo", "Vui lòng tải dữ liệu trước.")
        return

    # Loại bỏ các hàng có giá trị NaN (hoặc sử dụng imputation)
    df.dropna(inplace=True)

    # Chọn các cột đầu làm feature và cột cuối cùng làm target
    x = df.iloc[:, :-1].values  # Tất cả các cột ngoại trừ cột cuối cùng (biến mục tiêu)
    y = df.iloc[:, -1].values   # Cột cuối cùng (biến mục tiêu - Potability)

    # Chia dữ liệu thành tập huấn luyện và tập kiểm tra
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

    # Lấy thuật toán từ ComboBox
    selected_algorithm = algorithm_combobox.get()

    # Khởi tạo mô hình dựa trên thuật toán đã chọn
    start_time = time.time()
    if selected_algorithm == "KNN":
        model = neighbors.KNeighborsClassifier(n_neighbors=3)
    elif selected_algorithm == "Decision Tree":
        model = DecisionTreeClassifier(random_state=1)
    elif selected_algorithm == "SVM":
        model = SVC(kernel='linear')
    else:
        messagebox.showerror("Lỗi", "Thuật toán không hợp lệ.")
        return

    # Huấn luyện mô hình
    model.fit(X_train, y_train)
    models[selected_algorithm] = model  # Lưu mô hình đã huấn luyện
    end_time = time.time()
    training_time = end_time - start_time

    # Tính toán độ chính xác
    accuracy = model.score(X_test, y_test)

    # Hiển thị thời gian huấn luyện và độ chính xác
    messagebox.showinfo("Kết quả Huấn luyện", f"Thời gian huấn luyện: {training_time:.4f} giây\nĐộ chính xác: {accuracy:.4f}")

# Function to test accuracy of all models
def test_model():
    global models, X_test, y_test

    if not models:
        messagebox.showwarning("Cảnh báo", "Vui lòng huấn luyện ít nhất một mô hình trước.")
        return

    accuracies = {}

    for name, model in models.items():
        # Dự đoán
        y_predict = model.predict(X_test)

        # Tính toán độ chính xác
        accuracy = accuracy_score(y_test, y_predict)
        accuracies[name] = accuracy

    # Hiển thị đồ thị cột cho độ chính xác
    plot_accuracy_bar_chart(accuracies)

def plot_accuracy_bar_chart(accuracies):
    names = list(accuracies.keys())
    values = list(accuracies.values())

    plt.figure(figsize=(10, 5))
    plt.bar(names, values, color='skyblue')
    plt.ylim([0, 1])
    plt.title("Độ chính xác của các mô hình")
    plt.ylabel("Độ chính xác")
    plt.show()

# Function to predict water safety
def predict_water_safety():
    global model
    if model is None:
        messagebox.showwarning("Cảnh báo", "Vui lòng huấn luyện mô hình trước.")
        return
    try:
        # Get input values
        ph = float(entry_ph.get())
        hardness = float(entry_hardness.get())
        solids = float(entry_solids.get())
        chloramines = float(entry_chloramines.get())
        sulfate = float(entry_sulfate.get())
        conductivity = float(entry_conductivity.get())
        organic_carbon = float(entry_organic_carbon.get())
        trihalomethanes = float(entry_trihalomethanes.get())
        turbidity = float(entry_turbidity.get())

        # Ensure no negative values
        if any(v < 0 for v in [ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity]):
            raise ValueError("Giá trị nhập vào không được âm.")

        # Prepare input data
        input_data = np.array([[ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity]])

        # Predict and display result
        prediction = model.predict(input_data)[0]
        result = "An toàn" if prediction == 1 else "Không an toàn"
        result_label.config(text=f"Kết quả: {result}")

    except ValueError as e:
        messagebox.showerror("Lỗi", str(e))

# UI for loading data
load_button = tk.Button(root, text="Tải dữ liệu CSV", command=load_data)
load_button.pack(pady=10)

# UI for selecting algorithm
algorithm_label = tk.Label(root, text="Chọn thuật toán:")
algorithm_label.pack(pady=5)
algorithm_combobox = ttk.Combobox(root, values=["KNN", "Decision Tree", "SVM"])
algorithm_combobox.pack(pady=5)
algorithm_combobox.current(0)  # Set default selection

# UI for training the model
train_button = tk.Button(root, text="Huấn luyện mô hình", command=train_model)
train_button.pack(pady=10)

# Button to test model accuracy
test_button = tk.Button(root, text="Kiểm tra độ chính xác", command=test_model)
test_button.pack(pady=10)

# UI for entering water data and predicting
label_ph = tk.Label(root, text="pH:")
label_ph.pack(pady=5)
entry_ph = tk.Entry(root)
entry_ph.pack(pady=5)

label_hardness = tk.Label(root, text="Độ cứng:")
label_hardness.pack(pady=5)
entry_hardness = tk.Entry(root)
entry_hardness.pack(pady=5)

label_solids = tk.Label(root, text="Chất rắn:")
label_solids.pack(pady=5)
entry_solids = tk.Entry(root)
entry_solids.pack(pady=5)

label_chloramines = tk.Label(root, text="Chloramines:")
label_chloramines.pack(pady=5)
entry_chloramines = tk.Entry(root)
entry_chloramines.pack(pady=5)

label_sulfate = tk.Label(root, text="Sulfate:")
label_sulfate.pack(pady=5)
entry_sulfate = tk.Entry(root)
entry_sulfate.pack(pady=5)

label_conductivity = tk.Label(root, text="Độ dẫn điện:")
label_conductivity.pack(pady=5)
entry_conductivity = tk.Entry(root)
entry_conductivity.pack(pady=5)

label_organic_carbon = tk.Label(root, text="Carbon hữu cơ:")
label_organic_carbon.pack(pady=5)
entry_organic_carbon = tk.Entry(root)
entry_organic_carbon.pack(pady=5)

label_trihalomethanes = tk.Label(root, text="Trihalomethanes:")
label_trihalomethanes.pack(pady=5)
entry_trihalomethanes = tk.Entry(root)
entry_trihalomethanes.pack(pady=5)

label_turbidity = tk.Label(root, text="Độ đục:")
label_turbidity.pack(pady=5)
entry_turbidity = tk.Entry(root)
entry_turbidity.pack(pady=5)

# Button to predict water safety
predict_button = tk.Button(root, text="Kiểm tra độ an toàn của nước", command=predict_water_safety)
predict_button.pack(pady=20)

# Label to display prediction result
result_label = tk.Label(root, text="", font=("Helvetica", 16))
result_label.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
