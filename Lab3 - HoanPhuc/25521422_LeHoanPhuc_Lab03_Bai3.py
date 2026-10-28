import numpy as np
import matplotlib.pyplot as plt

N = 200

def pseudoternary(bits, bitrate=1.0):
    levels = []
    last = 1 # Cực tính xung kế tiếp (bắt đầu từ dương)
    for b in bits:
        if b == 0:
            levels.append(last)
            last = -last # Đảo cực cho bit 0 tiếp theo
        else:
            levels.append(0) # Bit 1 là mức 0
    x = np.repeat(levels, N)
    t = np.linspace(0, len(bits) / bitrate, x.size)
    return t, x

bits = [1, 0, 1, 0, 0, 1, 0, 1, 1, 0]
t, x = pseudoternary(bits)

plt.figure(figsize=(9, 2.6))
plt.plot(t, x, linewidth=3)
plt.axis([0, t[-1], -1.1, 1.1])
plt.xticks(np.arange(len(bits) + 1))
plt.grid(True)
plt.title("Pseudoternary: [%s]" % " ".join(str(b) for b in bits))
plt.tight_layout()
plt.show()