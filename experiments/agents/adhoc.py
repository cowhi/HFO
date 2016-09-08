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
import numpy as np
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
    
    ASK,ADVISE = range(2)
    
    
    def __init__(self, budgetAsk=0, budgetAdvise=0, epsilon=0.1, alpha=0.2, gamma=0.9):
        super(AdHoc, self).__init__()
        self.budgetAsk = budgetAsk
        self.budgetAdvise = budgetAdvise
        
        thread = Thread(target = self.advise)
        thread.start()
        self.ableToAdvise = True
        
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
        
        # Recovers the informed state to the numpy format
        state = state.split(";")[:-1] #Remove last empty element
        state = np.asfarray(state, dtype='float')
        
        
        importance = self.state_importance(state,self.ADVISE)
        midpoint = self.midpoint(self.ADVISE)
        
        #Calculates the probability
        prob = self.calc_prob_adv(importance,midpoint,self.ADVISE)
        
        #Check if the agent should advise
        if self.random() < prob and prob > 0.1:
            advisedAction = self.select_action(state)
            return True,advisedAction          
            
        return False,None
        
    def check_ask(self,state):
        """Returns if the agent should ask for advise in this state"""
        importance = self.state_importance(state,self.ASK)
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
                    
                    
   
        
      