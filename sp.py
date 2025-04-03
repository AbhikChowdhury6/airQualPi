import torch.multiprocessing as mp

from sp1 import sp_1

SP1 = mp.Process(target=sp_1, args=())
SP1.start()
