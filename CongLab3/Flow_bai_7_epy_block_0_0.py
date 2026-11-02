import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self, samp_rate=32000, bit_rate=500.0,
                 minimum=0.0, maximum=1.0, seed=0):
        gr.sync_block.__init__(
            self,
            name='Random Number',
            in_sig=None,
            out_sig=[np.float32]
        )
        self.minimum = float(minimum)
        self.maximum = float(maximum)
        self.spb = int(samp_rate / bit_rate)
        self.rng = np.random.default_rng(int(seed))
        self.set_output_multiple(self.spb)

    def work(self, input_items, output_items):
        count = len(output_items[0])
        nbit = count // self.spb
        values = self.rng.uniform(self.minimum, self.maximum, nbit)
        output_items[0][:] = np.repeat(values, self.spb)
        return count