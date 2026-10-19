import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

rng = np.random.default_rng(0)
#Tín hiệu tương tự
t1 = np.linspace(0, 1.0, 201)
x = 4 + 0.5 * np.sin(2 * np.pi * 3 * t1)
x = x + 0.1 * rng.standard_normal(201)



#Tín hiệu số
bits = np.array([1, 1, 0, 1, 0, 0 , 1, 0])
samples_per_bit = 50
wave = np.repeat(bits, samples_per_bit)
t2 = np.arange(wave.size) / samples_per_bit
print("Chuoi bit :", bits)
print("So mau sau khi lap:", wave.size)




#Tín hiệu tuần hoàn
fs = 10000 
f0 = 25 
t3 = np.arange(0, 0.1, 1 / fs)
sawtooth = signal.sawtooth(2 * np.pi * f0 * t3)
period = 1 / f0
print("Chu ky T =", period, "s")
print("So chu ky trong cua so 0.1 s:", 0.1 / period)



fig, axes = plt.subplots(3, 1, figsize=(8, 7))

axes[0].plot(t1, x)
axes[0].set_title("Tin hieu tuong tu")
axes[0].set_xlabel("Thoi gian (s)")
axes[0].set_ylabel("Bien do (V)")
axes[0].set_ylim(0, 6)
axes[0].grid(True)

axes[1].plot(t2, wave)
axes[1].set_title("Tin hieu so")
axes[1].set_xlabel("Thoi gian (don vi bit)")
axes[1].set_ylabel("Bien do (V)")
axes[1].set_ylim(-0.5, 1.5)
axes[1].grid(True)

axes[2].plot(t3, sawtooth)
axes[2].set_title("Tin hieu tuan hoan - song rang cua 25 Hz")
axes[2].set_xlabel("Thoi gian (s)")
axes[2].set_ylabel("Bien do (V)")
axes[2].grid(True)

fig.tight_layout()
fig.savefig("Bài 1.png")
plt.show()

