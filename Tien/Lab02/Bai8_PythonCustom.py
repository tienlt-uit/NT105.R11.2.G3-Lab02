"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

class SquareSynth(gr.sync_block):
    """
    Khoi nguon tong hop song vuong bang chuoi Fourier:
    x(t) = amplitude * (4 / pi) * SUM [ (1 / k) * sin(2 * pi * k * f0 * t) ]
    voi k chay cac so le: 1, 3, 5, ..., k_max
    """
    def __init__(self, samp_rate=32000.0, f0=1000.0, k_max=5, amplitude=1.0):
        gr.sync_block.__init__(
            self,
            name='Square Synth',
            in_sig=None,                     # Khoi nguon (Source) khong co dau vao
            out_sig=[np.float32]             # Dau ra tin hieu thuc kieu float
        )
        self.samp_rate = float(samp_rate)
        self.f0 = float(f0)
        self.k_max = int(k_max)
        self.amplitude = float(amplitude)
        
        # Bien luu vi tri mau thoi gian t de tin hieu lien tuc giua cac goi mau
        self.n = 0

        # Kiem tra dieu kien tan so Nyquist
        nyquist_limit = self.samp_rate / 2.0
        if self.k_max * self.f0 >= nyquist_limit:
            k_valid_max = int((nyquist_limit - 1) // self.f0)
            if k_valid_max % 2 == 0:
                k_valid_max -= 1
            print(f"\n[CANH BAO NYQUIST]: k_max * f0 ({self.k_max * self.f0} Hz) >= samp_rate / 2 ({nyquist_limit} Hz)!")
            print(f"--> Gia tri k_max lon nhat hop le de tranh chong pho: {k_valid_max}\n")

    def work(self, input_items, output_items):
        out = output_items[0]
        n_samples = len(out)

        # Tao truc thoi gian t cho block mau hien tai
        t = (self.n + np.arange(n_samples)) / self.samp_rate
        
        # Khoi tao mang gia tri 0
        signal = np.zeros(n_samples, dtype=np.float32)

        # Cong chuoi Fourier cac song hai bac le: 1, 3, 5, ..., k_max
        for k in range(1, self.k_max + 1, 2):
            signal += (1.0 / k) * np.sin(2.0 * np.pi * k * self.f0 * t)

        # Nhan he so (4/pi) cua song vuong va bien do amplitude
        signal = signal * (4.0 / np.pi) * self.amplitude

        out[:] = signal
        self.n += n_samples  # Cap nhat tong so mau da phat
        return len(out)