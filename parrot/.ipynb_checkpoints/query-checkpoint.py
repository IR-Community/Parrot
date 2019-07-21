
import os
import re
import os
import time
import gzip

import lucene
from .config import *
from java.io import File
from org.apache.lucene.analysis.standard import *
from org.apache.lucene.document import *
from org.apache.lucene.search import *
from org.apache.lucene.index import *
from org.apache.lucene.queryparser.classic import *
from org.apache.lucene.store import *
from org.apache.lucene.util import *

class Query:
    def __init__(self, qid: int, querystr: str):
        self.qid = qid
        self.querystr = querystr

    def __str__(self):
        return str(self.qid) + ":" + self.querystr

    def get_terms(self, parser: QueryParser):
        qstr = self.querystr
        qstr = qstr.replace("/", " ")
        qstr = qstr.replace("?", " ")

        query = parser.parse(qstr)
        qstr = query.toString()
        qstr = qstr.replace(Config.content_field + ":", " ")
        terms = qstr.split()
        return terms

    def to_string(self) -> str:
        return self.querystr


class QuerySet:
    def __init__(self):
        self.queries = []


    def size(self):
        return len(self.queries)

    @staticmethod
    def load(folder):
        qset = QuerySet()

        # self.config.query_folder = topics_folder
        # topic_writer = open(topic_file, "wt")
        g = os.walk(folder)
        for path, dir_list, file_list in g:
            for name in file_list:
                full_name = os.path.join(path, name)
                # print(full_name)
                if name.startswith("topic"):
                    with open(full_name, 'rb') as file:
                        QuerySet.extract_query(qset, file.read().decode("utf-8"))
        return qset
    
    @staticmethod
    def extract_query(qset, doc):
        pattern = re.compile("<top>[\u0000-\uffff]*?</top>")
        result = pattern.findall(doc)
        for doc in result:
            pattern = re.compile("<num>.*?([0-9]+)")
            num = pattern.findall(doc)
            qid = int(num[0])
            pattern = re.compile("<title>(.*)")
            titles = pattern.findall(doc)
            title = titles[0].replace("Topic:", "")
            qset.queries.append(Query(qid, title))





