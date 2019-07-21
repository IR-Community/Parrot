

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
import matchzoo

from .dataset import *


class MLDataSet:


    def fold(self, fold : int):

        train_relation = []
        for index in self.train_index_list[fold]:
            train_relation.append(self.relation[index])

        train_pack = self.build_datapack(train_relation)

        test_relation = []
        for index in self.test_index_list[fold]:
            test_relation.append(self.relation[index])

        test_pack = self.build_datapack(test_relation)

        return train_pack, test_pack


    def build_datapack(self, relation):

        relation_df = pd.DataFrame(relation, columns=['id_left', 'id_right', 'label'])

        qid_set = set()
        docno_set = set()

        for rel in relation:
            qid_set.add(rel[0])
            docno_set.add(rel[1])

        left = []
        for qid, query in self.dataset.query_set.queries.items():
            if str(qid) in qid_set:
                left.append([str(qid), query.querystr])
        left_df = pd.DataFrame(left, columns=['id_left', 'text_left'])
        left_df.set_index('id_left', inplace=True)

        right = []
        N = self.dataset.collection.N
        for doc_id in range(N):
            doc_no = self.dataset.collection.docno(doc_id)
            if doc_no in docno_set:
                text = self.dataset.collection.doc(doc_id)
                text = text[0:100]
                right.append([doc_no, text])
        right_df = pd.DataFrame(right, columns=['id_right', 'text_right'])
        right_df.set_index('id_right', inplace=True)

        pack = matchzoo.data_pack.data_pack.DataPack(
            relation=relation_df,
            left=left_df,
            right=right_df,
        )

        return pack

    @staticmethod
    def load(dataset : DataSet, fold : int):
        ml_dataset = MLDataSet()
        ml_dataset.dataset = dataset

        relation = []

        for query_id, judge in dataset.judgement_set.judgements.items():
            for doc_no, item in judge.items():
                relation.append([str(query_id), doc_no, item])

        ml_dataset.relation = relation

        ml_dataset.train_index_list = []
        ml_dataset.test_index_list = []

        kf = KFold(n_splits=fold, random_state=None, shuffle=False)

        for train_index, test_index in kf.split(ml_dataset.relation):
            ml_dataset.train_index_list.append(train_index)
            ml_dataset.test_index_list.append(test_index)

        return ml_dataset

