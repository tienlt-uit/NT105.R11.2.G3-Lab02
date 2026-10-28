import numpy as np
import matplotlib.pyplot as plt

N = 200 # Số mẫu mỗi bit
bits = [1, 0, 0, 0, 1, 1, 1, 0, 0, 1]

# 1. Hàm mã hóa NRZ-L (Bit 0: mức cao (1), Bit 1: mức thấp (0))
def nrz_l(bits, bitrate=1.0):
    levels = []
    for b in bits:
        levels.append(0 if b == 1 else 1) # 1 -> 0, 0 -> 1
    x = np.repeat(levels, N)
    t = np.linspace(0, len(bits)/bitrate, x.size)
    return t, x

# 2. Hàm mã hóa NRZI (Bit 0: giữ nguyên mức, Bit 1: đảo mức)
def nrzi(bits, bitrate=1.0, start_level=0):
    levels = []
    current_level = start_level
    for b in bits:
        if b == 1:
            current_level = 1 - current_level # Đảo mức
        levels.append(current_level)
    x = np.repeat(levels, N)
    t = np.linspace(0, len(bits)/bitrate, x.size)
    return t, x

# Vẽ đồ thị
t_nrzl, x_nrzl = nrz_l(bits)
t_nrzi, x_nrzi = nrzi(bits, start_level=0) # Bắt đầu mức thấp
t_nrzi_inv, x_nrzi_inv = nrzi(bits, start_level=1) # Bắt đầu mức cao

plt.figure(figsize=(10, 8))

plt.subplot(3, 1, 1)
plt.plot(t_nrzl, x_nrzl, linewidth=2.5)
plt.title("NRZ-L")
plt.xticks(np.arange(len(bits) + 1))
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(t_nrzi, x_nrzi, linewidth=2.5, color='orange')
plt.title("NRZI (Bắt đầu mức thấp)")
plt.xticks(np.arange(len(bits) + 1))
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(t_nrzi_inv, x_nrzi_inv, linewidth=2.5, color='green')
plt.title("NRZI (Bắt đầu mức cao)")
plt.xticks(np.arange(len(bits) + 1))
plt.grid(True)

plt.tight_layout()
plt.show()