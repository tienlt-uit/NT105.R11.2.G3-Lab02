import matplotlib.pyplot as plt
import numpy as np
fs = 10000
f0 = 50
t = np.arange(0, 0.1, 1 / fs)
phases = [0, 90, 180, 270]
labels = ["pha 0", "pha 90 độ", "pha 180 độ", "pha 270 độ"]
plt.figure(figsize=(8, 3.2))
for phase, label in zip(phases, labels):
    plt.plot(t, np.sin(2 * np.pi * f0 * t + np.radians(phase)), label=label)

T = 1/f0
T_points = np.array([ 0, T/4, T/2, 3*T/4])
for phase in (0, 90, 180, 270):
    y = np.sin(2 * np.pi * f0 * T_points + np.deg2rad(phase))
    print(phase, "do: ", np.round(y,2))


plt.title("Song sin 50 Hz voi bon gia tri pha ban dau")
plt.xlabel("Thoi gian (s)")
plt.ylabel("Bien do (V)")
plt.legend(loc="upper right")
plt.grid(True)
plt.tight_layout()

plt.savefig("Bài 2.png")
plt.show()