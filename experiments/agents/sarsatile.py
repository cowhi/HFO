# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 18:11:16 2016

@author: Felipe Leno
"""
from tilecoding import TileCoding
from sarsa import SARSA
class SARSATile(SARSA):
    
    
   def __init__(self, epsilon=0.1, alpha=0.1, gamma=0.9, decayRate=0.9, seed=12345, port=12345, 
                lowerBoundVariables=-1, upperBoundVariables=+1, tilesNumber=5,tileWidth=0.5,serverPath = "/home/leno/HFO/bin/"):
         super(SARSATile, self).__init__(epsilon=epsilon, alpha=alpha, gamma=gamma, 
            decayRate=decayRate,seed=seed, port=port, serverPath=serverPath)           
         self.cmac = TileCoding(lowerBoundVariables = lowerBoundVariables, 
            upperBoundVariables = upperBoundVariables, tilesNumber = tilesNumber, tileWidth=tileWidth)
            