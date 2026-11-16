import numpy as np
import matplotlib.pyplot as plt

n = 8
n1 = 8000
L = 2**n
x = np.linspace(0, 4 * np.pi, 2 * n1 + 1) 
s = 8 * np.sin(x)

def pcm_decode(coded, n, vmin, dl):
    bits = np.array(coded).reshape(-1, n)         
    weights = 2 ** np.arange(n - 1, -1, -1)       
    idx = bits @ weights                          
    return vmin + dl/2 + idx * dl                 # q = vmin + Δ/2 + i·Δ

plt.figure(figsize = (9, 7))
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

#quantization
vmax = 8
vmin = -vmax
dl = (vmax - vmin)/L
part = np.linspace(vmin, vmax, L+1)
code = np.linspace(vmin - dl/2, vmax + dl/2, L+2)
ind = np.searchsorted(part, s)
q = code[ind]
for i in range (len(ind)):
    if ind[i] != 0:
        ind[i] = ind[i] - 1
for i in range (len(q)):
    if q[i] == vmin - dl/2:
        q[i] = vmin + dl/2
plt.subplot(3, 1, 3)
plt.stem(q)
plt.grid(True)
plt.title("Quantized Signal")
plt.ylabel("Amplitude--->")
plt.xlabel("Sample--->")
plt.tight_layout()
plt.savefig("pcm_1.png")

#Mã hóa nhị phân
plt.figure(figsize=(9, 6))
coded = []
for i in range(len(ind)):
    word = np.binary_repr(ind[i], width=n)
    for j in range(n):
        coded.append(int(word[j]))
plt.subplot(2, 1, 1)
plt.grid(True)
plt.step(range(1, len(coded) + 1), coded, where="post")
plt.axis([0, 100, -2, 3])
plt.title("Encoded Signal")
plt.ylabel("Amplitude--->")
plt.xlabel("Time--->")

#Giải mã
dq = pcm_decode(coded, n, vmin, dl)
plt.subplot(2, 1, 2)
plt.stem(dq)
plt.grid(True)
plt.title("Demodulated Signal")
plt.ylabel("Amplitude--->")
plt.xlabel("Sample--->")
plt.tight_layout()
plt.savefig(f"pcm_2_n{n}.png")

#In số liệu cho bảng
print("n =", n)
print("So muc luong tu L      :", L)
print("Buoc luong tu delta    :", dl)
print("So bit moi tu ma       :", n)
print("So mau                 :", len(s))
print("Tong so bit sau ma hoa :", len(coded))
print("Sai so luong tu lon nhat:", np.max(np.abs(s - q)))
print("Giai ma trung Quantized:", np.allclose(dq, q))
plt.show()

