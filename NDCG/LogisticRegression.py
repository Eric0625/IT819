import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import rich

def Sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))
def iris_type(s):
    class_label = {'setosa':0, 'versicolor':1, 'virginica':2}
    return class_label[s]

# groups = data.groupby(by = "species")
# means, sds = groups.mean(), groups.std()
# means.plot(yerr = sds, kind = 'bar', figsize = (9, 5), table = True)
# plt.show()
new_iris = pd.io.parsers.read_csv('iris.csv', converters = {4:iris_type})
data = np.array(new_iris)  # 或者直接new_iris.values,结果是一样的
# 用np.split按列（axis=1）进行分割
# (4,):分割位置，前4列作为x的数据，第4列之后都是y的数据
x,y = np.split(data, (4,), axis = 1)  
# X = x[:,0:2] # 取前两列特征
# 用train_test_split将数据按照7：3的比例分割训练集与测试集，
# 随机种子设为1（每次得到一样的随机数），设为0或不设（每次随机数都不同）
x_train, x_test, y_train,y_test = train_test_split(x,y,test_size = 0.3,random_state = 0)

pipe_LR = Pipeline([
                    ('sc', StandardScaler()),
                    ('pca', PCA(n_components = 2)),
                    ('clf_lr', LogisticRegression(random_state=1))
                    ])
# 开始训练
pipe_LR.fit(x_train, y_train.ravel())
print(f"训练集准确率: {pipe_LR.score(x_train, y_train):.2f}")
print(f"测试集准确率: {pipe_LR.score(x_test, y_test):.2f}")

y_hat = pipe_LR.predict(x_test)
accuracy = metrics.accuracy_score(y_test, y_hat)
print("逻辑回归分类器的准确率：%0.2f" % accuracy)

target_names = ['setosa', 'versicolor', 'virginica']
print(metrics.classification_report(y_test, y_hat, target_names = target_names))