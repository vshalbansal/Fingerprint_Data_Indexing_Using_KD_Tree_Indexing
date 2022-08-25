#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 18:12:12 2022

@author: vishal
"""

import scipy as sc
import math
from math import pi as pi

# return triangle perimeter
def getTriPerimeter(sideAB,sideBC,sideCA):
    return sideAB+sideBC+sideCA

#return triangle area
def getTriArea(sideAB,sideBC,sideCA):
    perimeter = getTriPerimeter(sideAB,sideBC,sideCA)
    s = perimeter/2
    area = math.sqrt(s*(s-sideAB)*(s-sideBC)*(s-sideCA))
    return area

# Generate delaunay triangulation of the minutiae points
def getDelaunayTriangulation(coordinateSet):    
    delaunayTri = sc.spatial.Delaunay(coordinateSet)
    return delaunayTri


# return the side lengths of the triangle
def getTriSideLen(pointA,pointB,pointC):
    sideAB = math.sqrt((pointA[0]-pointB[0])**2 + (pointA[1]-pointB[1])**2)
    sideBC = math.sqrt((pointB[0]-pointC[0])**2 + (pointB[1]-pointC[1])**2) 
    sideCA = math.sqrt((pointA[0]-pointC[0])**2 + (pointA[1]-pointC[1])**2)
    return sideAB,sideBC,sideCA

# return the angles of the triangle
def getTriAngles(sideAB,sideBC,sideCA):
    
    angleA = math.acos((sideAB**2 + sideCA**2 - sideBC**2)/(2*sideAB*sideCA))
    angleB = math.acos((sideBC**2 + sideAB**2 - sideCA**2)/(2*sideAB*sideBC))
    angleC = math.acos((sideBC**2 + sideCA**2 - sideAB**2)/(2*sideBC*sideCA))   
    return angleA*(180.0/ pi ),angleB*(180.0/ pi ),angleC*(180.0/ pi )

# return the radius of the incircle of the triangle

def getRadiusIncircle(sideAB,sideBC,sideCA):
    perimeter = getTriPerimeter(sideAB,sideBC,sideCA)
    area = getTriArea(sideAB, sideBC, sideCA)
    radius = (area*2)/perimeter
    return radius

#return the radius of the circumcircle of the triangle

def getRadiusCircumcircle(sideAB,sideBC,sideCA):
    area = getTriArea(sideAB, sideBC, sideCA)
    circumRadius = (sideAB*sideBC*sideCA)/(4*area)
    return circumRadius

