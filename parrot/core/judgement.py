
import os
from java.io import File
from org.apache.lucene.analysis.standard import *
from org.apache.lucene.document import *
from org.apache.lucene.search import *
from org.apache.lucene.index import *
from org.apache.lucene.queryparser.classic import *
from org.apache.lucene.store import *
from org.apache.lucene.util import *

from .config import *


class JudgementSet:
    
    judgements = None

    def __init__(self):
        self.judgements = {}

    
    def get_doc_ids(self):
        return sorted([doc_id for _, docs_relevance in self.judgements.items() for doc_id in docs_relevance])

    def get_n_relevant(self, topic_id: int):
        if topic_id not in self.judgements: return 0
        return len([t for t, relevance in self.judgements[topic_id].items() if relevance >= 1])

    def is_relevant(self, topic_id, doc_id):
        try:
            return self.judgements[topic_id][doc_id] >= 1
        except KeyError:
            return False

    def get_all_relevants(self, topic_id: int):
        return {doc_id for doc_id, score in self.judgements[topic_id].items()
                if score >= 1}

    def get_relevance_score(self, topic_id: int, doc_id):
        try:
            return self.judgements[topic_id][doc_id]
        except KeyError:
            return None

    def get_relevance_scores(self, topic_id: int, doc_ids, non_judged=0):

        try:
            return [non_judged if not (topic_id in self.judgements and doc_id in self.judgements[topic_id])
                    else self.judgements[topic_id][doc_id]
                    for doc_id in doc_ids]
        except KeyError:
            return []

    def get_topic_ids(self):
        return self.judgements.keys()

    def get_n_topics(self):
        return len(self.judgements)

    def write(self, stream_out):
        for topic_id, dict_docs in self.judgements.items():
            for doc_id, relevance_score in dict_docs.items():
                stream_out.write('{}\t0\t{}\t{}\n'.format(topic_id, doc_id, relevance_score))

                
    @staticmethod
    def load(folder: str, index_folder: str = None):
        
        judgement_set = JudgementSet()
        docno_set = None

        if(index_folder is not None):
            docno_set = set([])
            index_path = File(index_folder).toPath()
            index_dir = FSDirectory.open(index_path)
            reader = DirectoryReader.open(index_dir)
            for k in range(reader.numDocs()):
                docno_set.add(reader.document(k).get(Config.docno_field))

        g = os.walk(folder)
        for path, dir_list, file_list in g:
            for name in file_list:
                full_name = os.path.join(path, name)
                if name.startswith("qrels"):
                    with open(full_name, 'r', encoding='utf-8') as file:
                        JudgementSet.extract_judgement(judgement_set, docno_set, file)
            
        return judgement_set

    @staticmethod
    def extract_judgement(judgement_set, docno_set, file):

        for line in file:
            line = line.strip()
            if line == '':
                continue
            split = line.split(' ')
            if len(split) < 4:
                continue

            topic_id, doc_id, relevance_score = split[0], split[2], float(split[3])

            topic_id = int(topic_id)

            if docno_set is not None:
                if doc_id not in docno_set:
                    continue

            if topic_id not in judgement_set.judgements:
                judgement_set.judgements[topic_id] = {}
            judgement_set.judgements[topic_id][doc_id] = relevance_score
                



