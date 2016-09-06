# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 14:45:44 2016

@author: Felipe Leno

Test for communicating agents. The hear and say methods provided by HFO
don't work for python agents (at least by the time this experiment is implemented).

This agent communicates through text files. Of course this only works if all agents are executed in the same pc.
TODO: an actual message passing implementation
"""



import random

from agent import Agent

class DummyCom(Agent):

    messageFolder = "messages/"
    steps = 0
    
    
    def __init__(self,hfo):
        super(DummyCom, self).__init__(hfo)
        


    def select_action(self,state):
        """ When this method is called, the agent executes an action. """
        if self.exploring:        
            self.say("Agent "+str(self.hfo.getUnum())+" - Say     "+str(self.steps))
        
            message = self.hear()
            if message:
                print message
            
            self.steps = self.steps+1
        
        
        if state[5] == 1: # State[5] is 1 when the player can kick the ball
            #return random.choice([SHOOT, PASS(team_mate), DRIBBLE])
            return random.choice([self.DRIBBLE, self.SHOOT])
        return self.MOVE


    def observeReward(self,state,reward,statePrime):
        """ After executing an action, the agent is informed about the state-reward-state tuple """
        pass
    
    def say(self,message):
        """ The say method stores the message in a file named by the agent's Unum"""
        #The last message is overwritten        
        fileSay = open(self.messageFolder+str(self.hfo.getUnum()), 'w+')
        fileSay.write(message)        
        fileSay.close()
        
    def hear(self):
        """This implementation reads the directory and return all messages"""
        messages = []
        import os
        for fileD in os.listdir(self.messageFolder):
            if(fileD != str(self.hfo.getUnum())):
                fileR = open(self.messageFolder+fileD)
                line = fileR.readline()
                messages.append(line)
        return messages
            