import numpy as np
import matplotlib.pyplot as plotter


# Hàm để thiết lập bộ lọc thông thấp bằng cách sử dụng numpy
def lowpass_filter(data, cutoff, fs):
    # Tính toán tần số Nyquist
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist

    # Tính toán các hệ số của bộ lọc
    order = 5
    b = np.firwin(order + 1, normal_cutoff)

    # Áp dụng bộ lọc thông thấp
    filtered_data = np.convolve(data, b, mode='same')

    return filtered_data


# Thông số tín hiệu
samplingFrequency = 100  # Tần số lấy mẫu
samplingInterval = 1 / samplingFrequency  # Khoảng thời gian lấy mẫu
beginTime = 0
endTime = 10
signal1Frequency = 4
signal2Frequency = 7

# Tạo các điểm thời gian
time = np.arange(beginTime, endTime, samplingInterval)

# Tạo hai sóng sine
amplitude1 = np.sin(2 * np.pi * signal1Frequency * time)
amplitude2 = np.sin(2 * np.pi * signal2Frequency * time)

# Tạo sóng sine tổng hợp
amplitude = amplitude1 + amplitude2

# Thiết lập bộ lọc thông thấp để lọc tần số 7 Hz
cutoff = 8  # Tần số cắt, lớn hơn tần số cần lọc một chút
filtered_signal = lowpass_filter(amplitude, cutoff, samplingFrequency)

# Vẽ biểu đồ
figure, axis = plotter.subplots(4, 1)
plotter.subplots_adjust(hspace=1)

# Thể hiện sóng sine 1
axis[0].set_title('Sine wave with a frequency of 4 Hz')
axis[0].plot(time, amplitude1)
axis[0].set_xlabel('Time')
axis[0].set_ylabel('Amplitude')

# Thể hiện sóng sine 2
axis[1].set_title('Sine wave with a frequency of 7 Hz')
axis[1].plot(time, amplitude2)
axis[1].set_xlabel('Time')
axis[1].set_ylabel('Amplitude')

# Thể hiện sóng sine tổng hợp
axis[2].set_title('Sine wave with multiple frequencies')
axis[2].plot(time, amplitude)
axis[2].set_xlabel('Time')
axis[2].set_ylabel('Amplitude')

# Thể hiện tín hiệu sau khi lọc
axis[3].set_title('Filtered signal (Lowpass filter)')
axis[3].plot(time, filtered_signal)
axis[3].set_xlabel('Time')
axis[3].set_ylabel('Amplitude')

plotter.show()
