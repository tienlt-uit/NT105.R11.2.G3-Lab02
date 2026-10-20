"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

class Channel(gr.sync_block):
    """
    Khoi mo phong kenh truyen:
    - Suy hao bien do theo khoang cach: h = 1.0 / distance
    - Cong them nhieu trang Gauss (AWGN) theo chi so snr_db
    """
    def __init__(self, distance=1.0, frequency=2.4e9, snr_db=30.0):
        gr.sync_block.__init__(
            self,
            name='Channel',
            in_sig=[np.float32],    # Dau vao Float
            out_sig=[np.float32]    # Dau ra Float
        )
        self.distance = float(distance)
        self.frequency = float(frequency)
        self.snr_db = float(snr_db)

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        # 1. Tinh suy hao bien do theo khoang cach (d cang lon thi bien do cang giam)
        # He so suy hao bien do: h = 1.0 / distance
        attenuation = 1.0 / max(self.distance, 1e-6)
        attenuated_signal = in0 * attenuation

        # 2. Tinh toan va cong them nhieu trang Gauss (AWGN)
        sig_power = np.mean(attenuated_signal**2)
        if sig_power > 1e-12:
            snr_linear = 10.0 ** (self.snr_db / 10.0)
            noise_power = sig_power / snr_linear
            noise = np.random.normal(0.0, np.sqrt(noise_power), len(in0)).astype(np.float32)
        else:
            noise = 0.0

        out[:] = attenuated_signal + noise
        return len(out)