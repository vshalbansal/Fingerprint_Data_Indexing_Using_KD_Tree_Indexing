#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 09:09:20 2022

@author: vishal
"""

import math
class kdTreeNode:
    def __init__(self,indexKey,featureVec,fpId):
        self.low = None
        self.high = None 
        self.disc = 0  #discrimination axis
        self.indexKey = indexKey
        self._members = [[fpId,featureVec]]
        
        
def checkEquality(root,indexKey):
    if(root.indexKey==indexKey):
        return True
    else:
        return False
            
def kdTreeInsert(root, indexKey,featureVec, fpId,prevdisc):
    if(root is None):
        root = kdTreeNode(indexKey,featureVec, fpId)
        root.disc = (prevdisc+1)%4
        return root
    else:
        isEqual = checkEquality(root, indexKey)
        if(isEqual==True):
            root._members.append([fpId,featureVec])
            return root
        else:
            if(root.indexKey[root.disc]<=indexKey[root.disc]):
                root.high = kdTreeInsert(root.high, indexKey,featureVec, fpId,root.disc)
            else:
                root.low = kdTreeInsert(root.low, indexKey,featureVec, fpId,root.disc)
        return root


def search(root,indexKey):
    if(root is None):
        return []
    else:
        isEqual = checkEquality(root, indexKey)
        if(isEqual==True):
            return root._members
        else:
            if(root.indexKey[root.disc]<=indexKey[root.disc]):
                return search(root.high, indexKey)
            else:
                return search(root.low, indexKey)
    
    
    

def genKDTree(dataset, binSize1, binSize2, binSize3):
    root = None
    for i in dataset.keys():
        for j in dataset[i].keys():
            for k in dataset[i][j]:
                indexKey = [k[0], math.floor(k[1]*binSize1), math.floor(k[2]*binSize2), math.floor(k[3]*binSize3) ]
                fpId = (i,j)
                root = kdTreeInsert(root,indexKey, k, fpId, -1)    
    return root