import numpy as np
import pandas as pd
import time
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from reco.recommender import FM
from sklearn.model_selection import train_test_split

def initData():
    train = pd.read_csv('PoiRatings.csv')
    cols = ['rating', 'poi_id', 'user_id']
    trainSub = train[cols]
    trainSub['rating'].fillna(1, inplace = True)

    train, test = train_test_split(trainSub, test_size = 0.3, random_state = 5)
    print(f' train data: \n {train.head()}')
    train.to_csv('data/train.csv', index=False)
    test.to_csv('data/test.csv', index=False)

def executeFM(epoch, learningRate, train, test, y_train, y_test):
    # global train, test, y_test, y_train
    print(f'start FM with it:{epoch}, lr:{learningRate}')
    f = FM(k=10, iterations = epoch, learning_rate = learningRate, regularizer=0.005)
    f.fit(X=train, y=y_train)
    y_pred = f.predict(test)
    rmse = np.square(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    return {"pred":y_pred, 'rmse': rmse, 'mae': mae}


train = pd.read_csv('data/train.csv')
y_train = train['rating']
train.drop(['rating'], axis=1, inplace=True)
train['user_id'] = train['user_id'].astype('str')
train['poi_id'] = train['poi_id'].astype('str')

test = pd.read_csv('data/test.csv')
y_test = test['rating']
test.drop(['rating'], axis=1, inplace=True)
test['user_id'] = test['user_id'].astype('str')
test['poi_id'] = test['poi_id'].astype('str')

iterations = [20, 60, 100, 200, 300, 480, 700, 1000, 1500, 2000]
learningRates = [0.01, 0.005, 0.001, 0.0001]
resultRMSE = {'iteration': iterations}
resultMAE = {'iteration': iterations}
for lr in learningRates:
    lrRMSEName = f'RMSE({lr})'
    lrMAEName = f'MAE({lr})'
    lrRMSEGroup = []
    lrMAEGroup = []
    for i in range(3):
        print(f'********循环第{i+1}次*********')
        lrRMSE = []
        lrMAE = []
        for it in iterations:
            result = executeFM(it, lr, 
                                train.copy(), test.copy(), 
                                y_train.copy(), y_test.copy())
            lrRMSE.append(result['rmse'])
            lrMAE.append(result['mae'])
        lrRMSEGroup.append(lrRMSE)
        lrMAEGroup.append(lrMAE)
    finalRMSE = np.mean(np.array(lrRMSEGroup), axis=0)
    finalMAE = np.mean(np.array(lrMAEGroup), axis=0)
    resultRMSE[lrRMSEName] = finalRMSE
    resultMAE[lrMAEName] = lrMAE

rmsePd = pd.DataFrame(data=resultRMSE)
print(rmsePd)
timestamp = str(int(time.time()))
rmsePd.to_csv(f'output/rmse{timestamp}.csv')
print('===================')
maePd = pd.DataFrame(data=resultMAE)
print(maePd)
maePd.to_csv(f'output/mae{timestamp}.csv')