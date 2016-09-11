import sys
import random

from .agent import Agent

class Dummy(Agent):

    def __init__(self, seed, port):
        super(Dummy, self).__init__(seed, port)


    def select_action(self,state, stateFeatures):
        """ When this method is called, the agent executes an action. """
        if state[5] == 1: # State[5] is 1 when the player can kick the ball
            #return random.choice([SHOOT, PASS(team_mate), DRIBBLE])
            return random.choice([self.DRIBBLE, self.SHOOT, self.PASSfar, self.PASSnear])
        return self.MOVE

    def observe_reward(self,state,action,reward,statePrime):
        """ After executing an action, the agent is informed about the state-reward-state tuple """
        pass

    def step(self, state, action):
        """ Perform a training step """
        #Execute the action in the environment
        self.execute_action(action)
        # Advance the environment and get the game status
        status = self.hfo.step()
        statePrime = self.get_transformed_features(self.hfo.getState())
        reward = self.get_reward(status)
        actionPrime = self.select_action(statePrime, statePrime)
        return status, statePrime, actionPrime
