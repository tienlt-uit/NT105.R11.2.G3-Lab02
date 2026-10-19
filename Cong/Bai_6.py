import numpy as np
import math
import matplotlib.pyplot as plt

rng = np.random.default_rng(0)
N_bits = 20000
spb = 4                                           

#Phát
bits = rng.integers(0, 2, N_bits)
symbols = np.where(bits == 1, 1.0, -1.0)           # 1 -> +1 V, 0 -> -1 V
tx = np.repeat(symbols, spb)                       # mỗi bit giữ 4 mẫu

#Kênh
c, f, d = 3e8, 2.4e9, 50 #với c là tốc độ ánh sáng, f là tần số sóng mang, d là khoảng cách truyền
FSL_dB = 20 * np.log10(4 * np.pi * d * f / c)       #Công thức độ suy hao
alpha = 10 ** (-FSL_dB / 20)                       
print("FSL tai 50 m = %.2f dB -> he so bien do = %.3e" % (FSL_dB, alpha))
rx_clean = alpha * tx
P_sig = np.mean(rx_clean ** 2)                     # công suất tín hiệu sau suy hao

#Quét SNR
snr_db_list = np.arange(-8, 9, 1)                  
ber_list = []
for snr_db in snr_db_list:
    P_noise = P_sig / (10 ** (snr_db / 10))
    noise = rng.normal(0, np.sqrt(P_noise), rx_clean.size)
    rx = rx_clean + noise                          # cộng nhiễu Gauss

    # Thu
    avg = rx.reshape(N_bits, spb).mean(axis=1)
    bits_hat = (avg > 0).astype(int)

    # Đo
    n_err = np.sum(bits_hat != bits)
    ber = n_err / N_bits
    ber_list.append(ber)
    ber_th = 0.5 * math.erfc(math.sqrt(spb * 10 ** (snr_db / 10) / 2))
    print("SNR = %+3d dB | so bit sai = %5d | BER = %.2e | BER ly thuyet = %.2e"
          % (snr_db, n_err, ber, ber_th))

ber_arr = np.array(ber_list, dtype=float)
ber_plot = np.where(ber_arr > 0, ber_arr, np.nan)  

# Đồ thị
snr_fine = np.linspace(-8, 8, 200)
ber_theory = np.array([0.5 * math.erfc(math.sqrt(spb * 10 ** (s / 10) / 2))
                       for s in snr_fine])

plt.figure(figsize=(8, 5))
plt.semilogy(snr_db_list, ber_plot, "o", label="Mo phong")
plt.semilogy(snr_fine, ber_theory, "r-", label="Ly thuyet")
plt.xlabel("SNR (dB)")
plt.ylabel("BER")
plt.title("BER cua NRZ luong cuc, 4 mau/bit")
plt.grid(True, which="both")
plt.legend()
plt.tight_layout()
plt.savefig("bai6.png", dpi=250)
plt.show()