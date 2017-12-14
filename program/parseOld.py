# -*- coding: utf-8 -*-
import csv
import re
import string

class Parse():
	def __init__(self):
		self.rows=[]
		self.rowSplit=[]
		self.addRow=[]
		self.BeginTime=""
		self.EndTime=""
		self.Sent=0
		self.Delivered=0
		self.Opened=0
		self.Clicks=0
		self.Subject=""
		self.openRate = 0
		self.clickRate = 0

	def saveLine(self,rowSplit):
		self.Subject=rowSplit[0]
		self.BeginTime=rowSplit[1]
		self.EndTime=rowSplit[2]
		self.Sent=rowSplit[3]
		self.Delivered=rowSplit[4]
		self.Opened=rowSplit[5]
		self.Clicks=rowSplit[6]

		#print self.Delivered
		#print self.Opened
		if(float(self.Delivered)>0):
			self.openRate = float(self.Opened)/float(self.Delivered)
		else:
			self.openRate=0
		if(float(self.Opened)>0):
			self.clickRate = float(self.Clicks)/float(self.Opened)
		else:
			self.clickRate=0
		self.addRow.append(self.Subject)
		self.addRow.append(self.BeginTime)
		self.addRow.append(self.EndTime)
		self.addRow.append(self.Sent)
		self.addRow.append(self.Delivered)
		self.addRow.append(self.Opened)
		self.addRow.append(self.Clicks)
		self.addRow.append(self.openRate)
		self.addRow.append(self.clickRate)

		self.rows.append(self.addRow)
		writeSubject=""
		subjectSplit=self.Subject.split(" ")
		for word in subjectSplit:
			if(word!="" and word!="\r\n"):
				writeSubject+=word+" "
		with open("preprocessed.txt","a+") as f:
			if(writeSubject!=""):
				f.write(writeSubject+":::"+str(self.openRate)+":::"+str(self.clickRate)+"\r\n")
		self.addRow = []
		self.Subject=""

	def parse(self, filename,numLines):
		count=0
		skip=0
		campaignID=""
		subject=""
		final=[]
		with open(filename,"r") as f:
			for line in f:
				if(count>0):
					try:
						self.rowSplit=line.split(',')
						#print count, self.rowSplit[11]
						if(len(self.rowSplit)>13):
							#Extra commas
							end=len(self.rowSplit)-1
							clicks=0
							beforeSubject=0
							subject=""
							#Find the last number column (Clicks)
							for i in range(end):
								check = re.compile('^[0-9]+$')
								check2 = re.compile('^[0-9]+.[0-9]+$')
								if(check.match(self.rowSplit[end-i]) or check2.match(self.rowSplit[end-i])):
									if(len(self.rowSplit[end-i])>=3):
										if("000" in self.rowSplit[end-i]):
											skip+=1
										elif(self.rowSplit[end-i][len(self.rowSplit[end-i])-3]!="\""):
											beforeSubject=end-i
											break
									else:
										beforeSubject=end-i
										break
							#Concatenate all the subjects together
							for i in range(end-beforeSubject):
								if(self.rowSplit[beforeSubject+1+i][0]=="\""):
									subject+=self.rowSplit[beforeSubject+i+1][1:]+","
								elif(self.rowSplit[beforeSubject+1+i][len(self.rowSplit[beforeSubject+1+i])-3]=="\""):
									#-3 because end of string would be '#\r\n'
									subject+=self.rowSplit[beforeSubject+i+1][:-3]
								else:
									subject+=self.rowSplit[beforeSubject+i+1]
							#print subject
							#Set the values for saving
							clicks=self.rowSplit[beforeSubject]
							opened=self.rowSplit[beforeSubject-1]
							bounced=self.rowSplit[beforeSubject-2]
							delivered=self.rowSplit[beforeSubject-3]
							sent=self.rowSplit[beforeSubject-4]
							endTime=self.rowSplit[beforeSubject-5]
							beginTime=self.rowSplit[beforeSubject-6]
							mailingName=""
							#Concatenate all the mailing names together (isn't important in the actual program)
							for i in range(beforeSubject-6):
								if(i>3):
									if(self.rowSplit[i][0]=="\""):
										mailingName+=self.rowSplit[i][1:]
									elif(self.rowSplit[i][len(self.rowSplit[i])-1]=="\""):
										mailingName+=self.rowSplit[i][:-1]
									else:
										mailingName+=self.rowSplit[i]
							final=[subject,beginTime,endTime,sent,delivered,opened,clicks]
							self.saveLine(final)
						else:
						#no extra commas -> set values and save
							subject=self.rowSplit[12]
							beginTime=self.rowSplit[5]
							endTime=self.rowSplit[6]
							sent=self.rowSplit[7]
							delivered=self.rowSplit[8]
							opened=self.rowSplit[9]
							clicks=self.rowSplit[10]
							final=[subject,beginTime,endTime,sent,delivered,opened,clicks]
							self.saveLine(final)
					except (ValueError,IndexError):
						skip+=1
				if(count==numLines):
					return
				count+=1



	# def parse(self,filename,numLines):
	# 	count=0
	# 	with open(filename,"r") as f:
	# 		for line in f:
	# 			if(count>0):
	# 				print count
	# 				self.rowSplit=line.split(',')
	# 				if(len(self.rowSplit)>13):
	# 					rowSplit=self.concatLine(rowSplit)
	# 				#	for i in range(len(self.rowSplit)-12):
	# 				#		self.Subject+=self.rowSplit[i+12]
	# 				else:
	# 					self.Subject=self.rowSplit[12]
	# 				self.BeginTime=self.rowSplit[5]
	# 				self.EndTime = self.rowSplit[6]
	# 				self.Sent = self.rowSplit[7]
	# 				self.Delivered = self.rowSplit[8]
	# 				self.Opened = self.rowSplit[10]
	# 				self.Clicks = self.rowSplit[11]
	# 				if(self.Delivered!="" and self.Opened!=""):
	# 					if(float(self.Delivered)>0):
	# 						self.openRate = float(self.Opened)/float(self.Delivered)
	# 				else:
	# 					self.openRate=0
	# 				if(self.Opened!="" and self.Clicks!=""):
	# 					if(float(self.Opened)>0):
	# 						self.clickRate = float(self.Clicks)/float(self.Opened)
	# 				else:
	# 					self.clickRate=0

	# 				self.addRow.append(self.Subject)
	# 				self.addRow.append(self.BeginTime)
	# 				self.addRow.append(self.EndTime)
	# 				self.addRow.append(self.Sent)
	# 				self.addRow.append(self.Delivered)
	# 				self.addRow.append(self.Opened)
	# 				self.addRow.append(self.Clicks)
	# 				self.addRow.append(self.openRate)
	# 				self.addRow.append(self.clickRate)

	# 				self.rows.append(self.addRow)
	# 				self.addRow = []
	# 				self.Subject=""
	# 			#If you reach the nth line, output
	# 			if(count==numLines):
	# 				return
	# 			count+=1

	def PrintRows(self, rows):
		count=0
		for row in rows:
			print count, row
			count+=1
