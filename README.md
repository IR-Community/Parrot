 
<div align='center'>
<img src="https://raw.githubusercontent.com/IR-Community/Parrot/master/parrot.png" width = "100"  alt="logo" align="center" />
</div> 

# Parrot 

>Parrot is a Python-based toolkit for information retrieval research. <br>
>It aims to facilitate the implement and diagnosis of information retrieval models.

[![Python 3.6](https://img.shields.io/badge/python-3.6%20%7C%203.7-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)



## An example of using Parrot:


```python
from parrot.core import * 
from parrot.model import *

# load index, topics and judgements from local folders

dataset = DataSet.load(
    base + "./index/ap90",
    base + "./topics/ap90-51-100",
    base + "./qrels/ap90-51-100",
    True
)

# implement and run the BM25 model

import math

class MyBM25Model(Model):

    def __init__(self, b=0.75, k1=1.2):
        self.b = b; self.k1 = k1; 

    def score_term(self, tf: float, tn: float, dl: float,
                  ql: float, ctf: float, df: float, qtf: float,
                  ctn: float, C: float, N: float):
        b = self.b; k1 = self.k1
        avgdl = C / N
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        tf_part = tf * (k1 + 1)\
                  / (tf + k1 * (1 - b + b * dl / avgdl))
        return tf_part * idf

model = MyBM25Model(b=0.4, k1=0.9)

result_set = model.run(dataset)
print(result_set.avg_prec())
print(result_set.ndcg())
print(result_set.precision_at(10))

```



## References


[Tutorials](https://github.com/IR-Community/Parrot/tree/master/parrot/examples)


## Install


1. [Install Python 3.7](https://www.anaconda.com/distribution/) *

* Step 2 : [Install Python 3.7](https://www.anaconda.com/distribution/) *



## Citation

If you use Parrot in your research, please use the following citation.

```
@inproceedings{Tu:2019:PPI:3331184.3331393,
 author = {Tu, Xinhui and Huang, Jimmy and Luo, Jing and Zhu, Runjie and He, Tingting},
 title = {Parrot: A Python-based Interactive Platform for Information Retrieval Research},
 booktitle = {Proceedings of the 42Nd International ACM SIGIR Conference on Research and Development in Information Retrieval},
 series = {SIGIR'19},
 year = {2019},
 isbn = {978-1-4503-6172-9},
 location = {Paris, France},
 pages = {1289--1292},
 numpages = {4},
 url = {http://doi.acm.org/10.1145/3331184.3331393},
 doi = {10.1145/3331184.3331393},
 acmid = {3331393},
 publisher = {ACM},
 address = {New York, NY, USA},
 keywords = {deep learning, information retrieval, python},
} 

```



