import re
import os
import gzip
from tqdm import tqdm
from java.io import File

from org.apache.lucene.analysis.standard import *
from org.apache.lucene.analysis.en import *
from org.apache.lucene.document import *
from org.apache.lucene.search import *
from org.apache.lucene.index import *
from org.apache.lucene.queryparser.classic import *
from org.apache.lucene.store import *
from org.apache.lucene.util import *

from parrot.core import *

from .zfile import unlzw

def build_index(doc_folder, doc_patterns, index_folder):
    index_builder = IndexBuilder(doc_folder, doc_patterns, index_folder)
    index_builder.indexing()
    print("doc_num : ", index_builder.doc_num)


class IndexBuilder:

    def __init__(self, doc_folder, doc_patterns, index_folder):

        self.doc_folder = doc_folder
        self.index_folder = index_folder
        self.doc_patterns = doc_patterns
        self.doc_store = True
        self.writer = None
        self.doc_num = 0
        self.analyzer = EnglishAnalyzer()
        self.doc_list = []


    def indexing(self):

        index_path = File(self.index_folder).toPath()
        indexDir = SimpleFSDirectory(index_path)
        writerConfig = IndexWriterConfig(self.analyzer)
        writerConfig.setRAMBufferSizeMB(1024.0)

        self.writer = IndexWriter(indexDir, writerConfig)
        self.scan_folder(self.doc_folder)

        for k in tqdm(range(len(self.doc_list))):
            self.unzip_file(self.doc_list[k])

        self.writer.commit()
        self.writer.close()



    def unzip_file(self, name):
        # print(name)
        if name.endswith("Z"):
            with open(name, mode="rb") as file:
                text = (unlzw(file.read())).decode("iso-8859-1")
                self.index_file(text)
        elif name.endswith("gz"):
            with gzip.open(name, 'rb') as file:
                self.index_file(file.read().decode("iso-8859-1"))


    def index_file(self, text):
        pattern = re.compile("<DOC>([\u0000-\uffff]*?)</DOC>")
        result = pattern.findall(text)

        for doc in result:
            pattern = re.compile("<DOCNO>([\u0000-\uffff]*?)</DOCNO>")
            docnos = pattern.findall(doc)
            docno = docnos[0].strip()
            content = remove_html_tags(doc)

            doc = Document()
            doc.add(StoredField(Config.docno_field, docno))

            fieldType = FieldType(TextField.TYPE_STORED)
            fieldType.setIndexOptions(
                IndexOptions.DOCS_AND_FREQS_AND_POSITIONS_AND_OFFSETS)
            fieldType.setTokenized(True)

            if self.doc_store is True:
                fieldType.setStoreTermVectors(True)
                fieldType.setStored(True)
            else:
                fieldType.setStoreTermVectors(False)
                fieldType.setStored(False)

            doc.add(Field(Config.content_field, content, fieldType))
            self.writer.addDocument(doc)
            self.doc_num += 1

    def scan_folder(self, doc_folder):
        # print(doc_folder)
        g = os.walk(doc_folder)
        for path, dir_list, file_list in g:
            for folder in dir_list:
                self.scan_folder(folder)
            for name in file_list:
                for pattern in self.doc_patterns:
                    if re.match(pattern, name):
                        full_name = os.path.join(path, name)
                        self.doc_list.append(full_name)





def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

"""
def merge_index(config):
    lucene.initVM()

    base_folder = index_folder
    sub_index_folder = base_folder + "/index_sub/"
    merged_index_folder = base_folder + "/index/"

    index_path = File(merged_index_folder).toPath()
    indexDir = SimpleFSDirectory(index_path)
    writerConfig = IndexWriterConfig(Config.analyzer)
    writerConfig.setRAMBufferSizeMB(4000.0)
    writer = IndexWriter(indexDir, writerConfig)

    g = os.walk(sub_index_folder)
    for path, dir_list, file_list in g:
        for name in dir_list:
            index_path = File(sub_index_folder + name).toPath()
            indexDir = SimpleFSDirectory(index_path)
            writer.addIndexes(indexDir)

    writer.commit()
    writer.close()

    indexPath = File(merged_index_folder).toPath()
    indexDir = FSDirectory.open(indexPath)
    reader = DirectoryReader.open(indexDir)
    reader.close()


def build_sub_index(param):
    lucene.initVM()
    worker = IndexBuilder(param)
    doc_num = worker.indexing()
    return doc_num
"""

