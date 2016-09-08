import logging
from hfo import *

_logger = logging.getLogger(__name__)

import abc

class Agent(object):
    """ This is the base class for all agent implementations.

    """
    __metaclass__ = abc.ABCMeta

    ''' The HFO object '''
    hfo = None
    ''' State discretizations '''
    cmac = None

    ''' An enum of the possible HFO actions
      [Low-Level] Dash(power, relative_direction)
      [Low-Level] Turn(direction)
      [Low-Level] Tackle(direction)
      [Low-Level] Kick(power, direction)
      [Mid-Level] Kick_To(target_x, target_y, speed)
      [Mid-Level] Move(target_x, target_y)
      [Mid-Level] Dribble(target_x, target_y)
      [Mid-Level] Intercept(): Intercept the ball
      [High-Level] Move(): Reposition player according to strategy
      [High-Level] Shoot(): Shoot the ball
      [High-Level] Pass(teammate_unum): Pass to teammate
      [High-Level] Dribble(): Offensive dribble
      [High-Level] Catch(): Catch the ball (Goalie Only)
      NOOP(): Do Nothing
      QUIT(): Quit the game '''
    DASH, TURN, TACKLE, KICK, KICK_TO, MOVE_TO, DRIBBLE_TO, INTERCEPT, \
      MOVE, SHOOT, PASS, DRIBBLE, CATCH, NOOP, QUIT = range(15)

    #Customized actions
    PASSnear = 15
    PASSfar = 16
    #The available actions
    actions = [MOVE, SHOOT, PASSnear, PASSfar, DRIBBLE]

    ''' Possible game status
      [IN_GAME] Game is currently active
      [GOAL] A goal has been scored by the offense
      [CAPTURED_BY_DEFENSE] The defense has captured the ball
      [OUT_OF_BOUNDS] Ball has gone out of bounds
      [OUT_OF_TIME] Trial has ended due to time limit
      [SERVER_DOWN] Server is not alive '''
    IN_GAME, GOAL, CAPTURED_BY_DEFENSE, OUT_OF_BOUNDS, OUT_OF_TIME, \
      SERVER_DOWN = range(6)

    ''' Possible sides '''
    RIGHT, NEUTRAL, LEFT = range(-1,2)


    '''State Variable Enum (with 2 friendly agents and 1 opponent)'''
    X_POSITION, Y_POSITION, ORIENTATION, BALL_PROXIMITY, BALL_ANGLE, \
      ABLE_KICK, CENTER_PROXIMITY, GOAL_ANGLE, GOAL_OPENING, \
      OPPONENT_PROXIMITY, FRIEND1_GOAL_OPPENING, FRIEND2_GOAL_OPPENING, \
      FRIEND1_OPP_PROXIMITY, FRIEND2_OPP_PROXIMITY, FRIEND1_OPENING, \
      FRIEND2_OPENING, FRIEND1_PROXIMITY, FRIEND1_ANGLE, FRIEND1_NUMBER, \
      FRIEND2_PROXIMITY, FRIEND2_ANGLE, FRIEND2_NUMBER, OPP_PROXIMITY, \
      OPP_ANGLE, OPP_NUMBER = range(25)

    def __init__(self):
        """ Initializes an agent for a given environment. """

        print('***** Connecting to HFO server')
        self.hfo = HFOEnvironment()
        self.hfo.connectToServer(HIGH_LEVEL_FEATURE_SET,
                          './bin/teams/base/config/formations-dt', 6000,
                          'localhost', 'base_left', False)
        #self.unum = self.hfo.getUnum()
        self.unum = 0
        self.exploring = True
       

    @abc.abstractmethod
    def select_action(self,state):
        """ When this method is called, the agent executes an action. """
        pass

    @abc.abstractmethod
    def observe_reward(self,state,action,reward,statePrime):
        """ After executing an action, the agent is informed about the state-action-reward-state tuple """
        pass

    @abc.abstractmethod
    def step(self, state, action):
        """ Perform a complete training step """
        pass

    def set_exploring(self, exploring):
        """ The agent keeps track if it should explore in the current state (used for evaluations) """
        self.exploring = exploring


    def get_reward(self, status):
        """The Reward Function returns -1 when a defensive agent captures the ball,
        +1 when the agent's team scores a goal and 0 otherwise"""
        if(status == self.CAPTURED_BY_DEFENSE):
             return -1.0
        elif(status == self.GOAL):
             return 1.0
        return 0.0

    def execute_action(self, action):
        """Executes the action in the HFO server"""
        #If the action is not one of the default ones, it needs translation
        if action in range(15):
            self.hfo.act(action)
        else:
            #In the statespace_util file
            action, parameter = self.translate_action(action, hfo.getState())
            self.hfo.act(action, parameter)

    def translate_action(self, action, stateFeatures):
        """Defines the nearest and farthest friendly agents,
        then return the PASS action with the correct parameter"""
        nearest = 0
        farthest = 0

        if(stateFeatures[self.FRIEND1_PROXIMITY] > stateFeatures[self.FRIEND2_PROXIMITY]):
            nearest = stateFeatures[self.FRIEND1_NUMBER]
            farthest = stateFeatures[self.FRIEND2_NUMBER]
        else:
            nearest = stateFeatures[self.FRIEND2_NUMBER]
            farthest = stateFeatures[self.FRIEND1_NUMBER]
        actionRet = self.PASS

        if(action == self.PASSnear):
            argument = nearest
        elif(action == self.PASSfar):
            argument = farthest

        return actionRet, argument


    def get_transformed_features(self, stateFeatures):
        """Erases the irrelevant features (such as agent Unums) and sort agents by
        their distance"""
        #Defines the agent order
        if(stateFeatures[self.FRIEND1_PROXIMITY] > stateFeatures[self.FRIEND2_PROXIMITY]):
            nearestGoalOpening = stateFeatures[self.FRIEND1_GOAL_OPPENING]
            nearestOppProximity = stateFeatures[self.FRIEND1_OPP_PROXIMITY]
            nearestOpening = stateFeatures[self.FRIEND1_OPENING]
            nearestProximity = stateFeatures[self.FRIEND1_PROXIMITY]
            nearestAngle = stateFeatures[self.FRIEND1_ANGLE]

            farthestGoalOpening = stateFeatures[self.FRIEND2_GOAL_OPPENING]
            farthestOppProximity = stateFeatures[self.FRIEND2_OPP_PROXIMITY]
            farthestOpening = stateFeatures[self.FRIEND2_OPENING]
            farthestProximity = stateFeatures[self.FRIEND2_PROXIMITY]
            farthestAngle = stateFeatures[self.FRIEND2_ANGLE]
        else:
            nearestGoalOpening = stateFeatures[self.FRIEND2_GOAL_OPPENING]
            nearestOppProximity = stateFeatures[self.FRIEND2_OPP_PROXIMITY]
            nearestOpening = stateFeatures[self.FRIEND2_OPENING]
            nearestProximity = stateFeatures[self.FRIEND2_PROXIMITY]
            nearestAngle = stateFeatures[self.FRIEND2_ANGLE]

            farthestGoalOpening = stateFeatures[self.FRIEND1_GOAL_OPPENING]
            farthestOppProximity = stateFeatures[self.FRIEND1_OPP_PROXIMITY]
            farthestOpening = stateFeatures[self.FRIEND1_OPENING]
            farthestProximity = stateFeatures[self.FRIEND1_PROXIMITY]
            farthestAngle = stateFeatures[self.FRIEND1_ANGLE]

        stateFeatures[self.FRIEND1_GOAL_OPPENING] = nearestGoalOpening
        stateFeatures[self.FRIEND1_OPP_PROXIMITY] = nearestOppProximity
        stateFeatures[self.FRIEND1_OPENING] = nearestOpening
        stateFeatures[self.FRIEND1_PROXIMITY] = nearestProximity
        stateFeatures[self.FRIEND1_ANGLE] = nearestAngle

        stateFeatures[self.FRIEND2_GOAL_OPPENING] = farthestGoalOpening
        stateFeatures[self.FRIEND2_OPP_PROXIMITY] = farthestOppProximity
        stateFeatures[self.FRIEND2_OPENING] = farthestOpening
        stateFeatures[self.FRIEND2_PROXIMITY] = farthestProximity
        stateFeatures[self.FRIEND2_ANGLE] = farthestAngle

        #Removes the agent Unum... makes the friendly agents differentiable only by their feature values
        # and makes easier the state translation for the advising
        stateFeatures = np.delete(stateFeatures, [self.FRIEND1_NUMBER, self.FRIEND2_NUMBER])
        return stateFeatures
        
        
    def get_Unum(self):
        return self.hfo.getUnum()