
import math
from parrot.core import *


class NTFIDFModel(Model):

    def score_term(self, tf: float, tn: float, dl: float, ql: float, ctf: float,
                  df: float, qtf: float, ctn: float, C: float, N: float):

        idf = math.log((N + 1) / (ctf + 0.1))
        avgDocLength = C / N
        omega = 2.0 / (1 + math.log(1 + ql) / math.log(2.0))
        cf = ctf / df
        idfAndCf = idf * (cf / (1 + cf))
        tfNorm = tf / (dl / tn)
        tfNormF = omega * tfNorm / (1 + tfNorm)
        dlNorm = tf * math.log(1 + avgDocLength / dl) / math.log(2.0)
        dlNormF = (1 - omega) * dlNorm / (1 + dlNorm)
        score = (tfNormF + dlNormF) * idfAndCf
        return qtf * score