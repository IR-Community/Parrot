

import math
from .model import Model


class DLMModel(Model):
    

    def score_term(self, tf: float, tn: float, dl: float, ql: float, ctf: float,
                  df: float, qtf: float, ctn: float, C: float, N: float):


        collectionFrequency = (1.0 + ctf) / (1.0 + C)

        mu = 2500;

        muTimesCollectionFrequency = mu * collectionFrequency

        seen = (tf + muTimesCollectionFrequency) / (dl + mu)

        score = qtf * math.log(1.0 + seen)

        return score