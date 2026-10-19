import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

fs = 10000
f0 = 100
t = np.arange(0, 0.1, 1 / fs)

wave_20 = (signal.square(2 * np.pi * f0 * t, duty = 0.2) + 1)/2
wave_50 = (signal.square(2 * np.pi * f0 * t, duty = 0.5) + 1)/2
wave_80 = (signal.square(2 * np.pi * f0 * t, duty = 0.8) + 1)/2

print ("Ti le mau o muc cao, song 20%%: %.1f %%" % (np.mean(wave_20 > 0)*100))
print ("Ti le mau o muc cao, song 50%%: %.1f %%" % (np.mean(wave_50 > 0)*100))
print ("Ti le mau o muc cao, song 80%%: %.1f %%" % (np.mean(wave_80 > 0)*100))

print ("Trung binh mau o muc cao, song 20%%: %.2f" % (np.mean(wave_20)))
print ("Trung binh mau o muc cao, song 50%%: %.2f" % (np.mean(wave_50)))
print ("Trung binh mau o muc cao, song 80%%: %.2f" % (np.mean(wave_80)))

fig, axes = plt.subplots(3, 1, figsize=(8, 7))
axes[0].plot(t, wave_20, color = "red", linewidth=2.5, label="100Hz, duty 20%")  
axes[0].set_xlabel("Thoi gian (s)")
axes[0].set_ylabel("Bien do (V)")
axes[0].legend(loc="upper right")
axes[0].grid(True)


axes[1].plot(t, wave_50, color = "blue", linewidth=2.5, label="100Hz, duty 50%")
axes[1].set_xlabel("Thoi gian (s)")
axes[1].set_ylabel("Bien do (V)")
axes[1].legend(loc="upper right")
axes[1].grid(True)


axes[2].plot(t, wave_80, color = "green", linewidth=2.5, label="100Hz, duty 80%")
axes[2].set_xlabel("Thoi gian (s)")
axes[2].set_ylabel("Bien do (V)")
axes[2].legend(loc="upper right")
axes[2].grid(True)


fig.tight_layout()
fig.savefig("Bài 3-1.png")

######################################
#Phổ một bên
######################################
fig2, axes2 = plt.subplots(3, 1, figsize=(9, 7))

waves = [wave_20, wave_50, wave_80]
names = ["100Hz, duty 20%", "100Hz, duty 50%", "100Hz, duty 80%"]
colors = ["red", "blue", "green"]

for i in range (3):
    X = np.fft.rfft(waves[i])
    freq = np.fft.rfftfreq(len(waves[i]), 1/fs)
    mag = np.abs(X) / len(waves[i])

    axes2[i].stem(freq, mag, linefmt=colors[i])
    axes2[i].set_xlim(0, 1000)
    axes2[i].set_title("Pho mot ben - " + names[i])
    axes2[i].set_xlabel("Tan so (Hz)")
    axes2[i].set_ylabel("|X(f)|")
    axes2[i].grid(True)

    print(names[i], "- vach DC:", round(mag[0], 3), "| np.mean:", round(np.mean(waves[i]), 3))

fig2.tight_layout()
fig2.savefig("Bài 3-2.png", dpi=250)

plt.show()