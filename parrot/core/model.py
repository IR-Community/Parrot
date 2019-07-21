import lucene

from org.apache.lucene.search.similarities import *
from org.apache.lucene.analysis.en import *
from org.apache.lucene.analysis.standard import *
from org.apache.lucene.document import *
from org.apache.lucene.search import *
from org.apache.lucene.index import *
from org.apache.lucene.queryparser.classic import *
from org.apache.lucene.store import *
from org.apache.lucene.util import *
from tqdm import tqdm


from .query import *
from .judgement import *
from .result import *
from .dataset import *
from .config import *

class Model:

    def get_name(self):
        return self.__class__.__name__

    
    def run(self, dataset: DataSet):


        #start = time.time()

        query_set = dataset.query_set

        analyzer = EnglishAnalyzer()

        self.parser = QueryParser(Config.content_field, analyzer)
        self.dataset = dataset
        self.collection = dataset.collection


        trec_run = ResultSet(dataset)

        q_num = len(query_set.queries_list)

        for k in tqdm(range(q_num)):
            query = query_set.queries_list[k]
            self.run_query(query, trec_run)

        #end = time.time()
        # print(end - start)

        return trec_run

    def run_query(self, query, trec_run):

        #query_vec = self.get_vec(query.to_string())

        C = self.collection.C
        N = self.collection.N
        ctn = self.collection.ctn
        qtf = 1

        self.doc_score_array = np.zeros(N, dtype=np.float64)
        term_list = query.get_terms(self.parser)

        for term in term_list:

            ctf = self.collection.ctf(term)
            df = self.collection.df(term)
            ql = len(term_list)

            for item in self.collection.tf_array(term):

                doc_id = item[0]
                tf = item[1]

                dl = self.collection.dl(doc_id)
                dtn = self.collection.dtn(doc_id)

                self.doc_score_array[doc_id] += self.score_term(tf, dtn, dl, ql, ctf, df, qtf, ctn, C, N)

                #print(doc_id, tf, self.doc_score_array[doc_id])

        score_tuple_array = []

        for idx in range(N):
            score = self.doc_score_array[idx]
            score_tuple_array.append((idx, score))

        def takeSecond(elem):
            return elem[1]

        result_num = min(1000, len(score_tuple_array))

        score_tuple_array.sort(key=takeSecond, reverse=True)

        qid = query.qid
        trec_run.entries[qid] = []

        for idx in range(result_num):
            docnum = score_tuple_array[idx][0]
            score = score_tuple_array[idx][1]
            docno = self.collection.docno(docnum)
            # doc_text = self.collection.doc(docnum)

            trec_run.entries[qid].append((docno, float(score), "TEST"))


    def score_term(self, tf: float, tn: float, dl: float, ctf: float,
                  df: float, qtf: float, ctn: float, C: float, N: float):
        pass

    def frange(start, stop, step):
        i = start
        while i < stop:
            yield i
            i += step