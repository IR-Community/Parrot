
import math
from .model import Model


class BM25RTFModel(Model):

    def __init__(self, b=0.75, k1=1.2, k3=1000):
        self.b = b
        self.k1 = k1
        self.k3 = k3

    def scoreTerm(self, tf: float, dtn: float, dl: float, ql: float, ctf: float,
                  df: float, qtf: float, ctn: float, C: float, N: float):
        k1 = self.k1
        k3 = self.k3
        b = self.b

        avgtf = dl / dtn

        tf = tf + 20 * pow( (tf - avgtf) / (10 * avgtf) , 3)

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