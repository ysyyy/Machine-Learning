from numpy import *
import operator
from os import listdir
def createDataSet():
        group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
        labels = ['A','A','B','B']
        return group, labels
def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect
def classify0(inX,dataSet,labels,k):
    #inX：用于分类的输入向量
    #dataSet：输入的训练样本集
    #labels：样本数据的类标签向量
    #k：用于选择最近邻居的数目
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX,(dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    classCount={}
    for i in range(k):
        voteIlable = labels[sortedDistIndicies[i]]
        classCount[voteIlable] = classCount.get(voteIlable,0)+1
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    # python2中的iteritems与python3中的items函数等价
    return sortedClassCount[0][0]
def handwritingClassTest(k):
    hwLabels = []
    trainingFileList = listdir('digits/trainingDigits')
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('digits/trainingDigits/%s'% fileNameStr)
    testFileList = listdir('digits/testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr=testFileList[i]
        fileStr=fileNameStr.split('.')[0]
        classNumStr=int(fileStr.split('_')[0])
        vectorTest = img2vector('digits/testDigits/%s' % fileNameStr)
        classifierResults = classify0(vectorTest,trainingMat,hwLabels,k)
        print ("预测结果:%d,实际结果:%d\n"%(classifierResults,classNumStr))
        if (classifierResults!=classNumStr):errorCount+=1.0
    print("总错误数:%d\n"%errorCount)
    print("错误率:%f\n"%(errorCount/float(mTest)))
    return errorCount/float(mTest)
handwritingClassTest(6)
    