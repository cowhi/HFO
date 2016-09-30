# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 19:07:33 2016

@author: Felipe Leno
Torrey & Taylor importance Advising implementation
"""

from sarsatile import SARSATile
from advice_util import AdviceUtil
import math
import agent


class Torrey(SARSATile):
    
    budget = 0
    spentBudget = 0
    lastStatus = agent.IN_GAME
    adviceObject = None
    advisedState = None
    
    def __init__(self, budget=1000,threshold = 0.01,seed=12345, port=12345, serverPath = "/home/leno/HFO/bin/"):
        super(Torrey, self).__init__(seed=seed,port=port,serverPath=serverPath)
        self.name = "Torrey"
        self.advisedState = {}
        self.budget = budget
        self.threshold = threshold
       
        
    def step(self, state, action):
        """Modifies the default step action just to include a state visit counter"""
        status, statePrime, actionPrime = super(Torrey, self).step(state,action)
        self.lastStatus = status
        if self.lastStatus != self.IN_GAME:
            self.advisedState = {}
        return status, statePrime, actionPrime        
    
    def select_action(self, stateFeatures, state, noAdvice = False):
        """Changes the exploration strategy"""
        if self.exploring and stateFeatures[self.ABLE_KICK] == 1 and not noAdvice and not (self.quantize_features(state) in self.advisedState):
            #Ask for advice
            advised = self.adviceObject.ask_advice(self.get_Unum(),stateFeatures)
            if advised:
                    try:
                        self.advisedState[state] = True
                        action = self.combineAdvice(advised)
                        return action
                    except:
                        print "Exception when combining the advice " + str(advised)
                    
        return super(Torrey, self).select_action(stateFeatures,state)
        
    def combineAdvice(self,advised):
        return int(max(set(advised), key=advised.count)) 
        
    def advise_action(self,uNum,state):
        """Verifies if the agent can advice a friend, and return the action if possible"""
        if self.spentBudget < self.budget:
            #Check if the agent should advise
            advise,advisedAction = self.check_advise(state,self.get_transformed_features(state))
            if advise:
                 self.spentBudget = self.spentBudget + 1
                 return advisedAction
        return None    
        
   
                                
    def check_advise(self,stateFeatures,state): 
        """Returns if the agent should advice in this state.
        The advised action is also returned in the positive case"""
            
        
        importance = self.state_importance(state)
        #if importance>0:
        #print "Importance "+str(importance) 
        if importance > self.threshold:
            advisedAction = self.select_action(stateFeatures,state,True)
            return True,advisedAction          
            
        return False,None
        
    def state_importance(self,state):
        """Calculates the state importance
        state - the state
        typeProb - is the state importance being calculated in regard to
        the number of visits or also by Q-table values?"""
        processedState = self.quantize_features(state)
        
        
        maxQ = -float("inf")
        minQ = float("inf")
        #Get max and min Q value
        actions = [self.DRIBBLE, self.SHOOT, self.PASSfar, self.PASSnear]
        for act in actions:
            if (processedState,act) in self.qTable:
                actQ = self.qTable.get((processedState, act))
                if actQ > maxQ:
                    maxQ = actQ
                if actQ < minQ:
                    minQ = actQ
        
        #print "MaxQ "+str(maxQ)+"   - MinQ "+str(minQ)
        #print "MinQ "+str(minQ)
        # print "len "+str(len(actions))
        if(minQ==float('Inf')):
            return 0

        qImportance = math.fabs(maxQ - minQ) 
        
        return qImportance        

    def get_used_budget(self):
        """Returns the ask budget the agent already used"""
        return self.spentBudget
        
        
    def setupAdvising(self,agentIndex,allAgents):
        """ This method is called in preparation for advising """
        self.adviceObject = AdviceUtil()
        #Get the next agent
        index = (agentIndex+1)%len(allAgents)
        advisors = [allAgents[index]]
        self.adviceObject.setupAdvisors(advisors)