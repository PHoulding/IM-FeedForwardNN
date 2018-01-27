import numpy as np

with open('preprocessed.txt','r') as f:
    for i,l in enumerate(f):
        pass
    numInputs=i
feature_sets=[]
with open('preprocessed.txt',buffering=20000) as f:
    for numLine,line in enumerate(f):
        if(numLine>int(numInputs*0.8)):
            feature_sets.append(line)
#            print "HERE"
print len(feature_sets)
npfeatures = np.array(feature_sets)
