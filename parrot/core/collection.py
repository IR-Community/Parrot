
from pathlib import Path
import numpy as np
import pickle

from java.io import File
from org.apache.lucene.analysis.standard import *
from org.apache.lucene.document import *
from org.apache.lucene.search import *
from org.apache.lucene.index import *
from org.apache.lucene.queryparser.classic import *
from org.apache.lucene.store import *
from org.apache.lucene.util import *


from .judgement import *


class Collection:

    def C(self) ->int:
        return self.C

    def N(self) -> int:
        return self.N

    def ctn(self) -> int:
        return self.ctn

    def dl(self, doc_index: int) -> int:
        return self.dl_array[doc_index]

    def dtn(self, doc_index: int) -> int:
        return self.dtn_array[doc_index]

    def ctf(self, term: str) -> int:
        return self.reader.totalTermFreq(Term(Config.content_field, term))

    def df(self, term: str) -> int:
        return self.reader.docFreq(Term(Config.content_field, term))

    def docno(self, doc_index: int) -> str:
        return self.reader.document(doc_index).get(Config.docno_field)

    def doc(self, doc_index: int) -> str:
        return self.reader.document(doc_index).get("raw")

    def tf_array(self, term: str):
        term = Term(Config.content_field, BytesRef(term))
        leaves = self.reader.leaves()
        start = 0
        for leaf in leaves:
            leaf_reader = leaf.reader()
            posting = leaf_reader.postings(term)
            if posting is not None:
                doc_id = posting.nextDoc()
                while doc_id != PostingsEnum.NO_MORE_DOCS:
                    freq = posting.freq()
                    yield (start + doc_id, freq)
                    doc_id = posting.nextDoc()
            start += leaf_reader.getDocCount(Config.content_field)


    def __str__(self):
        col_str = "Collection:" + str(self.index_folder)
        col_str += "\ntotal_term_freq:" + str(self.C)
        col_str +=  "\nnum_docs:" + str(self.N)
        col_str += "\nnum_terms:" + str(self.ctn)
        return col_str

    @staticmethod
    def build(self, col, index_folder: str):
        index_path = File(index_folder).toPath()
        index_dir = FSDirectory.open(index_path)
        reader = DirectoryReader.open(index_dir)

        col.C = reader.getSumTotalTermFreq(Config.content_field)
        col.N = reader.numDocs()

        termsEnum = MultiFields.getTerms(reader, Config.content_field).iterator()

        col.ctn = 0
        for term in BytesRefIterator.cast_(termsEnum):
            col.ctn += 1

        col.dl_array = np.zeros(col.N, dtype=int)
        col.dtn_array = np.zeros(col.N, dtype=int)
        # self.docno_array = [0] * self.N

        for j in range(col.N):

            terms = reader.getTermVector(j, Config.content_field)

            if terms is None:
                continue

            terms_enum = terms.iterator()
            dtn = terms.size()

            dl = 0
            for item in BytesRefIterator.cast_(terms_enum):
                dl += terms_enum.totalTermFreq()

            col.dl_array[j] = dl
            col.dtn_array[j] = dtn

        with open(index_folder + '/collection.pickle', 'wb') as f:
            pickle.dump(col.C, f)
            pickle.dump(col.N, f)
            pickle.dump(col.ctn, f)
            pickle.dump(col.dl_array, f)
            pickle.dump(col.dtn_array, f)
            f.close()


    @staticmethod
    def load(index_folder: str):
        file_name = index_folder + '/collection.pickle'
        index_path = File(index_folder).toPath()
        index_dir = FSDirectory.open(index_path)
        reader = DirectoryReader.open(index_dir)
        
        col = Collection()
        col.index_folder = index_path
        file = Path(file_name)
        if file.is_file():
            with open(file_name, 'rb') as f:
                col.C = pickle.load(f)
                col.N = pickle.load(f)
                col.ctn = pickle.load(f)
                col.dl_array = pickle.load(f)
                col.dtn_array = pickle.load(f)
                col.reader = reader
        else:
            Collection.build(col, index_folder)
            col.reader = reader
        
        return col


"""
    def tf_array(self, term: str):
        posting = MultiFields.getTermDocsEnum(self.reader, 
            Config.content_field, BytesRef(term), PostingsEnum.FREQS)
        if posting is not None:
            docid = posting.nextDoc()
            while docid != PostingsEnum.NO_MORE_DOCS:
                freq = posting.freq()
                yield (docid, freq)
                docid = posting.nextDoc()
"""