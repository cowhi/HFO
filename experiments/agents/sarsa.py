import random
from cmac import CMAC
from .agent import Agent

class SARSA(Agent):

    lastState = None

    def __str__(self):
        """ Overwrites the object.__str__ method.

        Returns:
            string (str): Important parameters of the object.
        """
        return "Agent: " + str(self.unum) + ", " + \
               "Type: " + str(self.name) + ", " + \
               "Training steps: " + str(self.training_steps_total) + ", " + \
               "Q-Table size: " + str(len(self.qTable))

    def __init__(self, epsilon=0.1, alpha=0.1, gamma=0.99):
        super(SARSA, self).__init__()
        self.name = "SARSA"
        self.qTable = {}
        self.stateTrace = {}
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.cmac = CMAC(1,0.1,0.1)

    def quantize_features(self, features):
        """ CMAC utilities for all agent """
        return self.cmac.quantize(features)
        #data = []
        #for feature in features:
        #    quantized_features = self.cmac.quantize(feature)
        #    data.append([quantized_features])
        #return data


    def get_Q(self, state, action):
        return self.qTable.get((state, action), 0.0)

    def observe_reward(self,state,action,reward,statePrime):
        """ After executing an action, the agent is informed about the state-reward-state tuple """
        pass
    '''
    def observe_reward(self,state,action,reward,statePrime):
        """ After executing an action, the agent is informed about the state-action-reward-state tuple """
        if self.exploring:
            #Selects the action for the next state without exploration
            lastState = self.lastState
            self.exploring = False
            nextAction = self.select_action(statePrime)
            #Hereafter the self.lastState refers to statePrime
            #Executes Q-update
            self.learn(lastState,action,reward,self.lastState,nextAction)
            #turns on the exploration again
    '''

    def select_action(self, stateFeatures, state):
        """Executes the epsilon-greedy exploration strategy"""
        #stores last CMAC result
        #self.lastState = state
        # select applicable actions
        if stateFeatures[5] == 1: # State[5] is 1 when the player can kick the ball
            actions = [self.DRIBBLE, self.SHOOT, self.PASSfar, self.PASSnear]
        else:
            actions = [self.MOVE]
        # epsilon greedy action selection
        if self.exploring and random.random() < self.epsilon:
            return random.choice(actions)
        else:
            cmacState = self.quantize_features(state)
            qValues = [self.get_Q(tuple(cmacState), action) for action in actions]
            maxQ = max(qValues)
            count = qValues.count(maxQ)
            if count > 1:
                best = [i for i in range(len(actions)) if qValues[i] == maxQ]
                return self.actions[random.choice(best)]
            else:
                return self.actions[qValues.index(maxQ)]


    def learn(self, state1, action1, reward, state2, action2):
        qnext = self.get_Q(state2, action2)
        self.learn_Q(state1, action1, reward, reward + self.gamma * qnext)

    def learn_Q(self, state, action, reward, value):
        oldv = self.qTable.get((state, action), None)
        if oldv is None:
            self.qTable[(state, action)] = reward
        else:
            self.qTable[(state, action)] = oldv + self.alpha * (value - oldv)

    def step(self, state, action):
        """ Perform a complete training step """
        # perform action and observe reward & statePrime
        self.execute_action(action)
        status = self.hfo.step()
        stateFeatures = self.hfo.getState()
        statePrime = self.get_transformed_features(stateFeatures)
        reward = self.get_reward(status)
        # select actionPrime
        actionPrime = self.select_action(tuple(stateFeatures), statePrime)
        # calculate TDError
        #TDError = reward + self.gamma * self.get_Q(statePrime, actionPrime) - self.get_Q(state, action)
        # update eligibility trace Function for state and action
        # update update ALL Q values and eligibility trace values
        # ???
        if self.exploring:
            self.learn(tuple(self.quantize_features(state)), action, reward,
                       tuple(self.quantize_features(statePrime)), actionPrime)
            self.training_steps_total += 1
        return status, statePrime, actionPrime
