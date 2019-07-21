import re
import os
import time
import gzip
import json
import random
import sys
from pathlib import Path

from multiprocessing import *
from .zfile import unlzw
from datetime import datetime
from typing import List
import numpy as np
import pickle

import lucene
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
from .judgement import JudgementSet
from .collection import *

class DataSet:
    
    @staticmethod
    def load(index_folder: str,  
            topics_folder: str, 
            qrels_folder: str,
            check_docno: str = False):
        
        dataset = DataSet()
        
        dataset.index_folder = index_folder
        dataset.qrels_folder = qrels_folder
        dataset.topics_folder = topics_folder

        dataset.query_set = QuerySet.load(topics_folder)

        if check_docno is True:
            dataset.judgement_set = JudgementSet.load(qrels_folder, index_folder)
        else:
            dataset.judgement_set = JudgementSet.load(qrels_folder)

        dataset.collection = Collection.load(index_folder)

        index_path = File(index_folder).toPath()
        index_dir = FSDirectory.open(index_path)
        dataset.reader = DirectoryReader.open(index_dir)
        
        return dataset















