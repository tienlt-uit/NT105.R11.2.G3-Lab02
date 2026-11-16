import numpy as np
import matplotlib.pyplot as plt
def nrz(bits, bitrate):
    N = 100 
    s = np.repeat(bits, N)
    t = np.arange(len(s)) / (N * bitrate)
    return t, s
a = 2
plt.figure(figsize=(9, 6))
plt.subplot(2, 1, 1)
t = np.linspace(0, 2 * np.pi, 101) 
x = a * np.sin(t)
l = len(x)
plt.plot(range(1, l + 1), x, "r")
delta = 0.2
xn = [0]
d = []
for i in range(l):
    if x[i] >= xn[i]:
        d.append(1)
        xn.append(xn[i] + delta)
    else:
        d.append(0)
        xn.append(xn[i] - delta)
plt.step(range(1, l + 2), xn, where="post")
plt.title(f"delta = {delta}, {l - 1} khoang/chu ky")
plt.plot(range(1, l + 2), xn, "c")
plt.subplot(2, 1, 2)
bitrate = 1
t, s = nrz(d, bitrate)
plt.plot(t, s, linewidth=3)
plt.axis([0, t[-1], -0.1, 1.1])
plt.grid(True)
plt.title("NRZ: " + " ".join(str(b) for b in d), fontsize=7)
plt.savefig("dm_d.png")
plt.show()