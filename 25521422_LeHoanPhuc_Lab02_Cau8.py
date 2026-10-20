import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self, samp_rate=32000, f0=1000, k_max=5, amplitude=1.0):
        gr.sync_block.__init__(
            self,
            name='Square Synth',
            in_sig=None, # Không có cổng vào
            out_sig=[np.float32]
        )
        self.samp_rate = samp_rate
        self.f0 = f0
        self.k_max = k_max
        self.amplitude = amplitude
        self.phase = 0.0

        # Kiểm tra Nyquist
        if k_max * f0 >= samp_rate / 2:
            k_max_valid = int((samp_rate / 2) // f0) - 1
            print(f"CANH BAO: k_max*f0 = {k_max*f0} Hz vuot qua Nyquist! k_max toi da hop le la: {k_max_valid}")

    def work(self, input_items, output_items):
        out = output_items[0]
        n = len(out)
        t = (np.arange(n) + self.phase) / self.samp_rate
        
        # Tính tổng chuỗi Fourier
        s = np.zeros(n, dtype=np.float64)
        for k in range(1, self.k_max + 1, 2): 
            s += np.sin(2 * np.pi * k * self.f0 * t) / k
            
        out[:] = self.amplitude * (4 / np.pi) * s
        self.phase += n
        return n