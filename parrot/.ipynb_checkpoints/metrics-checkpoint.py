import math



def precision(run, qrels, detailed=False):
    details = {}
    avg = 0
    for topicId in qrels.allJudgements:
        if topicId in run.entries:
            entryList = run.entries[topicId]
            numRelevant = len([docId for docId, score, _ in entryList
                               if qrels.is_relevant(topicId, docId)])
            numReturned = len(entryList)

            details[topicId] = numRelevant / numReturned
            avg += numRelevant / numReturned
        else:
            details[topicId] = 0
            avg += 0
    numTopics = qrels.get_n_topics()
    return avg / numTopics if not detailed else (avg / numTopics, details)


def recall(run, qrels, detailed=False):
    details = {}
    avg = 0
    nTopicsWRelevant = 0
    for topicId in qrels.allJudgements:
        numRelevant = qrels.get_n_relevant(topicId)
        if topicId in run.entries:
            entryList = run.entries[topicId]
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


def avgPrec(run, qrels, detailed=False):
    """Computes average precision."""
    details = {}
    avg = 0
    for topicId, entryList in run.entries.items():
        sumPrec = numRel = 0
        for (rank, (docId, score, _)) in enumerate(entryList, start=1):
            if qrels.is_relevant(topicId, docId):
                numRel += 1
                sumPrec += numRel / rank
        totRelevant = qrels.get_n_relevant(topicId)
        # if totRelevant == 0: print(topicId)
        ap = sumPrec / totRelevant if totRelevant > 0 else 0
        avg += ap
        details[topicId] = ap
    numtopics = qrels.get_n_topics()
    return avg / numtopics if not detailed else (avg / numtopics, details)


def precisionAt(rank):

    def precisionAtRank(run, qrels, detailed=False):
        details = {}
        avg = 0
        for topicId, entryList in run.entries.items():
            numRelevant = len([docId for docId, score, _ in entryList[0: rank]
                               if qrels.is_relevant(topicId, docId)])
            details[topicId] = numRelevant / rank
            avg += numRelevant / rank
        numtopics = qrels.get_n_topics()
        return avg / numtopics if not detailed else (avg / numtopics, details)

    return precisionAtRank


def ndcg(run, qrels, detailed=False):

    details = {}
    avg = 0
    for topicId, entryList in run.entries.items():
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
    numtopics = qrels.get_n_topics()
    return avg / numtopics if not detailed else (avg / numtopics, details)


STD_METRICS = [avgPrec, ndcg]
