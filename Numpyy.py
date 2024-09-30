import numpy as np

# Tạo một mảng NumPy từ một danh sách
a = np.array([1, 2, 3, 4, 5])

# Tạo một mảng NumPy với các số từ 0 đến 9
b = np.arange(10)

# Tính toán cơ bản trên mảng
c = a + 10    # Thêm 10 vào mỗi phần tử của mảng a
d = a * 2     # Nhân mỗi phần tử của mảng a với 2
e = a**2      # Bình phương mỗi phần tử của mảng a

# Tính tổng các phần tử trong mảng
total_sum = np.sum(a)

# Tính trung bình các phần tử trong mảng
mean_value = np.mean(a)

# Tính phần tử lớn nhất và nhỏ nhất
max_value = np.max(a)
min_value = np.min(a)

# Hiển thị kết quả
print("Mảng a:", a)
print("Mảng b:", b)
print("Mảng c (a + 10):", c)
print("Mảng d (a * 2):", d)
print("Mảng e (a^2):", e)
print("Tổng các phần tử của a:", total_sum)
print("Trung bình của a:", mean_value)
print("Phần tử lớn nhất của a:", max_value)
print("Phần tử nhỏ nhất của a:", min_value)
