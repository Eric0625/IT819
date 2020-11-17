import numpy as np
from sklearn.metrics import ndcg_score
# import pandas as pd
import vaex
import time

def convert(filename):
    colnames = ['col']*136
    for i in range(136):
        colnames[i] += str(i+1) 
    df = vaex.from_csv(f'MSLR-WEB10K/Fold1/{filename}.txt', sep=' ', usecols=range(138), names=['relevance', 'qid'] + colnames)
    df.export(f'MSLR-WEB10K/Fold1/{filename}.arrow')

def doCalculate(filename):
    df = vaex.open(f'{filename}.arrow')
    startTime = int(time.time())
    # df = vaex.open('MSLR-WEB10K/Fold1/train.arrow')
    qidList = df.qid.unique()
    ndcgList = []
    for qid in qidList:
        df.select(df.qid == qid)
        true_relevance = df.evaluate(df.relevance, selection=True)
        if len(true_relevance) < 2:   
            ndcgList.append(1)  
            continue
        scores = np.asarray(range(0, len(true_relevance))[: :-1])
        ndcg = ndcg_score(np.asarray([true_relevance]), np.asarray([scores]))
        ndcgList.append(ndcg)
    endTime = int(time.time())
    print(f'time used {endTime-startTime} sec')
    print(np.array(ndcgList).mean())

# convert('vali')
doCalculate('train')
# doCalculate('vali')
# doCalculate('test')
print('done')