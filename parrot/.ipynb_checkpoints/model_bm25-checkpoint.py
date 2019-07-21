import math
from .model import Model

class BM25Model(Model):

    def __init__(self, b=0.75, k1=1.2, beta=0.1):

        self.b = b; self.k1 = k1; self.beta = beta

    def scoreTerm(self, tf: float, tn: float, dl: float,
                  ql: float, ctf: float, df: float, qtf: float,
                  ctn: float, C: float, N: float):
        b = self.b; k1 = self.k1
        avgdl = C / N
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        tf_part = tf * (k1 + 1)\
                  / (tf + k1 * (1 - b + b * dl / avgdl))
        return tf_part * idf






    def scoreTerm2(self, tf: float, tn: float, dl: float, ql: float, ctf: float,
                  df: float, qtf: float, ctn: float, C: float, N: float):
        k1 = self.k1
        k3 = 1000
        b = self.b
        idf = math.log((N - df + 0.5) / (df + 0.5))
        avgDocLength = C / N
        idfTimesK1PlusOne = idf * (k1 + 1)
        k1TimesOneMinusB = k1 * (1 - b)
        bOverAvgDocLength = b / avgDocLength
        k1TimesBOverAvgDocLength = k1 * bOverAvgDocLength

        norm_qtf = (k3 + 1) * qtf / (k3 + qtf)
        numerator = norm_qtf * tf * idfTimesK1PlusOne
        denominator = tf + k1TimesOneMinusB + k1TimesBOverAvgDocLength * dl

        return numerator / denominator