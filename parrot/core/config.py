
from multiprocessing import *
import lucene
from org.apache.lucene.analysis.en import *


def get_process_pool():
    return process_pool


class Config:
    content_field = "contents"
    docno_field = "id"
    analyzer_name = "EnglishAnalyzer"

    def __init__(self):
        self.task_folder = ""
        self.doc_folder = ""
        self.doc_store = True
        self.doc_patterns = ""
        self.judgement_folder = ""
        self.query_folder = ""
        self.query_start = 0
        self.query_end = 0

    def get_analyzer(self):
        return eval(self.analyzer)

    WT_DOC_PATTERNS = ["B[0-9]{2}\.gz"]

    GOV2_DOC_PATTERNS = ["[0-9]{2}\.gz"]

    DISK45_DOC_PATTERNS = [
        "FR[0-9]{6}\.[0-9]Z",
        "FT[0-9]{3}.[0-9]+\.Z",
        "FB[0-9]{6}\.Z",
        "LA[0-9]{6}\.Z"
    ]

    DISK12_DOC_PATTERNS = [
        "AP89[0-9]{4}\.Z",
        "DOE[0-9]_[0-9]{3}\.Z",
        "FR89[0-9]{4}\.Z",
        "WSJ[0-9]_[0-9]{3}\.Z",
        "ZF_[0-9]{3}\.Z",
        "AP88[0-9]{4}\.gz",
        "FR88[0-9]{4}\.gz",
        "WSJ_[0-9]{4}\.gz",
        "ZF_[0-9]{3}\.gz"
    ]