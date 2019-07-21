import math
from parrot.core import *

class BM25Model(Model):

    def __init__(self, b=0.75, k1=1.2):
        self.b = b
        self.k1 = k1

    def score_term(self, tf: float, tn: float, dl: float,
                  ql: float, ctf: float, df: float, qtf: float,
                  ctn: float, C: float, N: float):
        b = self.b; k1 = self.k1
        avgdl = C / N
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        tf_part = tf * (k1 + 1)\
                  / (tf + k1 * (1 - b + b * dl / avgdl))
        return tf_part * idf

