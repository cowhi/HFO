import random


class SARSA(object):

    lastState = None

    def __init__(self, hfo, epsilon=0.1, alpha=0.2, gamma=0.9):
        super(SARSA, self).__init__(hfo)
        self.qTable = {}

        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma


    def get_Q(self, state, action):
        return self.qTable.get((state, action), 0.0)

    def learn_Q(self, state, action, reward, value):
        oldv = self.qTable.get((state, action), None)
        if oldv is None:
            self.qTable[(state, action)] = reward
        else:
            self.qTable[(state, action)] = oldv + self.alpha * (value - oldv)


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


    def select_action(self, state):
        """Executes the epsilon-greedy exploration strategy"""
        #Processes the state using cmac
        state = self.transformFeatures(state)
        #stores last CMAC result
        self.lastState = state

        if self.exploring and random.random() < self.epsilon:
            action = random.choice(self.actions)
        else:
            qValues = [self.get_Q(state, a) for a in self.actions]
            maxQ = max(qValues)
            count = qValues.count(maxQ)
            if count > 1:
                best = [i for i in range(len(self.actions)) if qValues[i] == maxQ]
                i = random.choice(best)
            else:
                i = qValues.index(maxQ)

            action = self.actions[i]
        return action

    def learn(self, state1, action1, reward, state2, action2):
        qnext = self.get_Q(state2, action2)
        self.learn_Q(state1, action1, reward, reward + self.gamma * qnext)
