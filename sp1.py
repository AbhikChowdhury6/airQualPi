import torch.multiprocessing as mp

from sp2 import sp_2

def sp_1():
    SP2 = mp.Process(target=sp_2, args=())
    SP2.start()