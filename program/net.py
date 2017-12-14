import tensorflow as tf
import numpy as np
import re
import string
from dictionary import Dictionary

#Testing creating Dataset
#x's shape will be [~ 600000 , 100] ie: 600k input w/ a 102 length array defining it
#None means it can be of any length
class NeuralNetwork():
    def __init__(self):
        self.n_nodes_hl1=1500
        self.n_nodes_hl2=1500
        self.n_classes=11
        self.batch_size=50
        with open('preprocessed.txt','r') as f:
            for i,l in enumerate(f):
                pass
            numInputs=i
        self.total_batches=int((numInputs*0.4)/self.batch_size)
        self.hm_epochs=2

        self.x=tf.placeholder('float')
        self.y=tf.placeholder('float')

        self.hidden_1_layer={'f_fum':self.n_nodes_hl1,\
                        'weight':tf.Variable(tf.random_normal([20978,self.n_nodes_hl1])),\
                        'bias':tf.Variable(tf.random_normal([self.n_nodes_hl1]))}
        self.hidden_2_layer={'f_fum':self.n_nodes_hl2,\
                        'weight':tf.Variable(tf.random_normal([self.n_nodes_hl1,self.n_nodes_hl2])),\
                        'bias':tf.Variable(tf.random_normal([self.n_nodes_hl2]))}
        self.output_layer={'f_fum':None,\
                        'weight':tf.Variable(tf.random_normal([self.n_nodes_hl2,self.n_classes])),\
                        'bias':tf.Variable(tf.random_normal([self.n_classes]))}
        self.saver = tf.train.Saver()
        self.tf_log = 'tf.log'

    def neural_network_model(self,data):
        l1 = tf.add(tf.matmul(data,self.hidden_1_layer['weight']),self.hidden_1_layer['bias'])
        l1 = tf.nn.relu(l1)
        l2 = tf.add(tf.matmul(l1,self.hidden_2_layer['weight']),self.hidden_2_layer['bias'])
        l2 = tf.nn.relu(l2)
        output = tf.matmul(l1,self.output_layer['weight']+self.output_layer['bias'])
        return output

    def createBagOfWords(self,subjectLine):
        with open('dictionary.txt','r') as dFile:
            for i,l in enumerate(dFile):
                pass
            dictLength=i
        features=np.zeros(dictLength+1)
        words = subjectLine.split(" ")
        for word in words:
            with open('dictionary.txt',"r") as dFile:
                for lineNum,line in enumerate(dFile):
                    if(word==line.split(':::')[0]):
                        features[lineNum]+=1
        return features
    def createLabel(self,openRate):
        label=[]
        if(0 < openRate <= 0.1):
            label=[0,1,0,0,0,0,0,0,0,0,0]
        elif(0.1 < openRate <= 0.2):
            label=[0,0,1,0,0,0,0,0,0,0,0]
        elif(0.2 < openRate <= 0.3):
            label=[0,0,0,1,0,0,0,0,0,0,0]
        elif(0.3 < openRate <= 0.4):
            label=[0,0,0,0,1,0,0,0,0,0,0]
        elif(0.4 < openRate <= 0.5):
            label=[0,0,0,0,0,1,0,0,0,0,0]
        elif(0.5 < openRate <= 0.6):
            label=[0,0,0,0,0,0,1,0,0,0,0]
        elif(0.6 < openRate <= 0.7):
            label=[0,0,0,0,0,0,0,1,0,0,0]
        elif(0.7 < openRate <= 0.8):
            label=[0,0,0,0,0,0,0,0,1,0,0]
        elif(0.8 < openRate <= 0.9):
            label=[0,0,0,0,0,0,0,0,0,1,0]
        elif(0.9 < openRate <= 1):
            label=[0,0,0,0,0,0,0,0,0,0,1]
        else:
            label=[1,0,0,0,0,0,0,0,0,0,0]
        return label

    def train_neural_network(self):
        prediction = self.neural_network_model(self.x)
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction,labels=self.y))
        optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(cost)
        with open('preprocessed.txt','r') as f:
            for i,l in enumerate(f):
                pass
            numInputs=i
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            try:
                epoch = int(open(self.tf_log,'r').read().split('\n')[-2])+1
                print("Starting:",epoch)
            except:
                epoch=1
            while epoch<=self.hm_epochs:
                if(epoch!=1):
                    self.saver.restore(sess,"./model.ckpt")
                epoch_loss=1
                #Load dictionary
                with open('preprocessed.txt',buffering=20000) as f:
                    batch_x=[]
                    batch_y=[]
                    batches_run=0
                    for numLine,line in enumerate(f):
                        if(numLine<int(numInputs*0.4)):
                            subject=line.split(':::')[0]
                            openRate=line.split(':::')[1]
                            #Generate bag of words for subject
                            features=self.createBagOfWords(subject)
                            label=self.createLabel(float(openRate))
                            line_x = features
                            line_y = label
                            batch_x.append(line_x)
                            batch_y.append(line_y)
                            if(len(batch_x)>=self.batch_size):
                                _, c =sess.run([optimizer,cost],feed_dict={self.x:np.array(batch_x),self.y:np.array(batch_y)})
                                with open("dump.txt","w+") as dumpF:
                                    dumpF.write(str(batch_x)+"\r\n\r\n")
                                epoch_loss+=c
                                batch_x=[]
                                batch_y=[]
                                batches_run+=1
                                print 'Batch run:',batches_run,'/',self.total_batches,'| epoch:',epoch,'| Batch loss:',c
                self.saver.save(sess,"./model.ckpt")
                print 'Epoch',epoch,'completed out of',self.hm_epochs,'total loss:',epoch_loss,'avg loss',epoch_loss/self.total_batches
                with open(self.tf_log,'a') as f:
                    f.write(str(epoch)+'\n')
                epoch+=1

    def test_neural_network(self):
        prediction=self.neural_network_model(self.x)
        with open('preprocessed.txt','r') as f:
            for i,l in enumerate(f):
                pass
            numInputs=i
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            for epoch in range(self.hm_epochs):
                try:
                    self.saver.restore(sess,"./model.ckpt")
                except Exception as e:
                    print str(e)
                epoch_loss=0
            correct=tf.equal(tf.argmax(prediction,1),tf.argmax(self.y,1))
            accuracy = tf.reduce_mean(tf.cast(correct,'float'))
            feature_sets=[]
            labels=[]
            counter=0
            with open('preprocessed.txt',buffering=20000) as f:
                for numLine,line in enumerate(f):
                    if(numLine>int(numInputs*0.96)):
                        try:
                            subject=line.split(':::')[0]
                            openRate=line.split(':::')[1]
                            features=self.createBagOfWords(subject)
                            label=self.createLabel(float(openRate))
                            feature_sets.append(features)
                            labels.append(label)
                            counter+=1
                        except Exception as e:
                            print str(e)

            print 'Tested',counter,'samples.'
            test_x=np.array(feature_sets)
            test_y=np.array(labels)
            print 'Accuracy:',accuracy.eval({self.x:test_x,self.y:test_y})
            output = sess.run(prediction,feed_dict={self.x:test_x})
            print output
            count=0
            with open("output.txt","w+") as outF:
                for _ in output:
                    outF.write(str(_)+":::"+str(test_y[count])+"\r\n")
                    count+=1

