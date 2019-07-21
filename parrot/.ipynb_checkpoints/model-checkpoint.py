import lucene

from .query import *
from .judgement import *
from .trecrun import *
from .dataset import *
from .config import *

import numpy as np
import math

from org.apache.lucene.search.similarities import *


from bert_serving.client import BertClient
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


from java.io import File
from org.apache.lucene.analysis.en import *
from org.apache.lucene.analysis.standard import *
from org.apache.lucene.document import *
from org.apache.lucene.search import *
from org.apache.lucene.index import *
from org.apache.lucene.queryparser.classic import *
from org.apache.lucene.store import *
from org.apache.lucene.util import *



class Model:
    #output = None
    #bc = BertClient(check_length=False)

    #filename = './pytrec/ap90_vec_uncased_L-24_H-1024_A-16'
    #input1 = open(filename, 'rb')
    #vec_list = pickle.load(input1)

    #print(len(vec_list))
    


    #def get_vec(self, term: str):
    #    vec = self.bc.encode([term])
    #    vec0 = np.array([vec[0]])
    #    return vec0

    #def get_vec_list(self, doc_list):
    #    vec_list = self.bc.encode(doc_list)
    #    vec_list = np.array(vec_list)
    #    return vec_list

    #def sim(self, vec0, vec1):
    #    return cosine_similarity(vec0, vec1)


    
    def run(self, dataset: DataSet):
        
        #print("testtest")
        
        #self.outfile = open("disk45-result",'wb')
        #self.match_list = []

        #print("beta", self.beta)

        start = time.time()

        query_set = dataset.query_set

        judgement_set = dataset.judgement_set
        analyzer = EnglishAnalyzer()

        self.parser = QueryParser(Config.content_field, analyzer)
        self.dataset = dataset
        self.collection = dataset.collection

        #self.doc_vec = []

        #for idx in range(self.collection.N):
        #    doc_vec = self.get_vec(self.collection.doc(idx))
        #    self.doc_vec.append(doc_vec)
        #    print(idx)

        trec_run = TrecRun(judgement_set, query_set)

        for query in query_set.queries:
            #print("run query", query)
            self.run_query(query, trec_run)
            
        #pickle.dump(self.match_list, self.outfile)
        #self.outfile.close()

        end = time.time()
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

                docid = item[0]
                tf = item[1]

                # print(term, docid, tf)

                dl = self.collection.dl(docid)
                dtn = self.collection.dtn(docid)

                self.doc_score_array[docid] += self.scoreTerm(tf, dtn, dl, ql, ctf, df, qtf, ctn, C, N)


        score_tuple_array = []

        for idx in range(N):
            score = self.doc_score_array[idx]
            #if score != 0:
                #doc_vec = self.vec_list[idx]
                #sim_score = self.sim(doc_vec, query_vec)

                #final_score = self.beta * score / (1 + score) \
                #             + (1 - self.beta) * sim_score / (1 + sim_score)
                
            score_tuple_array.append((idx, score))

        def takeSecond(elem):
            return elem[1]

        result_num = min(1000, len(score_tuple_array))

        score_tuple_array.sort(key=takeSecond, reverse=True)

        qid = query.qid
        trec_run.entries[qid] = []

        # print("trec_run")

        for idx in range(result_num):
            docnum = score_tuple_array[idx][0]
            score = score_tuple_array[idx][1]
            docno = self.collection.docno(docnum)
            doc_text = self.collection.doc(docnum)

            #print(qid, docno, idx, score)
            
            #print([query.querystr, len(doc_text), "k a b", 0])
            
            #self.match_list.append([query.querystr, doc_text,
            #                        "a b c", 0, qid, docno, score])

            trec_run.entries[qid].append((docno, float(score), "TEST"))

            #self.output.write("%s\tQ0\t%s\t%s\t%s\tTEST\n" % (query.qid, docno, idx, score) )

    def scoreTerm(self, tf: float, tn: float, dl: float, ctf: float,
                  df: float, qtf: float, ctn: float, C: float, N: float):
        pass

    def frange(start, stop, step):
        i = start
        while i < stop:
            yield i
            i += step