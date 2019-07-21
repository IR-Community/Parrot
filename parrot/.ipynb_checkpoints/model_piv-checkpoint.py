import math
from .model import Model

class PIVModel(Model):

    def __init__(self, s=0.25):
        self.s = s

    def scoreTerm(self, tf: float, dtn: float, dl: float, ql: float, ctf: float,
                  df: float, qtf: float, ctn: float, C: float, N: float):
        s = self.s
        avdl = C / N
        part3 = math.log((N + 1) / df)
        part1 = (1 + math.log(1 + math.log(tf))) / ((1 - s) + s * dl / avdl)
        score = part1 * qtf * part3
        return score