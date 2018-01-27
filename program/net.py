import tensorflow as tf
import numpy as np
import re
import string
from dictionary import Dictionary

'''
The Neural Network file is used to do all the math used in the actual model.
The network consists of six total layers
    - One input layer
    - Four hidden layers
    - One output layer
The input layer consists of the number of nodes which equals the total unique words used in the dataset
Each hidden layer consists of 1500 nodes
The output layer contains 11 nodes which represent
    - 0%
    - 1-10%
    - 11-20%
    ...
    -91-100%
'''
class NeuralNetwork():
    def __init__(self):
        self.n_nodes_hl1=1500
        self.n_nodes_hl2=1500
        self.n_nodes_hl3=1500
        self.n_nodes_hl4=1500
        self.n_classes=11
        self.batch_size=10
        #This gets the number of inputs to be used in calculating batches
        with open('preprocessed.txt','r') as f:
            for i,l in enumerate(f):
                pass
            numInputs=i
        #This gets the number of words in the dictionary
        with open('dictionary.txt','r') as f:
            for i,l in enumerate(f):
                pass
            dictLength=i
        #Set the total batches for output
        self.total_batches=int((numInputs*0.9)/self.batch_size)
        #Set the number of Epochs here
        self.hm_epochs=2

        self.x=tf.placeholder('float')
        self.y=tf.placeholder('float')

        #Define the hidden layer parameters
        self.hidden_1_layer={'f_fum':self.n_nodes_hl1,\
                        'weight':tf.Variable(tf.random_normal([dictLength+1,self.n_nodes_hl1])),\
                        'bias':tf.Variable(tf.random_normal([self.n_nodes_hl1]))}
        self.hidden_2_layer={'f_fum':self.n_nodes_hl2,\
                        'weight':tf.Variable(tf.random_normal([self.n_nodes_hl1,self.n_nodes_hl2])),\
                        'bias':tf.Variable(tf.random_normal([self.n_nodes_hl2]))}
        self.hidden_3_layer={'f_fum':self.n_nodes_hl3,\
                        'weight':tf.Variable(tf.random_normal([self.n_nodes_hl2,self.n_nodes_hl3])),\
                        'bias':tf.Variable(tf.random_normal([self.n_nodes_hl3]))}
        self.hidden_4_layer={'f_fum':self.n_nodes_hl4,\
                        'weight':tf.Variable(tf.random_normal([self.n_nodes_hl3,self.n_nodes_hl4])),\
                        'bias':tf.Variable(tf.random_normal([self.n_nodes_hl4]))}
        self.output_layer={'f_fum':None,\
                        'weight':tf.Variable(tf.random_normal([self.n_nodes_hl4,self.n_classes])),\
                        'bias':tf.Variable(tf.random_normal([self.n_classes]))}
        #Set the saver (for resuming a specific model)
        self.saver = tf.train.Saver()
        self.tf_log = 'tf.log'

    '''
        This function handles all the math used at the nodes.
        - Uses ReLU activation after mutliplying the node values by the weights, and adding the biases
            y=mx+b
                - m=weights
                - b=bias
        This simulates forward propagation
    '''
    def neural_network_model(self,data):
        l1 = tf.add(tf.matmul(data,self.hidden_1_layer['weight']),self.hidden_1_layer['bias'])
        l1 = tf.nn.relu(l1)
        l2 = tf.add(tf.matmul(l1,self.hidden_2_layer['weight']),self.hidden_2_layer['bias'])
        l2 = tf.nn.relu(l2)
        l3 = tf.add(tf.matmul(l2,self.hidden_3_layer['weight']),self.hidden_3_layer['bias'])
        l3 = tf.nn.relu(l3)
        l4 = tf.add(tf.matmul(l3,self.hidden_4_layer['weight']),self.hidden_4_layer['bias'])
        l4 = tf.nn.relu(l4)
        output = tf.matmul(l4,self.output_layer['weight']+self.output_layer['bias'])
        return output

    '''
        Creates the input array for a specific subject line depending on the indices of the words in the dictionary
        These are denoted as "features"
    '''
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
            #Adds personalization variables
            if("##" in word):
                if("name" in word):
                    features[1]=1
                features[0]=1
    #        features[2]=len(subjectLine)
        return features
    '''
    Creates the label for the specific subject line, depending on the open rate
    '''
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
    '''
    - Handles the training of the Neural Network model
    - Uses softmax cross entropy with logits as it's output comparrison/cost function
    - Adam Optimization was used due to it being computationally efficient
    '''
    def train_neural_network(self):
        prediction = self.neural_network_model(self.x)
        #set the cost and optimization variables
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction,labels=self.y))
        optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(cost)
        with open('preprocessed.txt','r') as f:
            for i,l in enumerate(f):
                pass
            numInputs=i
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            #Tries to restore previous session if needed
            try:
                epoch = int(open(self.tf_log,'r').read().split('\n')[-2])+1
                print("Starting:",epoch)
            except:
                epoch=1
            #Runs while the current epoch is less than or equal to the maximum epochs
            while epoch<=self.hm_epochs:
                if(epoch!=1):
                    self.saver.restore(sess,"./model.ckpt")
                epoch_loss=1
                #Load dictionary
                with open('trainData.txt',buffering=20000) as f:
                    batch_x=[]
                    batch_y=[]
                    batches_run=0
                    #Runs through the trainData.txt file
                    for numLine,line in enumerate(f):
                        #Sets subject and openRate depending on the split
                        subject=line.split(':::')[0]
                        openRate=line.split(':::')[1]
                        #Generate bag of words for subject
                        features=self.createBagOfWords(subject)
                        #Generate label for open rate
                        label=self.createLabel(float(openRate))
                        line_x = features
                        line_y = label
                        #appends both to the batch
                        batch_x.append(line_x)
                        batch_y.append(line_y)
                        if(len(batch_x)>=self.batch_size):
                            #Runs the optimization function
                            _, c =sess.run([optimizer,cost],feed_dict={self.x:np.array(batch_x),self.y:np.array(batch_y)})
                            #Dumps information to a text file
                            with open("dump.txt","a+") as dumpF:
                                dumpF.write(str(batch_x)+"\r\n")
                            epoch_loss+=c
                            batch_x=[]
                            batch_y=[]
                            batches_run+=1
                            #Prints the values for the current batch run
                            print 'Batch run:',batches_run,'/',self.total_batches,'| epoch:',epoch,'| Batch loss:',c
                #Saves the current session to checkpoint files
                self.saver.save(sess,"./model.ckpt")
                #Outputs the final values
                print 'Epoch',epoch,'completed out of',self.hm_epochs,'total loss:',epoch_loss,'avg loss',epoch_loss/self.total_batches
                #Writes the last epoch completed to the log file
                with open(self.tf_log,'a') as f:
                    f.write(str(epoch)+'\n')
                epoch+=1
    '''
    - Handles the testing of the model
    '''
    def test_neural_network(self):
        prediction=self.neural_network_model(self.x)
        #Loads the checkpoint files to recreate the model from previous training
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            for epoch in range(self.hm_epochs):
                try:
                    self.saver.restore(sess,"./model.ckpt")
                except Exception as e:
                    print str(e)
                epoch_loss=0
            #Sets the variables to check correctness and accuracy
            correct=tf.equal(tf.argmax(prediction,1),tf.argmax(self.y,1))
            accuracy = tf.reduce_mean(tf.cast(correct,'float'))
            feature_sets=[]
            labels=[]
            counter=0
            with open('testData.txt',buffering=20000) as f:
                #Runs through the testData file
                for numLine,line in enumerate(f):
                    try:
                        subject=line.split(':::')[0]
                        openRate=line.split(':::')[1]
                        #Sets the features and label arrays
                        features=self.createBagOfWords(subject)
                        label=self.createLabel(float(openRate))
        #                print float(openRate)
        #                print label
                        feature_sets.append(features)
                        labels.append(label)
                        counter+=1
                    except Exception as e:
                        print str(e)
            print 'Tested',counter,'samples.'
            test_x=np.array(feature_sets)
            test_y=np.array(labels)
        #    print test_y
            #Prints the accuracy depending on the different values
            print 'Accuracy:',accuracy.eval({self.x:test_x,self.y:test_y})
            output = sess.run(prediction,feed_dict={self.x:test_x})
        #    print output
            count=0
            #Writes data to an output file for further inspection
            with open("output.txt","w+") as outF:
                for _ in output:
                    outF.write(str(_)+":::"+str(test_y[count])+"\r\n")
                    count+=1
