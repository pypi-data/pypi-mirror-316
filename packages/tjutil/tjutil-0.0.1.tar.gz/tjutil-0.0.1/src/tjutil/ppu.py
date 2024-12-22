# Description: Prefer gpu device to be used for training and testing.
# PPU = Parallel Processing Unit

import torch

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
