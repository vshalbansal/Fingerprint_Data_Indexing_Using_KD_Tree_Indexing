#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 10:11:58 2022

@author: vishal
"""


import IndexVectorGenerator
import KDTreeIndexing as kdt
import pickle
from progressbar import ProgressBar
pbar = ProgressBar()


trainDataPath = "./FVC2000/train" # path to directory containing training set of fingerprint databases. Inside the datapath directory the file structure should be "database_id/fingerprint_image.tif"



#%%
# generate index vectors for the dataset
indxVecGen = IndexVectorGenerator.indexVectorGenerator()
indexVectorDataset = indxVecGen.genIndexFeature(trainDataPath)

#%%

#%%

# dump the generated index vector dataset into a pickle file
with open('featureVector_FVC2000_pickle', 'wb') as file:
    pickle.dump(indexVectorDataset, file, protocol=pickle.HIGHEST_PROTOCOL)
    
    
#%%%
# load pickle file
with open('featureVector_FVC2000_pickle','rb') as file:
    indexVectorDataset = pickle.load(file)
file.close()

#%%
# create kd Tree index for the index Vector dataset

binSize1, binSize2, binSize3 = 50, 10, 10 # define binSize1, binSize2, binSize3
indexRoot = kdt.genKDTree(indexVectorDataset, binSize1, binSize2, binSize3) 




#%%
#testing the indexing scheme

# generate index vector for the test dataset 
testDataPath = "./FVC2000/test"
testIndexVector = indxVecGen.genIndexFeature(testDataPath)

# searching for a specific fingerprint in the kd tree
searchDbID = "DB1_B"
searchFP = "101_1"


searchResult = [] # search result will contain a list of matched fingerprint id and feature vector associated with it
import math
for k in testIndexVector[searchDbID][searchFP]:
    indexKey = [k[0], math.floor(k[1]*50), math.floor(k[2]*10), math.floor(k[3]*10) ]
    searchResult.append(kdt.search(indexRoot, indexKey))

