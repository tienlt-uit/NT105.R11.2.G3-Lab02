import matplotlib.pyplot as plt
import numpy as np

f0, fs = 50.0, 10000.0
t = np.arange(0, 0.04, 1/fs)


def square_synth(t, amplitude, f0, k_max):
    out = np.zeros_like(t)
    for k in range(1, k_max + 1):
        out += (1 / (2 * k - 1)) * np.sin(2 * np.pi * (2 * k - 1) * f0 * t)
    return amplitude * (4 / np.pi) * out
fig, axes = plt.subplots(4, 1, figsize=(8, 7), sharex=True)
for ax, k_max in zip(axes, (1, 3, 9, 25)):
    y = square_synth(t, 1.0, f0, k_max)   
    overshoot = (np.max(y) - 1.0) / 1.0 * 100
    print("k_max = %2d | dinh = %.3f | overshoot = %.1f %%" % (k_max, np.max(y), overshoot))
    ax.plot(t, square_synth(t, 1.0, f0, k_max))
    ax.set_title("k = %d" % k_max, fontsize=10)
    ax.set_ylim(-1.4, 1.4)
    ax.grid(True)

axes[-1].set_xlabel("Thoi gian (s)")
fig.suptitle("Cang nhieu song Harmonic, cang gan song vuong")
fig.tight_layout()
fig.savefig("Bài 4-1.png", dpi=250)

k_nyq = int((fs / 2 / f0 + 1) // 2)
print("k_max lon nhat thoa Nyquist:", k_nyq)
print("Harmonic cao nhat:", (2 * k_nyq - 1) * f0, "Hz")

fig3, axes3 = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
for ax, k in zip(axes3, (k_nyq, 150)):
    ax.plot(t, square_synth(t, 1.0, f0, k))
    ax.set_title("k_max = %d" % k)
    ax.set_ylim(-1.6, 1.6)
    ax.grid(True)
axes3[-1].set_xlabel("Thoi gian (s)")
fig3.tight_layout()
fig3.savefig("Bài 4-2.png", dpi=130)


fig4, axes4 = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

for ax, k in zip(axes4, (k_nyq, 150)):
    y = square_synth(t, 1.0, f0, k)
    X = np.fft.rfft(y)
    freqs = np.fft.rfftfreq(len(y), 1/fs)
    mag = 2 * np.abs(X) / len(y)          
    n = freqs / f0
    ly_thuyet = np.where(n > 0, 4 / (np.pi * np.maximum(n, 1)), 0)

    ax.stem(freqs, mag, label="Pho tinh duoc")
    ax.plot(freqs, ly_thuyet, "r--", label="Ly thuyet 4/(pi*n)")
    ax.set_xlim(4000, 5000)                
    ax.set_ylim(0, 0.02)
    ax.set_title("Pho mot ben, k_max = %d" % k)
    ax.set_ylabel("Bien do")
    ax.legend(loc="upper right")
    ax.grid(True)

    overshoot = (np.max(y) - 1.0) * 100
    i = np.argmin(np.abs(freqs - 4950))
    print("k_max = %3d | overshoot = %.1f %% | vach 4950 Hz = %.4f (ly thuyet %.4f)"
          % (k, overshoot, mag[i], 4 / (np.pi * 99)))

axes4[-1].set_xlabel("Tan so (Hz)")
fig4.tight_layout()
fig4.savefig("Bài 4-3.png", dpi=130)
plt.show()