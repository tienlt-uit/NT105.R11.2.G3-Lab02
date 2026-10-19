import numpy as np
import matplotlib.pyplot as plt

c = 3e8
f = 2.4e9
d = np.logspace(0, np.log10(5000), 500)          
FSL = 20 * np.log10(4 * np.pi * d * f / c)       

P_phat = 20                                     

fig, ax1 = plt.subplots(figsize=(9, 5.5))
ax1.semilogx(d, FSL, "k", linewidth=2, label="FSL (dB)")
ax1.set_xlabel("Khoang cach d (m)")
ax1.set_ylabel("Suy hao FSL (dB)")
ax1.grid(True, which="both")

ax2 = ax1.twinx()                                  
for (Gt, Gr), col in zip([(0, 0), (6, 6), (12, 12)], ["red", "blue", "green"]):
    P_thu = P_phat + Gt + Gr - FSL
    ax2.semilogx(d, P_thu, color=col, linestyle="--",
                 label="P_thu, G=(%d,%d) dBi" % (Gt, Gr))
ax2.set_ylabel("Cong suat thu (dBm)")

l1, n1 = ax1.get_legend_handles_labels()
l2, n2 = ax2.get_legend_handles_labels()
ax1.legend(l1 + l2, n1 + n2, loc="upper center",
           bbox_to_anchor=(0.5, -0.15), ncol=2)
ax1.set_title("Suy hao khong gian tu do va cong suat thu tai 2.4 GHz")
fig.tight_layout()
fig.savefig("Bài 5.png", dpi=130)

for dd in (1, 50, 1000, 5000):
    fsl = 20 * np.log10(4 * np.pi * dd * f / c)
    print("d = %5d m | FSL = %6.2f dB | P_thu (0,0) = %7.2f | (6,6) = %7.2f | (12,12) = %7.2f dBm"
          % (dd, fsl, 20 - fsl, 32 - fsl, 44 - fsl))

plt.show()