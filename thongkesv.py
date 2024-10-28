import pandas as pd
from numpy import array
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


# Hàm đọc dữ liệu từ file CSV và hiển thị kết quả
def read_csv_and_analyze():
  # Mở hộp thoại để chọn file CSV
  filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

  if not filepath:
    messagebox.showwarning("Chọn file", "Vui lòng chọn một file CSV.")
    return

  try:
    # Đọc dữ liệu từ file CSV
    df = pd.read_csv(filepath, index_col=0, header=0)
    in_data = array(df.iloc[:, :])

    # Tính toán các thông tin cần thiết
    tongsv = in_data[:, 1]  # Cột số sinh viên
    diemA_plus = in_data[:, 2]
    diemA = in_data[:, 3]
    diemB_plus = in_data[:, 4]
    diemB = in_data[:, 5]
    diemC_plus = in_data[:, 6]
    diemC = in_data[:, 7]
    diemD_plus = in_data[:, 8]
    diemD = in_data[:, 9]
    diemF = in_data[:, 10]

    # Tính tổng sinh viên
    total_sv = np.sum(tongsv)
    total_A_plus = np.sum(diemA_plus)
    total_A = np.sum(diemA)
    total_B_plus = np.sum(diemB_plus)
    total_B = np.sum(diemB)
    total_C_plus = np.sum(diemC_plus)
    total_C = np.sum(diemC)
    total_D_plus = np.sum(diemD_plus)
    total_D = np.sum(diemD)
    total_F = np.sum(diemF)

    # Tìm lớp có nhiều sinh viên đạt điểm A+ và A nhất
    maxA_plus = diemA_plus.max()
    i_A_plus = np.argmax(diemA_plus)

    maxA = diemA.max()
    i_A = np.argmax(diemA)

    # Cập nhật kết quả lên giao diện
    result_text.set(f"Tổng số sinh viên: {total_sv}\n"
                    f"Tổng sinh viên đạt điểm A+: {total_A_plus}\n"
                    f"Tổng sinh viên đạt điểm A: {total_A}\n"
                    f"Tổng sinh viên đạt điểm B+: {total_B_plus}\n"
                    f"Tổng sinh viên đạt điểm B: {total_B}\n"
                    f"Tổng sinh viên đạt điểm C+: {total_C_plus}\n"
                    f"Tổng sinh viên đạt điểm C: {total_C}\n"
                    f"Tổng sinh viên đạt điểm D+: {total_D_plus}\n"
                    f"Tổng sinh viên đạt điểm D: {total_D}\n"
                    f"Tổng sinh viên đạt điểm F: {total_F}\n"
                    f"Lớp có nhiều sinh viên đạt điểm A+ nhất là {in_data[i_A_plus, 0]} với {int(maxA_plus)} sinh viên.\n"
                    f"Lớp có nhiều sinh viên đạt điểm A nhất là {in_data[i_A, 0]} với {int(maxA)} sinh viên.")

    # Vẽ biểu đồ
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(diemA_plus)), diemA_plus, 'r-', label="Điểm A+")
    plt.plot(range(len(diemA)), diemA, 'b-', label="Điểm A")
    plt.plot(range(len(diemB_plus)), diemB_plus, 'g-', label="Điểm B+")
    plt.plot(range(len(diemB)), diemB, 'c-', label="Điểm B")
    plt.plot(range(len(diemC_plus)), diemC_plus, 'm-', label="Điểm C+")
plt.plot(range(len(diemC)), diemC, 'y-', label="Điểm C")
    plt.plot(range(len(diemD_plus)), diemD_plus, 'k-', label="Điểm D+")
    plt.plot(range(len(diemD)), diemD, 'gray', label="Điểm D")
    plt.plot(range(len(diemF)), diemF, 'orange', label="Điểm F")
    plt.xlabel('Lớp')
    plt.ylabel('Số sinh viên đạt điểm')
    plt.legend(loc='upper right')
    plt.title('Phân bố số sinh viên đạt các loại điểm theo lớp')
    plt.grid(True)
    plt.show()

  except Exception as e:
    messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi đọc file: {str(e)}")


# Tạo giao diện người dùng
root = tk.Tk()
root.title("Thống kê điểm môn Python K15")

# Khung hiển thị kết quả
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left", padx=10, pady=10)
result_label.pack()

# Nút chọn file CSV
btn_open_file = tk.Button(root, text="Chọn file CSV", command=read_csv_and_analyze, padx=10, pady=10)
btn_open_file.pack()

# Bắt đầu vòng lặp giao diện
root.mainloop()
