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
from advice_util import ask_advice,verify_advice,give_advice

from agent import Agent


class DummyCom(Agent):

   
    steps = 0


    def __init__(self):
        super(DummyCom, self).__init__()



    def select_action(self,state):
        """ When this method is called, the agent executes an action. """
        if self.exploring:
            advised = ask_advice(self.get_Unum(),state)
            if advised:
                print "ADVISED: "+advised

            reads = verify_advice(self.get_Unum())            

            if reads:
                print reads
                for ad in reads:
                    advisee = ad[0]
                    state = ad[1]
                    give_advice(advisee,self.get_Unum(),self.MOVE)
            

            self.steps = self.steps+1


        if state[5] == 1: # State[5] is 1 when the player can kick the ball
            #return random.choice([SHOOT, PASS(team_mate), DRIBBLE])
            return random.choice([self.DRIBBLE, self.SHOOT])
        return self.MOVE


    def observe_reward(self,state,action,reward,statePrime):
        """ After executing an action, the agent is informed about the state-reward-state tuple """
        pass
    
    def say(self,message):
        """ The say method stores the message in a file named by the agent's Unum"""
        #The last message is overwritten
        fileSay = open(self.messageFolder+str(self.hfo.get_Unum()), 'w+')
        fileSay.write(message)
        fileSay.close()

    def hear(self):
        """This implementation reads the directory and return all messages"""
        messages = []
        import os
        for fileD in os.listdir(self.messageFolder):
            if(fileD != str(self.hfo.get_Unum())):
                fileR = open(self.messageFolder+fileD)
                line = fileR.readline()
                messages.append(line)
        return messages
        
    def step(self, state, action):
        """ Perform a training step """
        #Execute the action in the environment
        self.execute_action(action)
        # Advance the environment and get the game status
        status = self.hfo.step()
        statePrime = self.get_transformed_features(self.hfo.getState())
        
        actionPrime = self.select_action(statePrime)
        return status, statePrime, actionPrime

   
