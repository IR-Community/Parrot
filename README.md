 
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

import matchzoo as mz

train_pack = mz.datasets.wiki_qa.load_data('train', task='ranking')
valid_pack = mz.datasets.wiki_qa.load_data('dev', task='ranking')
predict_pack = mz.datasets.wiki_qa.load_data('test', task='ranking')
```



## References





