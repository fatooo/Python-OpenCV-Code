import cv2
import numpy as np
import numba as nb
import time

start = time.time()

@nb.jit(nopython=True, parallel=True)
def f(x,y):
    x=5
    y=4
    return x+y
f(1,2)

stop = time.time()

print(stop-start)