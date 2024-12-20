import pkgutil

from io import BytesIO

import torch
import numpy as np

class NoCJKLogitsProcessor:
    def __init__(self):
        data = pkgutil.get_data(__name__, "data/qwen-cjk.npy")
        self.np_mask = np.load(BytesIO(data))
        self.mask = None

    def __call__(self, _, logits):
        if self.mask is None:
            self.mask = torch.from_numpy(self.np_mask).to(logits.device)
            
        logits.masked_fill_(self.mask, float("-inf"))
        return logits