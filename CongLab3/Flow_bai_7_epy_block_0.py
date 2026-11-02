import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self, threshold=0.5):
        gr.sync_block.__init__(
            self,
            name='Switch',
            in_sig=[np.float32, np.float32, np.float32],
            out_sig=[np.float32]
        )
        self.threshold = float(threshold)

    def work(self, input_items, output_items):
        in1 = input_items[0]
        control = input_items[1]
        in3 = input_items[2]
        output_items[0][:] = np.where(control >= self.threshold, in1, in3)
        return len(control)