from java.io import File
from org.apache.lucene.analysis.en import *
from org.apache.lucene.analysis.standard import *
from org.apache.lucene.document import *
from org.apache.lucene.search import *
from org.apache.lucene.index import *
from org.apache.lucene.queryparser.classic import *
from org.apache.lucene.store import *
from org.apache.lucene.util import *


from parrot.core import *


class LuceneModel:

    def __init__(self, similarity):
        self.similarity = similarity

    def run(self, dataset):
        start = time.time()

        self.config = Config()

        query_set = dataset.query_set

        judgement_set = dataset.judgement_set
        self.parser = QueryParser(Config.content_field, EnglishAnalyzer())
        self.dataset = dataset

        trec_run = TrecRun(judgement_set, query_set)

        index_path = File(dataset.index_folder).toPath()
        directory = SimpleFSDirectory(index_path)
        reader = DirectoryReader.open(directory)
        searcher = IndexSearcher(reader)
        searcher.setSimilarity(self.similarity)


        for query in query_set.queries:
            # print(query.to_string())
            self.run_query(self.parser, searcher, query, trec_run)

        end = time.time()
        print(end - start)

        return trec_run

    def run_query(self, qp, searcher, query, trec_run):
        qstr = query.querystr
        qstr = qstr.replace("/", " ")
        qstr = qstr.replace("?", " ")

        luecne_query = qp.parse(qstr)
        hits = searcher.search(luecne_query, 1000).scoreDocs

        idx = 0
        qid = query.qid
        trec_run.entries[qid] = []

        for hit in hits:
            doc = searcher.doc(hit.doc)
            docno = doc.get(Config.docno_field)
            score = hit.score
            idx += 1

            trec_run.entries[qid].append((docno, float(score), "TEST"))

