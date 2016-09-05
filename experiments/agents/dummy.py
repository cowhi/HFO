import sys
import random

from .agent import Agent

class Dummy(Agent):

    def __init__(self):
        super(Dummy, self).__init__()


    def select_action(self,state):
        """ When this method is called, the agent executes an action. """
        if state[5] == 1: # State[5] is 1 when the player can kick the ball
            #return random.choice([SHOOT, PASS(team_mate), DRIBBLE])
            return random.choice([self.DRIBBLE, self.SHOOT])
        return self.MOVE


    def observeReward(self,state,reward,statePrime):
        """ After executing an action, the agent is informed about the state-reward-state tuple """
        pass
