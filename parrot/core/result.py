import math
from org.apache.lucene.analysis import *
from org.apache.lucene.document import *
from org.apache.lucene.index import *
from org.apache.lucene.queryparser.classic import *
from org.apache.lucene.search.highlight import *
from org.apache.lucene.search import *
from org.apache.lucene.store import *
from org.apache.lucene.analysis.en import *
from org.apache.lucene.analysis.core import *
from .config import *

from IPython.core.display import display, HTML


class ResultSet:


    def __init__(self, dataset):
        self.entries = {}
        self.name = None
        self.dataset = dataset
        self.judgement_set = dataset.judgement_set
        self.query_set = dataset.query_set


    def _extract_runname(self, file_name):
        if file_name.endswith('.trecrun'):
            return file_name[file_name.rfind('/') + 1: file_name.rfind('.')]
        else:
            return file_name

    def _parse_file(self, source):
        self.entries = {}
        f = open(source, 'r', encoding='utf-8')
        for line in f:
            line = line.strip()
            if line == "": continue
            splitLine = line.split('\t')
            if len(splitLine) == 6:
                topic_id, Q0, docId, rank, score, annotation = splitLine
            elif len(splitLine) == 5:
                topic_id, Q0, docId, rank, score = splitLine
                annotation = ''
            else:
                raise BaseException('Unparsable run')
            score = float(score)
            if topic_id not in self.entries: self.entries[topic_id] = []
            self.entries[topic_id].append((docId, score, annotation))
        f.close()

    def restrict_topics_to(self, qrels):

        good_topics = set(qrels.get_topic_ids())
        bad_topics = [run_topic for run_topic in self.get_topic_ids() if run_topic not in good_topics]
        for t in bad_topics:
            self.remove_entries(t)

    def get_entries_by(self, topic_id):
        return [] if topic_id not in self.entries else self.entries[topic_id]

    def get_score(self, topic_id, doc_id):
        scores = [score for did, score in self.entries[topic_id] if did == doc_id]
        if scores == []: raise KeyError('Invalid docId for topic "' + topic_id + '"')
        return scores[0]

    def get_topic_ids(self):
        return self.entries.keys()

    def remove_entries(self, topic_id):
        self.entries.pop(topic_id, '')

    def write(self, file_name):

        with open(file_name, "wt") as file:
            for topic_id, entry_list in self.entries.items():
                for (rank, (docId, score, annotation)) in enumerate(entry_list, start=1):
                    file.write('{}\tQ0\t{}\t{}\t{}\t{}\n'.format(topic_id, docId, rank, score, annotation))

            file.close()

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'TrecRun ' + self.name


    def load(self, source, name=''):

        if type(source) == str:
            self._parse_file(source)
            self.name = name if name != '' else self._extract_runname(source)
        elif type(source) == dict:
            self.entries = source
            self.name = name
        else:
            raise RuntimeError("Wrong parameter for TrecRun's constructor. Accepted str and dict, given", type(source))

        for topicId, entryList in self.entries.items():
            entryList.sort(key=lambda x: x[1], reverse=True)



    def precision(self, detailed=False):

        qrels = self.judgement_set

        details = {}
        avg = 0
        for topic_id in qrels.judgements:
            if topic_id in self.entries:
                entry_list = self.entries[topic_id]
                num_relevant = len([doc_id for doc_id, score, _ in entry_list
                                   if qrels.is_relevant(topic_id, doc_id)])
                num_returned = len(entry_list)
                details[topic_id] = num_relevant / num_returned
                avg += num_relevant / num_returned
            else:
                details[topic_id] = 0
                avg += 0
        num_topics = self.judgement_set.get_n_topics()

        return avg / num_topics if not detailed else (avg / num_topics, details)


    def recall(self, detailed=False):
        qrels = self.judgement_set
        details = {}
        avg = 0
        n_topics_w_relevant = 0
        for topic_id in qrels.judgements:
            num_relevant = qrels.get_n_relevant(topic_id)
            if topic_id in self.entries:
                entry_list = self.entries[topic_id]
                num_relevant_found = len([doc_id for doc_id, score, _ in entry_list
                                        if qrels.is_relevant(topic_id, doc_id)])
                if num_relevant > 0:
                    details[topic_id] = num_relevant_found / num_relevant
                    avg += num_relevant_found / num_relevant
                    n_topics_w_relevant += 1
                    # ignore queries without relevant docs is 1
            else:
                details[topic_id] = 0
                avg += 0
                if num_relevant > 0: n_topics_w_relevant += 1
        num_topics = qrels.get_n_topics()

        return avg / n_topics_w_relevant if not detailed else (avg / n_topics_w_relevant, details)


    def avg_prec(self, detailed=False):
        qrels = self.judgement_set
        details = {}
        avg = 0
        no_relevent = 0
        for topic_id, entry_list in self.entries.items():
            sum_prec = num_rel = 0
            for (rank, (docId, score, _)) in enumerate(entry_list, start=1):
                if qrels.is_relevant(topic_id, docId):
                    num_rel += 1
                    sum_prec += num_rel / rank
            tot_relevant = qrels.get_n_relevant(topic_id)
            if tot_relevant == 0:
                # print("relevent:0, topic id:", topicId)
                no_relevent += 1
            ap = sum_prec / tot_relevant if tot_relevant > 0 else 0

            avg += ap
            details[topic_id] = ap

        num_topics = qrels.get_n_topics()

        # print(numtopics)

        return avg / num_topics if not detailed else (avg / num_topics, details)


    def precision_at(self, rank, detailed=False):


        qrels = self.judgement_set
        details = {}
        avg = 0
        for topic_id, entry_list in self.entries.items():
            num_relevant = len([docId for docId, score, _ in entry_list[0: rank]
                               if qrels.is_relevant(topic_id, docId)])
            details[topic_id] = num_relevant / rank
            avg += num_relevant / rank
        num_topics = qrels.get_n_topics()

        return avg / num_topics if not detailed else (avg / num_topics, details)

    def ndcg(self, detailed=False):

        qrels = self.judgement_set

        details = {}
        avg = 0
        no_relevent = 0
        for topic_id, entry_list in self.entries.items():
            relevances_by_rank = qrels.get_relevance_scores(topic_id, [doc for (doc, _, _) in entry_list])

            sum_dcg = relevances_by_rank[0] + sum([relScore / math.log2(rank)
                                                   for rank, relScore in enumerate(relevances_by_rank[1:], start=2)])
            # sumdcg = sum( [ (2**relScore - 1) / math.log2(rank+1)
            #                for rank, relScore in enumerate(relevancesByRank, start=1)] )
            relevances_by_rank.sort(reverse=True)  # sort the relevance list descending order
            sumIdcg = relevances_by_rank[0] + sum([relScore / math.log2(rank)
                                                   for rank, relScore in enumerate(relevances_by_rank[1:], start=2)])
            # sumIdcg = sum( [ (2**relScore - 1) / math.log2(rank+1)
            #                   for rank, relScore in enumerate(relevancesByRank, start=1)] )
            if sumIdcg == 0:
                details[topic_id] = 0
            else:
                details[topic_id] = sum_dcg / sumIdcg
                avg += sum_dcg / sumIdcg

            tot_relevant = qrels.get_n_relevant(topic_id)
            if tot_relevant == 0:
                # print("relevent:0, topic id:", topicId)
                no_relevent += 1

        num_topics = qrels.get_n_topics()

        return avg / num_topics if not detailed else (avg / num_topics, details)

    def show_detail(self):
        detail = self.avg_prec(True)
        output = "Avg Prec: "
        output += str(detail[0])
        output += "<table>"
        output += "<tr><td>QueryId</td><td>Title</td><td>MAP</td></tr>"

        for i, v in detail[1].items():
            pat = "<tr><td>{:d}</td><td>{:s}</td><td style='background:rgba(76, 175, 80, {:f})'>{:f}</td></tr>"
            output += pat.format(i, self.query_set.queries[i].querystr, v, v)

        output += "</table>"
        display(HTML(output))


    def show_results(self, topic_id, start, limit):
        qid = topic_id
        output = "Query:"
        output += self.query_set.queries[qid].to_string()
        output += "<table>"
        output += "<tr ><td>Rank</td><td>DocId</td><td>Score</td><td>IsRel</td></tr>"

        for i in range(start, start + limit):
            rel = self.dataset.judgement_set.is_relevant(qid, self.entries[qid][i][0])
            if rel == 1:
                bcolor = "style='background-color: rgba(76, 175, 80, 1)'"
            else:
                bcolor = ""
            pat = "<tr><td>{:d}</td><td> {:s}</td><td> {:f} </td><td {:s} >{:b}</td></tr>"
            output += pat.format(i, self.entries[qid][i][0], self.entries[qid][i][1], bcolor, rel)
        output += "</table>"
        display(HTML(output))

    def ireplace(self, text, old_str, new_str):
        import re
        redata = re.compile(re.escape(old_str), re.IGNORECASE)
        new_text = redata.sub(new_str, text)
        return new_text

    def show_doc(self, topic_id, rank_index):
        qid = topic_id

        docid = self.entries[qid][rank_index][0]
        score = self.entries[qid][rank_index][1]

        reader = self.dataset.collection.reader
        searcher = IndexSearcher(reader)

        query = QueryParser("id", WhitespaceAnalyzer()).parse(docid)
        topDocs = searcher.search(query, 1)
        text = self.dataset.collection.doc(topDocs.scoreDocs[0].doc)

        qp = QueryParser(Config.content_field, EnglishAnalyzer())

        colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#FF0000"]

        terms = self.dataset.query_set.queries[qid].get_terms(qp)

        output = "Query:"

        index = 0
        for term in terms:
            output += "&nbsp;<span style='color:white;background:" + \
                colors[min(len(colors) - 1, index)] + "'>" + term + "</span>&nbsp;"
            index += 1

        output += '<br><br>'

        output += "Score:" + str(score) + "<br><br>"

        index = 0
        text = text.replace("\n", "<br>")
        for term in terms:
            text = self.ireplace(text, term,
                "&nbsp;<span style='color:white;background:" + colors[
                min(len(colors) - 1, index)] + "'>" + term + "</span>&nbsp;")
            index += 1

        output += text

        display(HTML(output))