# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 16:36:47 2016

@author: Felipe Leno
Loads everything from adhoc.py, this class only defines parameters for the Q-based
advising
"""
from adhoc import AdHoc
import math
class AdHocTD(AdHoc):
        #Enum for importance metrics
    VISIT_IMPORTANCE, Q_IMPORTANCE = range(2)
    
    def __init__(self, budgetAsk=100, budgetAdvise=100,stateImportanceMetric=Q_IMPORTANCE, epsilon=0.1, alpha=0.1, gamma=0.9, decayRate=0.9):
        super(AdHocTD, self).__init__(budgetAsk,budgetAdvise,stateImportanceMetric)
    
    def midpoint(self,typeMid):
        """Calculates the midpoint"""     
        if typeMid == self.ADVISE:
           numVisits = 100
           impMid = numVisits / (numVisits + math.log(self.scalingVisits + numVisits))
           return impMid * 1.1
        elif typeMid == self.ASK:
            numVisits = 10
            impMid = numVisits / (numVisits + math.log(self.scalingVisits + numVisits))
            return impMid
            
        #Error
        return None