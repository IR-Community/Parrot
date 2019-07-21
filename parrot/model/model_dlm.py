

import math
from parrot.core import *


class DLMModel(Model):

    def score_term(self, tf: float, tn: float, dl: float, ql: float, ctf: float,
                   df: float, qtf: float, ctn: float, C: float, N: float):
        mu = 2500
        delta = 0.05
        collectionFrequency = ctf / C
        deltaPart = math.log(1.0 + delta / collectionFrequency)
        score = math.log(1 + tf / collectionFrequency) + deltaPart + ql * math.log(mu / (mu + dl))

        return qtf * score