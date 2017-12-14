# -*- coding: utf-8 -*-
import csv
import re
import string

class Parse():
    def saveLine(self,subject,openRate,clickRate):
        with open("preprocessed2.txt","a+") as f:
            f.write(subject+":::"+str(openRate)+":::"+str(clickRate)+"\r\n")
    def cleanSubject(self,subject):
        subject = subject.lower()
        subject = re.sub('[\"():!?.,]','',subject)
        subject = re.sub(u'é','e',subject)
        subject = re.sub(u'è','e',subject)
        subject = re.sub(u'ê','e',subject)
        subject = re.sub(u'É','e',subject)
        subject = re.sub(u'È','e',subject)
        subject = re.sub(u'Ê','e',subject)

        subject = re.sub(u'à','a',subject)
        subject = re.sub(u'â','a',subject)
        subject = re.sub(u'À','a',subject)
        subject = re.sub(u'Â','a',subject)

        subject = re.sub(u'ù','u',subject)
        subject = re.sub(u'û','u',subject)
        subject = re.sub(u'Ù','u',subject)
        subject = re.sub(u'Û','u',subject)

        subject = re.sub(u'î','i',subject)
        subject = re.sub(u'ô','o',subject)
        subject = re.sub(u'ç','c',subject)
        subject = re.sub(u'\'','\'',subject)

        final = ""
        for word in subject.split(' '):
            if(word=="" or word=="\r\n"):
                skip=0
            else:
                final+=word+" "
        if(final=="" or final=="\r\n"):
            final="NOACCEPT"
        return final

    def concatSubjects(self,rowSplit,end,beforeSubject):
        subject=""
        for i in range(end-beforeSubject):
            if(rowSplit[beforeSubject+1+i]=="" or rowSplit[beforeSubject+1+i]=="\r\n"):
                skip=0
            elif(rowSplit[beforeSubject+1+i][0]=="\""):
                subject+=rowSplit[beforeSubject+1+i][1:]+","
            elif(rowSplit[beforeSubject+1+i][len(rowSplit[beforeSubject+1+i])-3]=="\""):
                subject+=rowSplit[beforeSubject+1+i][:-3]
            else:
                subject+=rowSplit[beforeSubject+1+i]
        subject = self.cleanSubject(subject)
        return subject
    def parse(self,filename,numLines):
        count=0
        skip=0
        subject=""
        final=[]
        with open(filename,"r")as f:
            for line in f:
                try:
                    if(count>0):
                        rowSplit = line.split(',')
                        end=len(rowSplit)-1
                        beforeSubject=0
                        #check for last number
                        check=re.compile('^[0-9]+$')
                        check2=re.compile('^[0-9]+.[0-9]+$')
                        for i in range(end):
                            if(check.match(rowSplit[end-i]) or check2.match(rowSplit[end-i])):
                                if(len(rowSplit[end-i])>=3):
                                    if("000" in rowSplit[end-i]):
                                        skip+=1
                                    elif(rowSplit[end-i][len(rowSplit[end-i])-3]!="\""):
                                        beforeSubject=end-i
                                        break
                                else:
                                    beforeSubject=end-i
                                    break
                        subject = self.concatSubjects(rowSplit,end,beforeSubject)
                        clicks=rowSplit[beforeSubject]
                        opened=rowSplit[beforeSubject-1]
                        delivered=rowSplit[beforeSubject-3]
                        if(float(delivered)>0):
                            openRate = float(opened)/float(delivered)
                        else:
                            openRate=0
                        if(float(opened)>0):
                            clickRate=float(clicks)/float(opened)
                        else:
                            clickRate=0
                        if(subject!="NOACCEPT"):
                            self.saveLine(subject,openRate,clickRate)
                    if(count==numLines):
                        return
                    count+=1
                except (IndexError, ValueError): #For when there are newline characters in the subject line for whatever reason, or if there's any weird values which dont make sense
                    count+=1

    def split_train_test(self, processedFile):
		with open(processedFile,'r') as f:
			for i,l in enumerate(f):
				pass
			fileLength=i
		with open(processedFile,'r') as f:
			for i,l in enumerate(f):
				if(i<int(fileLength*0.8)):
					with open('preprocessed_train.txt','a+') as fp:
						fp.write(l)
				else:
					with open('preprocessed_test.txt','a+') as fp:
						fp.write(l)
