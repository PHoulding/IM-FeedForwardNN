# -*- coding: utf-8 -*-
import csv
import re
import string

class Dictionary():
	def __init__(self):
		self.corpus=["the","and","or","is","but","are","this","that",\
				"of","","\n\r","\n","\r","\r\n",">","<","-","!",\
				"+","a",None]
		self.skipCount=0
		self.wordDictionary={}

	def CheckPersonalization(wordDictionary):
		pflag = 'PERSONALIZATIONFLAG'
		nflag = 'NAMEUSEDFLAG'
		for key,value in wordDictionary.items():
			if("##" in key):
				if(value>0):
					if("firstname" in key.lower() or "lastname" in key.lower() or "first_name" in key.lower()\
						or "name_first" in key.lower() or "name_last" in key.lower() or "last_name" in key.lower()):
						if(nflag in wordDictionary.keys()):
							wordDictionary[nflag]+=1
						else:
							wordDictionary[nflag]=1
					if(pflag in wordDictionary.keys()):
						wordDictionary[pflag]+=1
					else:
						wordDictionary[pflag]=1
		return wordDictionary

	def addWords(self, subjectWords):
		for word in subjectWords:
			check = word.lower() in (w for i,w in enumerate(self.corpus))
			if(len(word)<=2):
				self.skipCount+=1
			elif(not check):
				if(word in self.wordDictionary.keys()):
					self.wordDictionary[word] += 1
				else:
					self.wordDictionary[word] = 1

	def concatTags(self,subjectWords):
		final=[]
		temp=""
		appendTag=0
		tempTag=0
		for word in subjectWords:
			if(word!="" and len(word)>1):
				if(word[0]=="\""):
					word = word[1:]
				elif(word[len(word)-1]=="\""):
					word=word[:-1]
				elif(word[len(word)-1]==","):
					word=word[:-1]
				if(word[0]=="#" and word[len(word)-1]!="#"):
					temp=""
					appendTag=1
				elif(word[len(word)-1]=="#"):
					appendTag=0
					temp+=word
					tempTag=1
				if(appendTag):
					temp+=word+" "
				else:
					if(tempTag):
						final.append(temp)
						temp=""
					else:
						final.append(word)
					tempTag=0
		return final
	# 	for word in final:
	# 		if(len(word)>1 and word!=""):
	# 			print word
	# 			if("##" in word and (word[0]!="#" or word[len(word)-1]!="#")):
	# 				print word
	# 	#print final

	# From analysis of data, there seem to currently be 6 cases:
	# 1) ##TAG## string							-Done
	# 2) ##TAG## string ##TAG##					-Done
	# 3) ##TAG##%								-Done
	# 4) test_##TAG##_##TAG##					-Done
	# 5) ##TAG## string ##TAG TAG##				-Done
	# 6) Normal string with no special cases	-Done
	def createDictionary(self,preprocessedFile):
		with open(preprocessedFile,"r") as f:
			for line in f:
				lineSplit = line.split(":::")
				if("##" in lineSplit[0]): # Has personalization tag
					numTags = 0
					for i in range(len(lineSplit[0])):
						if(lineSplit[0][i-1]=="#"):
							numTags+=1
					if(numTags==4):
						if("%" in lineSplit[0]): #Case 3
							subjectWords = lineSplit[0].split(" ")
							self.addWords(subjectWords)                   #Check this
						else: #Case 1
							subjectWords = lineSplit[0].split(" ")
							final = self.concatTags(subjectWords)
							self.addWords(final)
					elif(numTags>4): #Case 2, 4, or 5
						subjectWords = lineSplit[0].split(" ")
						final = self.concatTags(subjectWords)
						self.addWords(final)
				else:
					subjectWords = lineSplit[0].split(" ")
					self.addWords(subjectWords)
'''
	# From analysis of data, there seem to currently be 6 cases:
	# 1) ##TAG## string							-Done
	# 2) ##TAG## string ##TAG##					-Done
	# 3) ##TAG##%								-Done
	# 4) test_##TAG##_##TAG##					-Done
	# 5) ##TAG## string ##TAG TAG##				-Done
	# 6) Normal string with no special cases	-Done
	def createDictionary(self, rows):
		for row in rows:
			if("##" in row[0]):
				#Has a personalization tag
				numTags=0
				for i in range(len(row[0])):
					if(row[0][i-1]=="#"):
						numTags+=1
				if(numTags==4): #Case 1 or 3
					if("%" in row[0]): #Case 3
						subjectWords = row[0].split(" ")
						self.addWords(subjectWords)
					else: #Case 1
						#Split on spaces, append stuff between tags
						subjectWords = row[0].split(" ")
						final=self.concatTags(subjectWords)
						self.addWords(final)
				elif(numTags>4): #Case 2, 4, or 5
					subjectWords = row[0].split(" ")
					final=self.concatTags(subjectWords)
					self.addWords(final)
			else:
				#Does not have a personalization tag
				subjectWords = row[0].split(" ")
				self.addWords(subjectWords)
'''
