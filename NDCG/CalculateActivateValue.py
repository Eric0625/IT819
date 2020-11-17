import h5py
import vaex
import numpy as np

def sigmoid(x):
  return 1 / (1 + np.exp(-x))

biasList = []
kernelList = []

with h5py.File('small.h5', 'r') as f:
    for i in range(3):
        if i == 0:
            index = '/model_weights/dense/dense'
        else: 
            index = f'/model_weights/dense_{i}/dense_{i}'
        layer = f[index]
        biasList.append(layer['bias:0'][:])
        kernelList.append(layer['kernel:0'][:])
    f.close()
df = vaex.open('small1.arrow')
df = df.drop(['relevance'])
inputList = list(df[0])
output = []
layerNumber = len(biasList)
finalOutput = inputList[:5]
for outputIndex in range(layerNumber):
    outputLength = len(biasList[outputIndex])
    output.append([0] * outputLength)
    for i in range(outputLength):
        output[outputIndex][i] = biasList[outputIndex][i]
        if outputIndex == 0:
            inputX = inputList
        else:
            inputX = output[outputIndex-1]
        length = len(inputX)
        for j in range(length):
            output[outputIndex][i] += kernelList[outputIndex][j][i]*inputX[j]
        #relu
        if outputIndex != layerNumber-1:
            if output[outputIndex][i] < 0:
                output[outputIndex][i] = 0
    finalOutput += output[outputIndex]
print(finalOutput) 