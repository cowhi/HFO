# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 09:21:38 2016

@author: Felipe Leno

This file implements our advisor-advisee proposal.

This agent act as SARSA, and the exploration strategy is changed according to our proposal
"""

from sarsa import SARSA
from threading import Thread
import advice_util as advice

import math


class AdHoc(SARSA):
    
    budgetAsk = 0
    budgetAdvise = 0
    spentBudgetAsk = 0
    spentBudgetAdvise = 0
    
    #These two variables are used to control the advising thread
    ableToAdvise = False
    quitAdvising = False
    
    #Enum for importance metrics
    VISIT_IMPORTANCE, Q_IMPORTANCE = range(2)
    
    stateImportanceMetric = None
    
    ASK,ADVISE = range(2)
    visitTable = None
    
    def __init__(self, budgetAsk=0, budgetAdvise=0,stateImportanceMetric=VISIT_IMPORTANCE, epsilon=0.1, alpha=0.2, gamma=0.9):
        super(AdHoc, self).__init__()
        self.name = "AdHoc"
        self.qTable = {}
        self.budgetAsk = budgetAsk
        self.budgetAdvise = budgetAdvise
        
        thread = Thread(target = self.advise)
        thread.start()
        self.ableToAdvise = True
        self.stateImportanceMetric = stateImportanceMetric
        
    def select_action(self, state):
        """Changes the exploration strategy"""
        if self.exploring and self.spentBudgetAsk < self.spentBudgetAsk:
            #Check if it should ask for advice
            ask = self.check_ask(state)
            if ask:
                #Ask for advice
                advised = advice.ask_advice(self.get_Unum(),state)
                if advised:
                    self.spentBudgetAsk = self.spentBudgetAsk + 1
                    action = self.combineAdvice()
                    return action
                    
        return super.select_action(state)
        
    def check_advise(self,state): 
        """Returns if the agent should advice in this state.
        The advised action is also returned in the positive case"""
            
        
        importance = self.state_importance(state,self.stateImportanceMetric)
        midpoint = self.midpoint(self.ADVISE)
        
        #Calculates the probability
        prob = self.calc_prob_adv(importance,midpoint,self.ADVISE)
        
        #Check if the agent should advise
        if self.random() < prob and prob > 0.1:
            advisedAction = self.select_action(state)
            return True,advisedAction          
            
        return False,None
        
    def state_importance(self,state,typeProb):
        """Calculates the state importance
        state - the state
        typeProb - is the state importance being calculated in regard to
        the number of visits or also by Q-table values?"""
        processedState = tuple(self.quantize_features(state))
        numberVisits = self.number_visits(processedState)
         
        if numberVisits == 0:
            return 0
            
        visitImportance = numberVisits / (numberVisits + math.log(self.scalingVisits + numberVisits))
        
        if typeProb == self.VISIT_IMPORTANCE:
            return visitImportance
        elif typeProb==self.Q_IMPORTANCE:            
            
            maxQ = -float("inf")
            minQ = float("inf")
            #Get max and min Q value
            for act in self.actions:
                actQ = self.qTable.get(processedState,act)
                if actQ > maxQ:
                    maxQ = actQ
                if actQ < minQ:
                    minQ = actQ
             
            qImportance = math.fabs(maxQ - minQ) * len(self.actions.count)
            
            return visitImportance * qImportance        
        #If the agent got here, it is an error
        return None
        
    def step(self, state, action):
        """Modifies the default step action just to include a state visit counter"""
        if self.exploring:
                processedState = tuple(self.quantize_features(state))
                self.visitTable[processedState] = self.visitTable.get(processedState,0.0) + 1
        super.step(state,action)
        
        
    def check_ask(self,state):
        """Returns if the agent should ask for advise in this state"""
        importance = self.state_importance(state,self.VISIT_IMPORTANCE)
        midpoint = self.midpoint(self.ASK)
        
        #Calculates the probability
        prob = self.calc_prob_adv(importance,midpoint,self.ASK)
        
        if self.random() < prob and prob > 0.1:
            return True
        return False
        
        
        #Call default sarsa method if no action was selected
        
    def calc_prob_adv(self,importance,midpoint,typeProb):
        """Calculates the probability of giving/receiving advice
        importance - the current state importance
        midpoint - the midpoint for the logistic function
        typeProb - ASK or ADVISE
        """
        signal = 1 if typeProb == self.ASK else -1
        k = 3        
        
        prob = 1 / (1 + math.exp(signal * k * (importance-midpoint)))
        return prob
        
        
            
    def advise(self):
        """Method executed in a parallel thread.
        The agent checks if there is another friendly agent asking for advice,
        and helps him if possible"""
        while self.spentBudgetAdvise < self.budgetAdvise and not self.quitAdvising:
            if self.exploring:            
                reads = advice.verify_advice(self.get_Unum())            
                
                #Is there anyone asking for advice?
                if reads:
                    for ad in reads:
                        advisee = ad[0]
                        state = advice.recover_state(ad[1])
                        if state != "":
                            #Check if the agent should advise
                            advise,advisedAction = self.check_advise(state)
                            if advise:
                                advice.give_advice(int(advisee),self.get_Unum(),advisedAction)
                                self.spentBudget = self.spentBudget + 1
                    
                    
    def get_used_budget(self):
        return self.spentBudgetAsk
        
      