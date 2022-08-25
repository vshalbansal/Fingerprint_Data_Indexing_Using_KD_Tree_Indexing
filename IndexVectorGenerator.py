#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 10:11:58 2022

@author: vishal
"""

import numpy as np
import cv2 as cv
import os
import FingerprintFeatureExtractor as FFE
from FingerprintImageEnhancer import FingerprintImageEnhancer
import TriangleFeatureGenerator as tfg
from skimage.filters.rank import entropy
from skimage.morphology import disk
from skimage.filters import threshold_otsu


from progressbar import ProgressBar
pbar = ProgressBar()



class indexVectorGenerator(object):
    def __init__(self):
        self._inputImgPath = [] # each entry is a list of three attributes namely database_id, fingerprint_id and file path
        self._featureDict = {}
        self.datapath = None
    
    def loadImages(self):
        for i in os.listdir(self.datapath):
            dbId = i
            dbPath = os.path.join(self.datapath,i)
            for j in os.listdir(dbPath):
                if j.endswith(".tif"):
                    imgPath = os.path.join(dbPath,j)
                    fpId = j.strip(".tif") # capture fingerprint id from filename
                    self._inputImgPath.append([dbId,fpId,imgPath])


    def getBoundaryMask(self,enhancedImg):
        entropy_img = entropy(enhancedImg,disk(10))
        thresh_otsu = threshold_otsu(entropy_img)
        binarized_img = entropy_img>=thresh_otsu
        binarized_img = np.array(binarized_img,dtype=np.ubyte)
        kernel = np.ones((5,5), np.uint8)
        img_erosion = cv.erode(binarized_img, kernel, iterations=8)
        boundaryFilterMask = np.array(img_erosion,dtype=bool)
        return boundaryFilterMask
    
    def genIndexFeature(self,datapath):
        
        self.datapath = datapath
        self.loadImages()
        for i in pbar(self._inputImgPath):
            inputImg = cv.imread(i[2],0)
            dbId = i[0]
            if dbId not in self._featureDict:
                self._featureDict[dbId] = {}
            fpId = i[1]
            image_enhancer = FingerprintImageEnhancer()
            enhancedImg = image_enhancer.enhance(inputImg)
            enhancedImg = np.ubyte(enhancedImg)
            enhancedImg = enhancedImg*254
            
            FeaturesTerminations, FeaturesBifurcations = FFE.extract_minutiae_features(enhancedImg, False)
            
            
            boundaryFilterMask = self.getBoundaryMask(enhancedImg)
            
            # create minutiae coordinate set only for the points which are not filtered out using boundary filter mask
            coordinateSet = []
            for i in FeaturesTerminations:
                if(boundaryFilterMask[i.locX][i.locY] == True):
                    coordinateSet.append([i.locX,i.locY,0]) # 0 is to indicate that this minutiae point is of termination type
            for i in FeaturesBifurcations:
                if(boundaryFilterMask[i.locX][i.locY] == True):
                    coordinateSet.append([i.locX,i.locY,1]) # 1 indicates that this minutiae point is of bifurcation type
            coordinateSet = np.array(coordinateSet)
            
            delaunayTri = tfg.getDelaunayTriangulation(coordinateSet[:,0:2])

            for j in delaunayTri.simplices:
                
                pointA,pointB,pointC = coordinateSet[j[0]],coordinateSet[j[1]],coordinateSet[j[2]]
                sideC, sideA, sideB = tfg.getTriSideLen(pointA[0:2], pointB[0:2], pointC[0:2])
                angleA, angleB, angleC = tfg.getTriAngles(sideC, sideA, sideB)
                incircleRadius = tfg.getRadiusIncircle(sideC, sideA, sideB)
                circumcircleRadius = tfg.getRadiusCircumcircle(sideC, sideA, sideB)
                
                
                angleTypeList = []
                angleTypeList.append([angleA,pointA[2]])
                angleTypeList.append([angleB,pointB[2]])
                angleTypeList.append([angleC,pointC[2]])
                angleTypeList = sorted(angleTypeList, key=lambda x:x[0])
                triSides = [sideC, sideA, sideB]
                triSides.sort()
                triClass = angleTypeList[0][1]*1 + angleTypeList[1][1]*2 + angleTypeList[2][1]*4 #triangle class 
                
                indxFeatureVec = []
                indxFeatureVec.append(triClass)
                indxFeatureVec.append(incircleRadius/circumcircleRadius)
                indxFeatureVec.append(angleTypeList[1][0]/angleTypeList[2][0])
                indxFeatureVec.append(triSides[1]/triSides[2])
                
                if fpId not in self._featureDict[dbId]:
                    self._featureDict[dbId][fpId] = []
                self._featureDict[dbId][fpId].append(indxFeatureVec)
        return self._featureDict
                

