import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self, code='NRZ-L', samples_per_bit=64, seed=0):
        gr.sync_block.__init__(self, name='Line Code Source',
                               in_sig=None, out_sig=[np.float32])
        self.code = str(code)
        self.spb = int(samples_per_bit)
        self.rng = np.random.default_rng(int(seed))
        self.nrzi_level = 0.0
        self.ami_last = -1.0
        self.set_output_multiple(self.spb)

    def encode(self, bits):
        c = self.code.upper()
        spb, half = self.spb, self.spb // 2
        if c == 'NRZ-L':
            return np.repeat(np.where(bits == 1, 0.0, 1.0), spb)
        if c == 'NRZI':
            lv = []
            for b in bits:
                if b == 1:
                    self.nrzi_level = 1.0 - self.nrzi_level
                lv.append(self.nrzi_level)
            return np.repeat(lv, spb)
        if c == 'AMI':
            lv = []
            for b in bits:
                if b == 1:
                    self.ami_last = -self.ami_last
                    lv.append(self.ami_last)
                else:
                    lv.append(0.0)
            return np.repeat(lv, spb)
        if c == 'MANCHESTER':
            out = []
            for b in bits:
                a, d = (1.0, -1.0) if b == 0 else (-1.0, 1.0)
                out += [a] * half + [d] * (spb - half)
            return np.array(out)
        raise ValueError('code khong hop le')

    def work(self, input_items, output_items):
        out = output_items[0]
        nbit = len(out) // self.spb
        bits = self.rng.integers(0, 2, nbit)
        out[:nbit * self.spb] = self.encode(bits)
        return nbit * self.spb