
from java.io import File
from org.apache.lucene.analysis.standard import *
from org.apache.lucene.document import *
from org.apache.lucene.search import *
from org.apache.lucene.index import *
from org.apache.lucene.queryparser.classic import *
from org.apache.lucene.store import *
from org.apache.lucene.util import *

from .config import *
from .query import *
from .judgement import *
from .collection import *

class DataSet:
    
    @staticmethod
    def load(index_folder: str,
             queries_folder: str,
             judgements_folder: str,
             check_docno: str = False):
        
        dataset = DataSet()
        
        dataset.index_folder = index_folder
        dataset.judgements_folder = judgements_folder
        dataset.topics_folder = queries_folder

        dataset.query_set = QuerySet.load(queries_folder)

        if check_docno is True:
            dataset.judgement_set = JudgementSet.load(judgements_folder, index_folder)
        else:
            dataset.judgement_set = JudgementSet.load(judgements_folder)

        dataset.collection = Collection.load(index_folder)

        index_path = File(index_folder).toPath()
        index_dir = FSDirectory.open(index_path)
        dataset.reader = DirectoryReader.open(index_dir)
        
        return dataset















