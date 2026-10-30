import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self, distance=1.0, freq=2.4e9, snr_db=30.0):
        gr.sync_block.__init__(
            self,
            name='Channel',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.distance = distance
        self.freq = freq
        self.snr_db = snr_db
        self.rng = np.random.default_rng(0)

        # Tính suy hao không gian tự do (FSL)
        c = 299792458.0
        lam = c / freq
        fsl = (4 * np.pi * distance / lam) ** 2 
        
        # THÊM DÒNG NÀY: Hệ số Gain để tín hiệu không bị chìm về 0 trên đồ thị
        Gain = 1000.0 
        
        # Sửa công thức: nhân thêm Gain vào trước khi lấy căn bậc 2
        self.atten = np.sqrt(Gain / fsl) 

    def work(self, input_items, output_items):
        x = input_items[0]
        out = output_items[0]

        # 1. Suy hao tín hiệu
        y = x * self.atten

        # 2. Cộng nhiễu Gauss
        sig_power = np.mean(x ** 2) * self.atten ** 2
        noise_power = sig_power / (10 ** (self.snr_db / 10))
        sigma = np.sqrt(noise_power)
        y = y + self.rng.normal(0.0, sigma, len(y))

        out[:] = y
        return len(out)