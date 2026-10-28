import numpy as np 
import matplotlib.pyplot as plt 
 
N = 200 
HALF = N // 2 
 
 
def diff_manchester(bits, bitrate=1.0):
    levels = []
    current_level = -1 # Mức khởi đầu
    for b in bits:
        # Xử lý đầu bit
        if b == 0:
            current_level = -current_level # Đảo mức
        # Giữa bit luôn đảo mức
        levels.append(current_level)
        current_level = -current_level
        levels.append(current_level)
    x = np.repeat(levels, N//2) # Nửa bit là N//2 mẫu
    t = np.linspace(0, len(bits)/bitrate, x.size)
    return t, x
 
 
bits = [1, 0, 1, 0, 0, 1, 0, 1, 1, 0] 
t, x = diff_manchester(bits) 
 
plt.figure(figsize=(9, 2.6)) 
plt.plot(t, x, linewidth=3) 
plt.axis([0, t[-1], -1.1, 1.1]) 
plt.xticks(np.arange(len(bits) + 1)) 
plt.grid(True) 
plt.title("Differential Manchester: [%s]"           % " ".join(str(b) for b in bits)) 
plt.tight_layout() 
plt.savefig("diff_manchester.png", dpi=130) 
