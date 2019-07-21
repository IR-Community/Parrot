import sys
import math



class TrecRun:

    # Collects the entries of the run:
    # runEntries[topicID] = [ (docID, score, annotation) ] sorted by score
    #entries = None
    #name = None

    def __init__(self, qrels, query_set):
        self.entries = {}
        self.name = None
        self.qrels = qrels
        self.query_set = query_set


    def _extract_runname(self, filename):
        if filename.endswith('.trecrun'):
            return filename[filename.rfind('/') + 1: filename.rfind('.')]
        else:
            return filename

    def _parseFile(self, source):
        self.entries = {}
        f = open(source, 'r', encoding='utf-8')
        for line in f:
            line = line.strip()
            if line == "": continue
            splitLine = line.split('\t')
            if len(splitLine) == 6:
                topicId, Q0, docId, rank, score, annotation = splitLine
            elif len(splitLine) == 5:
                topicId, Q0, docId, rank, score = splitLine
                annotation = ''
            else:
                raise BaseException('Unparsable run')
            score = float(score)
            if topicId not in self.entries: self.entries[topicId] = []
            self.entries[topicId].append((docId, score, annotation))
        f.close()

    def restrictTopicsTo(self, qrels):

        good_topics = set(qrels.get_topic_ids())
        bad_topics = [run_topic for run_topic in self.getTopicIds() if run_topic not in good_topics]
        for t in bad_topics:
            self.removeEntries(t)

    def getEntriesBy(self, topicId):
        return [] if topicId not in self.entries else self.entries[topicId]

    def getScore(self, topicId, docId):
        scores = [score for did, score in self.entries[topicId] if did == docId]
        if scores == []: raise KeyError('Invalid docId for topic "' + topicId + '"')
        return scores[0]

    def getTopicIds(self):
        return self.entries.keys()

    def removeEntries(self, topicId):
        self.entries.pop(topicId, '')

    def write(self, file_name):

        with open(file_name, "wt") as file:
            for topicId, entryList in self.entries.items():
                for (rank, (docId, score, annotation)) in enumerate(entryList, start=1):
                    file.write('{}\tQ0\t{}\t{}\t{}\t{}\n'.format(topicId, docId, rank, score, annotation))

            file.close()

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'TrecRun ' + self.name


    def load(self, source, name=''):

        if type(source) == str:
            self._parseFile(source)
            self.name = name if name != '' else self._extract_runname(source)
        elif type(source) == dict:
            self.entries = source
            self.name = name
        else:
            raise RuntimeError("Wrong parameter for TrecRun's constructor. Accepted str and dict, given", type(source))

        for topicId, entryList in self.entries.items():
            entryList.sort(key=lambda x: x[1], reverse=True)



    def precision(self, detailed=False):

        qrels = self.qrels

        details = {}
        avg = 0
        for topicId in qrels.allJudgements:
            if topicId in self.entries:
                entryList = self.entries[topicId]
                numRelevant = len([docId for docId, score, _ in entryList
                                   if qrels.is_relevant(topicId, docId)])
                numReturned = len(entryList)
                details[topicId] = numRelevant / numReturned
                avg += numRelevant / numReturned
            else:
                details[topicId] = 0
                avg += 0
        numTopics = self.qrels.get_n_topics()

        return avg / numTopics if not detailed else (avg / numTopics, details)


    def recall(self, detailed=False):
        qrels = self.qrels
        details = {}
        avg = 0
        nTopicsWRelevant = 0
        for topicId in qrels.allJudgements:
            numRelevant = qrels.get_n_relevant(topicId)
            if topicId in self.entries:
                entryList = self.entries[topicId]
                numRelevantFound = len([docId for docId, score, _ in entryList
                                        if qrels.is_relevant(topicId, docId)])
                if numRelevant > 0:
                    details[topicId] = numRelevantFound / numRelevant
                    avg += numRelevantFound / numRelevant
                    nTopicsWRelevant += 1
                    # ignore queries without relevant docs is 1
            else:
                details[topicId] = 0
                avg += 0
                if numRelevant > 0: nTopicsWRelevant += 1
        numtopics = qrels.get_n_topics()

        return avg / nTopicsWRelevant if not detailed else (avg / nTopicsWRelevant, details)


    def avgPrec(self, detailed=False):
        qrels = self.qrels
        details = {}
        avg = 0
        no_relevent = 0
        for topicId, entryList in self.entries.items():
            sumPrec = numRel = 0
            for (rank, (docId, score, _)) in enumerate(entryList, start=1):
                if qrels.is_relevant(topicId, docId):
                    numRel += 1
                    sumPrec += numRel / rank
            totRelevant = qrels.get_n_relevant(topicId)
            if totRelevant == 0:
                # print("relevent:0, topic id:", topicId)
                no_relevent += 1
            ap = sumPrec / totRelevant if totRelevant > 0 else 0

            avg += ap
            details[topicId] = ap

        numtopics = qrels.get_n_topics()

        # print(numtopics)

        return avg / numtopics if not detailed else (avg / numtopics, details)


    def precisionAt(self, rank,  detailed=False):


        qrels = self.qrels
        details = {}
        avg = 0
        for topicId, entryList in self.entries.items():
            numRelevant = len([docId for docId, score, _ in entryList[0: rank]
                               if qrels.is_relevant(topicId, docId)])
            details[topicId] = numRelevant / rank
            avg += numRelevant / rank
        numtopics = qrels.get_n_topics()

        return avg / numtopics if not detailed else (avg / numtopics, details)

    def ndcg(self, detailed=False):

        qrels = self.qrels

        details = {}
        avg = 0
        no_relevent = 0
        for topicId, entryList in self.entries.items():
            relevancesByRank = qrels.get_relevance_scores(topicId, [doc for (doc, _, _) in entryList])

            sumdcg = relevancesByRank[0] + sum([relScore / math.log2(rank)
                                                for rank, relScore in enumerate(relevancesByRank[1:], start=2)])
            # sumdcg = sum( [ (2**relScore - 1) / math.log2(rank+1)
            #                for rank, relScore in enumerate(relevancesByRank, start=1)] )
            relevancesByRank.sort(reverse=True)  # sort the relevance list descending order
            sumIdcg = relevancesByRank[0] + sum([relScore / math.log2(rank)
                                                 for rank, relScore in enumerate(relevancesByRank[1:], start=2)])
            # sumIdcg = sum( [ (2**relScore - 1) / math.log2(rank+1)
            #                   for rank, relScore in enumerate(relevancesByRank, start=1)] )
            if sumIdcg == 0:
                details[topicId] = 0
            else:
                details[topicId] = sumdcg / sumIdcg
                avg += sumdcg / sumIdcg

            totRelevant = qrels.get_n_relevant(topicId)
            if totRelevant == 0:
                # print("relevent:0, topic id:", topicId)
                no_relevent += 1

        numtopics = qrels.get_n_topics()

        return avg / numtopics if not detailed else (avg / numtopics, details)


