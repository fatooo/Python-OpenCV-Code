from numba import vectorize
from numba import jit

@jit(forceobj=True,parallel=True)
#@vectorize(["int32(int32,int32)"],target="cpu")
def fish_eye_correct(frame, coords_T):

    t_rasa = (frame[tuple(coords_T)]).reshape((1080, 1920,3))

    return t_rasa
