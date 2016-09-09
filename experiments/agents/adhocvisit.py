# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 16:36:47 2016

@author: Felipe Leno
Loads everything from adhoc.py, this class only defines parameters for the visit-based
ad hoc advising
"""
from adhoc import AdHoc

class AdHocVisit(AdHoc):
        #Enum for importance metrics
    VISIT_IMPORTANCE, Q_IMPORTANCE = range(2)
    
    def __init__(self, budgetAsk=100, budgetAdvise=100,stateImportanceMetric=VISIT_IMPORTANCE, epsilon=0.1, alpha=0.1, gamma=0.9, decayRate=0.9):
        super(AdHocVisit, self).__init__(budgetAsk,budgetAdvise,stateImportanceMetric)
        
        
