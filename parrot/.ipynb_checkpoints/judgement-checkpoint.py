
import re
import os
import time
import gzip
import json
import random
import sys
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
    
    allJudgements = None

    def __init__(self):
        self.allJudgements = {}

    
    def getDocIds(self):
        return sorted([docId for _, docsRelevance in self.allJudgements.items() for docId in docsRelevance])

    def getNRelevant(self, topicId):
        if topicId not in self.allJudgements: return 0
        return len([t for t, relevance in self.allJudgements[topicId].items() if relevance >= 1])

    def isRelevant(self, topicId, docId):
        try:
            return self.allJudgements[topicId][docId] >= 1
        except KeyError:
            return False

    def getAllRelevants(self, topicId: int):
        return {docId for docId, score in self.allJudgements[topicId].items()
                if score >= 1}

    def getRelevanceScore(self, topicId: int, docId):
        try:
            return self.allJudgements[topicId][docId]
        except KeyError:
            return None

    def getRelevanceScores(self, topicId: int, docIds, nonJudged=0):

        try:
            return [nonJudged if not ( topicId in self.allJudgements and docId in self.allJudgements[topicId])
                    else self.allJudgements[topicId][docId]
                    for docId in docIds]
        except KeyError:
            return []

    def getTopicIds(self):
        return self.allJudgements.keys()

    def getNTopics(self):
        return len(self.allJudgements)

    def write(self, streamOut):
        for topicId, dictDocs in self.allJudgements.items():
            for docId, relevanceScore in dictDocs.items():
                streamOut.write('{}\t0\t{}\t{}\n'.format(topicId, docId, relevanceScore))

                
    @staticmethod
    def load(folder: str, index_folder: str = None):
        
        judgement_set = JudgementSet()
        docno_set = None

        if(index_folder is not None):
            docno_set = set([])
            indexPath = File(index_folder).toPath()
            indexDir = FSDirectory.open(indexPath)
            reader = DirectoryReader.open(indexDir)
            for k in range(reader.numDocs()):
                docno_set.add(reader.document(k).get(Config.docno_field))

        g = os.walk(folder)
        for path, dir_list, file_list in g:
            for name in file_list:
                full_name = os.path.join(path, name)
                if name.startswith("qrels"):
                    with open(full_name, 'r', encoding='utf-8') as file:
                        JudgementSet.extract_judgement(judgement_set, docno_set, file)
        
        #print("JudgementSet", ":", folder)
        #for item in judgement_set.allJudgements:
            #print(item, judgement_set.getNRelevant(item))
            
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

            topicId, docId, relevanceScore = split[0], split[2], float(split[3])

            topicId = int(topicId)

            if docno_set is not None:
                if docId not in docno_set:
                    continue

            if topicId not in judgement_set.allJudgements:
                judgement_set.allJudgements[topicId] = {}
            judgement_set.allJudgements[topicId][docId] = relevanceScore
                



