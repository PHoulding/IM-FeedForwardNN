import numpy as np

#test = np.array(100)
with open('preprocessed.txt','r') as f:
    for i,l in enumerate(f):
        print i,l.split(":::")[0],l.split(":::")[1],l.split(":::")[2][:-2]
#print test
#
