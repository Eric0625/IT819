import numpy as np
from sklearn.metrics import ndcg_score
# import pandas as pd
import vaex
import time
from LambdaRankNN import LambdaRankNN

def cleanData(filename):
    df = vaex.open(f'{filename}.arrow')
    #去掉字符串
    def getRidofSemicolon(data):
        if not isinstance(data, str):
            return float(data)
        slices = data.split(':')
        if len(slices) > 1:
            return float(slices[1])
        return float(data)
    colnames = df.get_column_names()
    for col in colnames:
        df[col] = df.apply(getRidofSemicolon, arguments=[df[col]])
    df.export(f'{filename}1.arrow')

def doCalculate(filename):
    df = vaex.open(f'{filename}1.arrow')
    startTime = int(time.time())
    y = df.relevance.to_numpy()
    qidList = df.qid.to_numpy()
    X = df[['col1', 'col2', 'col3']].to_pandas_df()
    
    # X = np.array([[0.2, 0.3, 0.4],
    #           [0.1, 0.7, 0.4],
    #           [0.3, 0.4, 0.1],
    #           [0.8, 0.4, 0.3],
    #           [0.9, 0.35, 0.25]])
    # y = np.array([0, 1, 0, 0, 2])
    # qidList = np.array([1, 1, 1, 2, 2])

    ranker = LambdaRankNN(input_size=X.shape[1], hidden_layer_sizes=(10,5,1), activation=('relu', 'relu', 'relu'), solver='adam')
    ranker.fit(X, y, qidList, epochs=10)
    y_pred = ranker.predict(X)
    print(y_pred)
    ranker.evaluate(X, y, qidList, eval_at=5)
    endTime = int(time.time())
    print(f'time used {endTime - startTime} seconds')

# cleanData('small')
doCalculate('small')
# generate query data


# train model
print('done')