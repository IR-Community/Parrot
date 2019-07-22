 
<div align='center'>
<img src="https://raw.githubusercontent.com/IR-Community/Parrot/master/parrot.png" width = "100"  alt="logo" align="center" />
</div> 

# Parrot 

>Parrot is a Python-based toolkit for information retrieval research. <br>
>It aims to facilitate the implement and diagnosis of information retrieval models.

[![Python 3.6](https://img.shields.io/badge/python-3.6%20%7C%203.7-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)



## An simple example of using Parrot:


```python

from parrot.core import * 

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


####  Parrot is dependent on PyLucene, TensorFlow, Keras, and MatchZoo.


* [Python 3.7](https://www.anaconda.com/distribution/)

* [PyLucene](https://lucene.apache.org/pylucene/)

* [TensorFlow](https://www.tensorflow.org/install)

* [Keras](https://keras.io/)

* [MatchZoo](https://github.com/NTMC-Community/MatchZoo)


#### Install script for Ubuntu

* Install Python 

```bash

cd ~

curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh

bash Anaconda3-2019.03-Linux-x86_64.sh

source ~/.bashrc

conda create --name parrot python=3.7

source activate parrot

```

* Install PyLuncene  

```bash

apt-get update 

apt-get install -y default-jdk ant

cd /usr/lib/jvm/default-java/jre/lib

ln -s ../../lib amd64

mkdir /usr/src/pylucene

cd /usr/src/pylucene

curl https://dist.apache.org/repos/dist/dev/lucene/pylucene/8.1.1-rc2/pylucene-8.1.1-src.tar.gz \
    | tar -xz --strip-components=1

cd jcc \
    && JCC_JDK=/usr/lib/jvm/default-java python setup.py install
    
make all install JCC='python -m jcc' ANT=ant PYTHON=python NUM_FILES=8

```

* Install Tensorflow, Kears, and Matchzoo

```bash

pip install tensorflow

pip install keras

pip install matchzoo

```

* Install Parrot

```bash

cd ~

wget https://github.com/IR-Community/Parrot/archive/master.zip

unzip master.zip

cd Parrot-master

```

* Start Jupyter

```bash

jupyter lab

```

* Load package parrot from local folder in Jupyter Notebook ( Currently Parrot doesn't support pip install  )

```python

import os,sys
module_path = os.path.abspath(os.path.join('~/Parrot-master/'))
sys.path.append(module_path)

from parrot.core import *

```




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





Some codes are from other open source project. <br>
(e.g., https://github.com/umeat/unlzw, A Python decompression module for .Z files). 

