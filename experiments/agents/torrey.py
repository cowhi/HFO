# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 19:07:33 2016

@author: Felipe Leno
Torrey & Taylor importance Advising implementation
"""

from sarsa import SARSA
from threading import Thread
import advice_util as advice
import math
import agent


class Torrey(SARSA):
    
    budget = 0
    spentBudget = 0
    lastStatus = agent.IN_GAME
    
    def __init__(self, budget=100,threshold = 0.01,seed=12345, port=12345):
        super(Torrey, self).__init__(seed=seed,port=port)
        self.name = "Torrey"
        
        self.budget = budget
        self.threshold = threshold
       
        thread = Thread(target = self.advise)
        thread.start()
        
    def step(self, state, action):
        """Modifies the default step action just to include a state visit counter"""
        status, statePrime, actionPrime = super(Torrey, self).step(state,action)
        self.lastStatus = status
        return status, statePrime, actionPrime        
    
    def select_action(self, stateFeatures, state):
        """Changes the exploration strategy"""
        if self.exploring and stateFeatures[self.ABLE_KICK] == 1:
            #Ask for advice
            advised = advice.ask_advice(self.get_Unum(),stateFeatures)
            if advised:
                action = self.combineAdvice(advised)
                return action
                    
        return super(Torrey, self).select_action(stateFeatures,state)
        
    def combineAdvice(self,advised):
        return int(max(set(advised), key=advised.count))  
        
    def advise(self):
        """Method executed in a parallel thread.
        The agent checks if there is another friendly agent asking for advice,
        and helps him if possible"""
        while self.spentBudget < self.budget and not self.lastStatus == self.SERVER_DOWN:
            if self.exploring:            
                reads = advice.verify_advice(self.get_Unum())            
                
                #Is there anyone asking for advice?
                if reads:
                    for ad in reads:
                        advisee = ad[0]    
                        if ad[1] != "":
                            stateFeatures = advice.recover_state(ad[1])
                            #Check if the agent should advise
                            advise,advisedAction = self.check_advise(stateFeatures,self.get_transformed_features(stateFeatures))
                            if advise:
                                advice.give_advice(int(advisee),self.get_Unum(),advisedAction)
                                self.spentBudget = self.spentBudget + 1
                                #print "ADVISED***"
                                
    def check_advise(self,stateFeatures,state): 
        """Returns if the agent should advice in this state.
        The advised action is also returned in the positive case"""
            
        
        importance = self.state_importance(state)
        #if importance>0:
        #print "Importance "+str(importance) 
        if importance > self.threshold:
            advisedAction = self.select_action(stateFeatures,state)
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
        if(maxQ==-float('Inf') or minQ==float('Inf')):
            return 0

        qImportance = math.fabs(maxQ - minQ) 
        
        return qImportance        

    def get_used_budget(self):
        """Returns the ask budget the agent already used"""
        return self.spentBudget