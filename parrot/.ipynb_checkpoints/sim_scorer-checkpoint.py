






from org.apache.pylucene.search import PythonSimpleCollector
from org.apache.pylucene.search.similarities import *


class Scorer(PythonSimilarity.PythonSimScorer):

    def __init__(self, similarity):
        PythonSimilarity.PythonSimScorer.__init__(self)
        self.similarity = similarity
        self.dataset = self.similarity.dataset

    def score(self, doc, freq):

        tf = freq
        dl = 200
        s = 0.25
        qtf = 1
        N = self.dataset.N()
        df = self.similarity.df
        avdl = self.similarity.avdl
        part3 = self.similarity.part3

        part3 = math.log((N + 1) / df)
        part1 = (1 + math.log(1 + math.log(tf))) / ((1 - s) + s * dl / avdl)
        score = part1 * qtf * part3
        return score

        return

    def computeSlopFactor(self, distance):
        return 1.0

    def computePayloadFactor(self, doc, start, end, payload):
        return 1.0


class SimpleSimilarity(PythonSimilarity):

    def __init__(self, dataset):
        PythonSimilarity.__init__(self)
        self.dataset = dataset


    def lengthNorm(self, numTerms):
        return numTerms


    def computeWeight(self, boost, collectionStats, termStats):
        ts = termStats[0]
        self.term = ts.term().utf8ToString()
        self.df = ts.docFreq()
        self.ctf = ts.totalTermFreq()
        C = self.dataset.C()
        N = self.dataset.N()
        self.avdl = C / N
        self.part3 = math.log((N + 1) / self.df)
        return None

    def simScorer(self, weight, context):
        return Scorer(self)











