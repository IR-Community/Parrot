import math
from .model import Model

class PIVRTFModel(Model):

    def __init__(self, s=0.25):
        self.s = s

    def scoreTerm(self, tf: float, dtn: float, dl: float, ql: float, ctf: float,
                  df: float, qtf: float, ctn: float, C: float, N: float):
        s = self.s

        avgtf = dl / dtn

        tf = tf + 20 * pow((tf - avgtf) / (10 * avgtf), 3)

        avdl = C / N
        part1 = (1 + math.log(1 + math.log(tf))) / ((1 - s) + s * dl / avdl)
        part3 = math.log( (N + 1) / df )
        score = part1 * qtf * part3
        return score