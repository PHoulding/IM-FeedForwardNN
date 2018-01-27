import random
import string
import re

'''
Shuffles the data set then splits the data into training (90%) and testing (10%)
'''
class Shuffle():
    def writeLines(self,trainLines,testLines):
        with open("trainData.txt",'w+') as f:
            for line in trainLines:
                f.write(line)
        with open("testData.txt",'w+') as f:
            for line in testLines:
                f.write(line)
        print "Done splitting"
    def splitTrainTest(self,data):
        inputData=[]
        trainLines=[]
        testLines=[]
        with open(data,"r") as f:
            for i,l in enumerate(f):
                inputData.append(l)
        random.shuffle(inputData)
        split = int(len(inputData)*0.9)
        trainLines=inputData[:split]
        testLines=inputData[split:]
        self.writeLines(trainLines,testLines)
