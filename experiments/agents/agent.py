import logging
from hfo import *
_logger = logging.getLogger(__name__)

import abc

class Agent(object):
    """ This is the base class for all agent implementations.

    The agent gets its available actions from the environment, keeps track of
    his current state and saves his experiences in a replay memory while acting
    in the environment.

    Attributes:
        name (str): The name of the network object.
        env (Environment): The envirnoment in which the agent actuates (which is an HFO object).
        rng (mtrand.RandomState): Initialized Mersenne Twister pseudo-random number generator.
        n_steps_total (int): Counter of all training steps.
        callback (Statistics): The stats module that attaches itself to the agent.
        exploring: variable to indicate if the agent is exploring or exploiting

    Note:
        All subclasses must inherite this class --> 'class NewClass(Agent)'

    """
    __metaclass__ = abc.ABCMeta

    '''The HFO object'''
    hfo = None

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


    def __str__(self):
        """ Overwrites the object.__str__ method.

        Returns:
            string (str): Important parameters of the object.
        """
        return "'name':" + str(self.name) + ", " + \
               "'epsilon_start':" + str(self.epsilon_start) + ", " + \
               "'epsilon_end':" + str(self.epsilon_end) + ", " + \
               "'epsilon_decay_steps':" + str(self.epsilon_decay_steps) + ", " + \
               "'n_avail_actions':" + str(self.n_avail_actions) + ", " + \
               "'avail_actions':" + str(self.avail_actions)

    def __init__(self,hfo):
        """ Initializes an agent for a given environment. """
        self.hfo = hfo
        self.exploring = True


    @abc.abstractmethod
    def select_action(self,state):
        """ When this method is called, the agent executes an action. """
        pass

    @abc.abstractmethod
    def observe_reward(self,state,action,reward,statePrime):
        """ After executing an action, the agent is informed about the state-action-reward-state tuple """
        pass

    def set_exploring(self,exploring):
        """ The agent keeps track if it should explore in the current state (used for evaluations) """
        self.exploring = exploring