'''
    def pullSubjectAndOpenRate(line):
        split = line.split(",")
        if(len(split)>13): #extra commas
            end=len(split)-1
            beforeSubject=0
            subject=""
            opens=0
            #Find last number column
            for i in range(end):
                check=re.compile('^[0-9]+$')
                check2=re.compile('^[0-9]+.[0-9+]$')
                if(check.match(split[end-i]) or check2.match(split[end-i])):
                    if(len(split[end-i])>=3):
                        if("000" in split[end-i]):
                            skip+=1
                        elif(split[end-i][len(split[end-i])-3]!="\""):
                            beforeSubject=end-i
                            break
                    else:
                        beforeSubject=end-i
                        break
            #Concat all subject parts together
            for i in range(end-beforeSubject):
                if(split[beforeSubject+1+i][0]=="\""):
                    subject+=split[beforeSubject+i+1][1:]+","
                elif(split[beforeSubject+1+i][len(split[beforeSubject+1+i])-3]=="\""):
                    subject+=split[beforeSubject+i+1][:-3]
                else:
                    subject+=split[beforeSubject+i+1]
            opens=split[beforeSubject-1]
            delivered=split[beforeSubject-3]
    #        print delivered
            if(float(delivered)<=0):
                openRate=0
            else:
                openRate=float(opens)/float(delivered)
            return subject,openRate
        else: #No extra commas
            subject=split[12]
            opens=split[9]
            delivered=split[8]
    #        print delivered
            if(float(delivered)<=0):
                openRate=0
            else:
                openRate=float(opens)/float(delivered)
            return subject,openRate

    def createDataset(inputFile, dictFile):
        skip=0
        lineCount=0
        dictLength=0
        with open(dictFile,"r") as dFile:
            for i,l in enumerate(dFile):
                pass
            dictLength=i
        features=np.zeros((200,dictLenth))
        labels=np.zeros((200,10))
        with open(inputFile,"r") as f:
            for line in f:
                if(lineCount>0):
                    #parse subject lines according to dictionary2 into features array
                    subject,openRate=pullSubjectAndOpenRate(line)
                    words = subject.split(" ")
                    lineFeatures=np.zeros((1,dictLength))
                    for word in words:
                        d=Dictionary()
                        word = d.cleanWord(word)
                        count=0
                        with open(dictFile,"r") as df:
                            for dfLine in df:
                                dfWord=dfLine.split(",")[0]
                                if(word==dfWord):
                                    lineFeatures[0][count]+=1
                                count+=1
                    features[lineCount-1]=lineFeatures
                    #    np.append(features,lineFeatures,axis=1)
                    #parse open rates according to the 10 bins into labels array
                    if(0 < openRate <= 0.1):
                        labels[lineCount-1]=[1,0,0,0,0,0,0,0,0,0]
                    #    np.append(labels,np.array(),axis=1)
                    elif(0.1 < openRate <= 0.2):
                        labels[lineCount-1]=[0,1,0,0,0,0,0,0,0,0]
                        #np.append(labels,np.array([0,1,0,0,0,0,0,0,0,0]),axis=1)
                    elif(0.2 < openRate <= 0.3):
                        labels[lineCount-1]=[0,0,1,0,0,0,0,0,0,0]
                    #    np.append(labels,np.array([0,0,1,0,0,0,0,0,0,0]),axis=1)
                    elif(0.3 < openRate <= 0.4):
                        labels[lineCount-1]=[0,0,0,1,0,0,0,0,0,0]
                    #    np.append(labels,np.array([0,0,0,1,0,0,0,0,0,0]),axis=1)
                    elif(0.4 < openRate <= 0.5):
                        labels[lineCount-1]=[0,0,0,0,1,0,0,0,0,0]
                    #    np.append(labels,np.array([0,0,0,0,1,0,0,0,0,0]),axis=1)
                    elif(0.5 < openRate <= 0.6):
                        labels[lineCount-1]=[0,0,0,0,0,1,0,0,0,0]
                    #    np.append(labels,np.array([0,0,0,0,0,1,0,0,0,0]),axis=1)
                    elif(0.6 < openRate <= 0.7):
                        labels[lineCount-1]=[0,0,0,0,0,0,1,0,0,0]
                    #    labels.append(np.array([0,0,0,0,0,0,1,0,0,0]),axis=1)
                    elif(0.7 < openRate <= 0.8):
                        labels[lineCount-1]=[0,0,0,0,0,0,0,1,0,0]
                    #    labels.append(np.array([0,0,0,0,0,0,0,1,0,0]),axis=1)
                    elif(0.8 < openRate <= 0.9):
                        labels[lineCount-1]=[0,0,0,0,0,0,0,0,1,0]
                    #    labels.append(np.array([0,0,0,0,0,0,0,0,1,0]),axis=1)
                    elif(0.9 < openRate <= 1):
                        labels[lineCount-1]=[0,0,0,0,0,0,0,0,0,1]
                    #    labels.append(np.array([0,0,0,0,0,0,0,0,0,1]),axis=1)
                    print subject
                    print openRate
                    print lineFeatures
                    print labels[lineCount-1]
                if(lineCount==3):
                    break
                lineCount+=1

        features_placeholder = tf.placeholder(features.dtype,features.shape)
        labels_placeholder = tf.placeholder(labels.dtype,labels.shape)

        dataset = tf.data.Dataset.from_tensor_slices((features_placeholder,labels_placeholder))
        return dataset

    data = createDataset("../input/corrected.csv","dictionary2.txt")
'''
