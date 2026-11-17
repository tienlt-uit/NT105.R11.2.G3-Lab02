import numpy as np
import matplotlib.pyplot as plt
n = 8 # so luong bit tuong ung voi moi mau
n1 = 8000 # tan so lay mau
L = 2 ** n
x = np.linspace(0, 4 * np.pi, 2 * n1 + 1) # x = 0:2*pi/n1:4*pi
s = 8 * np.sin(x)
plt.figure(figsize=(9, 7))
plt.subplot(3, 1, 1)
plt.plot(s)
plt.title("Analog Signal")
plt.ylabel("Amplitude--->")
plt.xlabel("Time--->")
plt.subplot(3, 1, 2)
plt.stem(s)
plt.grid(True)
plt.title("Sampled Signal")
plt.ylabel("Amplitude--->")
plt.xlabel("Sample--->")
# qua trinh quantization
vmax = 8
vmin = -vmax
dl = (vmax - vmin) / L
part = np.linspace(vmin, vmax, L + 1)

code = np.linspace(vmin - dl / 2, vmax + dl / 2, L + 2)
ind = np.searchsorted(part, s)
q = code[ind]
for i in range(len(ind)):
    if ind[i] != 0:
        ind[i] = ind[i] - 1
for i in range(len(q)):
    if q[i] == vmin - dl / 2:
        q[i] = vmin + dl / 2
plt.subplot(3, 1, 3)
plt.stem(q)
plt.grid(True)
plt.title("Quantized Signal")
plt.ylabel("Amplitude--->")
plt.xlabel("Sample--->")
plt.tight_layout()
plt.savefig("pcm_1.png")
# ma hoa nhi phan: moi chi so -> n bit, bit trong so lon truoc
plt.figure(figsize=(9, 3))
coded = []
for i in range(len(ind)):
    word = np.binary_repr(ind[i], width=n)
for j in range(n):
    coded.append(int(word[j]))
plt.grid(True)
plt.step(range(1, len(coded) + 1), coded, where="post")
plt.axis([0, 100, -2, 3])
plt.title("Encoded Signal")
plt.ylabel("Amplitude--->")
plt.xlabel("Time--->")
plt.tight_layout()
plt.savefig("pcm_2.png")
plt.show()