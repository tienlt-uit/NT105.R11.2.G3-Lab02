import numpy as np 
import matplotlib.pyplot as plt 
 
N = 200 
 
def hdb3(bits, bitrate=1.0):
    levels = []
    last_pulse = -1 # Cực tính xung 1 gần nhất
    count_ones_since_last_sub = 0 # Đếm số bit 1 từ lần thay thế trước
    i = 0
    while i < len(bits):
        if bits[i] == 1:
            last_pulse = -last_pulse
            levels.append(last_pulse)
            count_ones_since_last_sub += 1
            i += 1
        else:
            # Đếm số 0 liên tiếp
            zeros = 0
            while i + zeros < len(bits) and bits[i + zeros] == 0:
                zeros += 1
            
            if zeros >= 4:
                if count_ones_since_last_sub % 2 == 0:
                    # Số chẵn bit 1 -> thay bằng 000V (V cùng cực với xung trước)
                    levels.extend([0, 0, 0, last_pulse])
                else:
                    # Số lẻ bit 1 -> thay bằng B00V (B ngược cực xung trước)
                    levels.extend([-last_pulse, 0, 0, last_pulse])
                count_ones_since_last_sub = 0
                i += 4
            else:
                levels.extend([0] * zeros)
                i += zeros
    x = np.repeat(levels, N)
    t = np.linspace(0, len(bits)/bitrate, x.size)
    return t, x
 
 
bits = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1] 
t, x = hdb3(bits) 
 
plt.figure(figsize=(10, 2.8)) 
plt.plot(t, x, linewidth=3) 
plt.axis([0, t[-1], -1.1, 1.1]) 
plt.xticks(np.arange(0, len(bits) + 1, 2)) 
plt.grid(True) 
plt.title("HDB3: [%s]" % " ".join(str(b) for b in bits)) 
plt.tight_layout() 
plt.savefig("hdb3.png", dpi=130) 