# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 14:15:56 2016
AdHocVisit Implementation
@author: Felipe Leno
"""
from adhoc import AdHoc
import math
import random
class AdHocVisit(AdHoc):
    
    def __init__(self,agentIndex,alpha=0.2,gamma=0.9,T=0.4,budgetAsk = 500,budgetAdv = 500):
         super(AdHocVisit, self).__init__(agentIndex,alpha=alpha,gamma=gamma,T=T,budgetAsk = budgetAsk, budgetAdv = budgetAdv)

    
    def check_advise(self,state): 
        """Returns if the agent should advice in this state.
        The advised action is also returned in the positive case"""
            
        
        numberVisits = self.visitedNumber.get(state,0)
         
        
        if numberVisits == 0:
            return False,None
        
        #param = 0.2  #-> Experiments Action and NoAction
        param = 0.15
        #param = 1.5
        #Calculates the probability
        prob = 1 - math.pow((1 + param),-math.log(numberVisits,2))#math.sqrt(numberVisits))#
        ##
        #processedState = self.quantize_features(state)
        #numberVisits = self.number_visits(processedState)
        #if importance>0:        
            #print str(importance)+"  -  "+str(prob)
        ##
        #Check if the agent should advise
        if random.random() < prob: #and prob > 0.1:
            advisedAction = self.action(state,True)
            #print "Advised: prob:"+str(prob)+" visits: "+str(numberVisits)
            return True,advisedAction          
            
        return False,None
        
    def check_ask(self,state):
        """Returns if the agent should ask for advise in this state"""
        
        if self.exploring and self.spentBudgetAsk < self.budgetAsk and not (state in self.advisedState):
            
            numberVisits = self.visitedNumber.get(state,0)
            if numberVisits == 0:
                return True
            
            param = 0.4
            #Calculates the probability
            prob =  math.pow((1 + param),-math.sqrt(numberVisits))
            
            ##
            #processedState = self.quantize_features(state)
            #numberVisits = self.number_visits(processedState)
            #print str(numberVisits)+"  -  "+str(prob)
            ##
            
            if random.random() < prob: #and prob > 0.1:
                #print "Asked: prob:"+str(prob)+" visits: "+str(numberVisits)
                return True
        return False