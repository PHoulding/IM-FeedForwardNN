# -*- coding: utf-8 -*-
#from parse import Parse
from parse import Parse
from dictionary import Dictionary
from net import NeuralNetwork
import re
import string
import collections

	#Create Neural Network
    #Create trainer
    #parse						-Done
    #do input shit
if __name__=='__main__':
	while(1):
		nn= NeuralNetwork()
		p = Parse()
		print "1 - Preprocess the CSV file (This takes a long time -ie. more than a few hours - so dont do it often)"
		print "2 - Generate dictionary"
		print "3 - Train the Neural Network on the preprocessed data"
		print "4 - Test the Neural Network (Should only be done after training)"
		print "5 - Quit"
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
			useDict = collections.OrderedDict(sorted(d.wordDictionary.items(),key=lambda t: t[1]))
			with open("dictionary.txt","w+") as fp:
				for key,value in useDict.items():
			 		fp.write("%s:::0\r\n"%key)
		elif(userIn=="3"): #Train network
			nn.train_neural_network()
		elif(userIn=="4"): #Test network
			nn.test_neural_network()
		elif(userIn=="5"):
			quit()
'''
if __name__=='__main__':
	while(1):
		print "1 - Parse the CSV file"
		print "2 - Train the algorithm"
		print "3 - Test with your own input"
		print "4 - Quit the program"
		userIn = raw_input("Enter the command you wish to complete:")
		if(userIn=="1"): #Parse the CSV
			print "Please enter the number of lines you wish to parse, or \"all\" for all the lines"
			userIn = raw_input()
			parse = Parse()
			if(userIn=="all"):
				with open("../input/corrected.csv","r") as fp:
					for i,l in enumerate(fp):
						pass
				parse.parse("../input/corrected.csv",i+1)
			else:
				parse.parse("../input/corrected.csv",int(userIn))
			print "Parsing completed. Creating dictionary now. This may take some time..."
			asd = Dictionary()
			asd.createDictionary(parse.rows)
			asd.wordDictionary["PERSONALIZATIONFLAG"]=0
			asd.wordDictionary["NAMEUSEDFLAG"]=0
			useDict = collections.OrderedDict(sorted(asd.wordDictionary.items(),key=lambda t: t[1]))
		#	with open("dictionary.txt","w+") as fp:
		#		for key,value in useDict.items():
		#	 		fp.write("%s %d\r\n"%(key,value))
			print "Dictionary created."
		elif(userIn=="2"): #Train the algorithm
			print "not complete yet"

		elif(userIn=="3"): #Test with input
			print "not complete yet"
		elif(userIn=="4"): #Quit
			quit()
		elif(userIn=="5"):
			dict1={}
			with open("dictionary.txt","r") as f:
				with open("dictionary2.txt","w+") as fp:
					for i,line in enumerate(f):
						if(i>=20846):
							print line
							temp=line.split(" ")
				 			if(temp[0]!="aaa" and temp[0]!="pour" and temp[0]!="vous" and temp[0]!="mobilicity"\
				 				and temp[0]!="votre" and temp[0]!="mts" and temp[0]!="emax" and temp[0]!="u-verse"\
				 				and temp[0]!="at&t"):
				 					fp.write("%s,0\r\n"%temp[0])
				 	fp.write("PERSONALIZATIONFLAG,0\r\n")
				 	fp.write("NAMEUSEDFLAG,0\r\n")
	# 	print key,":",value
		#tempString = ""
	#	if("##" in key):
	#		print key,':',value
		#	tempString+=key+', '
		#	print tempString
'''
#	wordDictionary = {}
#	parse = Parse()
#	parse.parse("../input/corrected.csv",50000)

#	wordDictionary=CreateWordBank(parse.rows)
#	wordDictionary=CleanWordBank(wordDictionary)
#	wordDictionary=CheckPersonalization(wordDictionary)

#	for key,value in wordDictionary.items():
#		print key,":",value
	#	Print all the personalization keys
#		tempString = ""
#		if("##" in key):
#			print key,':',value
#			tempString+=key+', '
#		print tempString[:-2]

# def cleanWord(word):
# 	word = word.lower()
# 	word = re.sub('[\"():!?.]','',word)
# 	word = re.sub(u'é','e',word)
# 	word = re.sub(u'à','a',word)
# 	word = re.sub(u'è','e',word)
# 	word = re.sub(u'ù','u',word)
# 	word = re.sub(u'â','a',word)
# 	word = re.sub(u'ê','e',word)
# 	word = re.sub(u'î','i',word)
# 	word = re.sub(u'ô','o',word)
# 	word = re.sub(u'û','u',word)
# 	word = re.sub(u'ç','c',word)
# 	word = re.sub(u'\'','\'',word)
# 	return word

# def CreateWordBank(rows):
# #	print("here")
# 	tempTagString=""
# 	count=0
# 	tagCheck=0
# 	subjectWords=[]
# 	wordDictionary={}
# 	for row in rows:
# 		subjectWords = row[0].split(" ")
# 		wordCount=0
# 		x=0
# 		for word in subjectWords[x:]:
# 			word = cleanWord(word)
# 			#Remove two letter or less words
# 			if(len(word)<=2):
# 				count+=1
# 			#Check and pull out hashtag terms
# 			elif("##" in word and "]##" not in word):
# 				tempString=""
# 				tempCount=0
# 				#check next, if it also contains a ##, concatenate them
# 				for i in range(len(subjectWords)-wordCount-1):
# 					if("##" not in subjectWords[wordCount+i+1]):
# 						tempString+=' '+cleanWord(subjectWords[wordCount+i+1])
# 					if("##" in subjectWords[wordCount+i+1]):
# 						word=word+tempString+' '+cleanWord(subjectWords[wordCount+i+1])
# 						tempString=""
# 				if(word in wordDictionary.keys()):
# 					wordDictionary[word] += 1
# 				else:
# 					wordDictionary[word] = 1
# 			else:
# 				#Remove unimportant words (corpus)
# 				if(word=="the" or word=="and" or word=="or" or word=="is" or word=="but" \
# 				or word=="are" or word=="this" or word=="that" or word=="of" \
# 				or word=="" or word=="\n\r" or word=="\n" or word=="\r" or word=="\r\n" or word==">" \
# 				or word=="-" or word=="!" or word=="" or word=="+" or word=="a" or word==None):
# 					count+=1
# 				else:
# 					if(word in wordDictionary.keys()):
# 						wordDictionary[word] += 1
# 					else:
# 						wordDictionary[word] = 1
# 			wordCount+=1
# 	return wordDictionary

# def CleanWordBank(wordDictionary):
# 	for key,value in wordDictionary.items():
# 		if("]##" in key and "##[" not in key):
# 			del wordDictionary[key]
# 	return wordDictionary

# def CheckPersonalization(wordDictionary):
# 	pflag = 'PERSONALIZATIONFLAG'
# 	nflag = 'NAMEUSEDFLAG'
# 	for key,value in wordDictionary.items():
# 		if("##" in key):
# 			if(value>0):
# 				if("firstname" in key.lower() or "lastname" in key.lower() or "first_name" in key.lower()\
# 					or "name_first" in key.lower() or "name_last" in key.lower() or "last_name" in key.lower()\
# 					or "name" in key.lower()):
# 					if(nflag in wordDictionary.keys()):
# 						wordDictionary[nflag]+=1
# 					else:
# 						wordDictionary[nflag]=1
# 				if(pflag in wordDictionary.keys()):
# 					wordDictionary[pflag]+=1
# 				else:
# 					wordDictionary[pflag]=1
# 	return wordDictionary
