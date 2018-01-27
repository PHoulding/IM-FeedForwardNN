# -*- coding: utf-8 -*-
#from parse import Parse
from parse import Parse
from dictionary import Dictionary
from net import NeuralNetwork
import re
import string
import collections
from shuffle import Shuffle

'''
This is the main function for the project
- Includes simple choice directory for the user to dictate what they want to do
'''
if __name__=='__main__':
	#Runs until program is quit
	while(1):
		nn= NeuralNetwork()
		p = Parse()
		print "1 - Preprocess the CSV file (This takes a long time -ie. more than a few hours - so dont do it often)"
		print "2 - Generate dictionary"
		print "3 - Train the Neural Network on the preprocessed data"
		print "4 - Test the Neural Network (Should only be done after training)"
		print "5 - Shuffle the dataset"
		print "6 - Quit"
		userIn = raw_input("Please enter the desired action:")
		if(userIn=="1"): #PreProcess
			with open("../input/corrected.csv","r") as fp:
				for i,l in enumerate(fp):
					pass
				#p.parse("../input/corrected.csv",i+1)
				p.split_train_test("preprocessed.txt")
		elif(userIn=="2"): #Generate Dictionary
			d = Dictionary()
			d.createDictionary("preprocessed.txt")
			d.wordDictionary["PERSONALIZATIONFLAG"]=0
			d.wordDictionary["NAMEUSEDFLAG"]=0
			d.wordDictionary["SUBJECTLINELENGTHFLAG"]=0
			#Creates a sorted dictionary to write the words to
			useDict = collections.OrderedDict(sorted(d.wordDictionary.items(),key=lambda t: t[1]))
			with open("dictionary.txt","w+") as fp:
				for key,value in useDict.items():
			 		fp.write("%s:::0\r\n"%key)
		elif(userIn=="3"): #Train network
			nn.train_neural_network()
		elif(userIn=="4"): #Test network
			nn.test_neural_network()
		elif(userIn=="5"): #Shuffle the dataset
			inputData = Shuffle()
			inputData.splitTrainTest("preprocessed.txt")
		elif(userIn=="6"): #quits
			quit()
