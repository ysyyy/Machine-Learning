# -*- coding: UTF-8 -*- 

#a for training ,e for test

from numpy import *
import operator
from os import listdir
 
def madeVector(fileAddress):

        #初始化向量
        returnVector = zeros((1,1024))

        #读取文件内容／读取逐行
        fr = open(fileAddress)
        for i in range(32):
                lineStr = fr.readline()

                for j in range(32):
                        returnVector[0,i*32 + j] = int(lineStr[j])

        return returnVector



def classify(Vector, DataSet, labels, k):

        #计算训练数据阵的行数，初始化装填相应倍数测试向量的数组／计算距离得到与各测试数据距离向量拼成的矩阵
        DataSetShape = DataSet.shape[0]
        diffMat = tile( Vector, (DataSetShape,1) ) - DataSet
        sqDiffMat = diffMat ** 2
        sqDistances = sqDiffMat.sum(axis=1)
        distances = sqDistances ** 0.5

        #初始化计数器
        calculator = {}
	sortedList = distances.argsort()

        #按从距离小到大顺序的标准排列Ｄｉｓｔａｎｃｅｓ中元素的序号，根据序号在标签列表中取出相应的标签,精度为用户设置的k
        for i in range(k):
	        voteLabel = labels[sortedList[i]]
        	calculator[voteLabel] = calculator.get(voteLabel,0) + 1

   	# 对类别出现的频次进行排序，从高到低
   	classifyResult = sorted(calculator.iteritems(), key=operator.itemgetter(1), reverse=True)

   	# 返回出现频次最高的类别
   	return classifyResult[0][0]                



#读取"训练数据文件名列表"和数量／初始化”标签向量“
aFileList = listdir('digits/trainingDigits/')
n = len(aFileList)
hwlabels = []

#初始化装填“训练数据向量”的数组
aDataSet = zeros((n,1024 ))

#读取所有“训练数据文件'加工为向量并依序存入数组／制作＂标签向量＂
for i in range(n):
	aFileName = aFileList[i]
	aDataSet[i,:] = madeVector('digits/trainingDigits/%s' % aFileName)
	aFileNumber = int( aFileName.split('_')[0] )
	hwlabels.append(aFileNumber)


#初始化错误次数，读入＂精度＂
eFileList = listdir('digits/testDigits')
m = len(eFileList)
errors = 0.0
k = int( raw_input('Please enter a number as stardard: ') )

#依次输入＂测试数据阵＂得到测试结果／比较＂测试结果＂与＂正确结果＂并记录错误次数／打印测试结果和正确答案
for i in range(m):
	eFileName = eFileList[i]
	eDataVector = madeVector('digits/testDigits/%s' % eFileName)
	trueAnswer = int( eFileName.split('_')[0] )
	testResult = classify(eDataVector, aDataSet, hwlabels, k)
	print '\n 分类结果是%d,正确答案是%d' % (testResult,trueAnswer)
	if trueAnswer != testResult:
		errors +=1.0

#计算并打印错误次数和正确率
print '错误次数:%d' % errors
print '\n正确率:%f' % (errors/float(m))





	
	











	
