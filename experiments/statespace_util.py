# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 09:54:23 2016

@author: Felipe Leno

This file implements Utilities for state space processing
"""

from agents.agent import Agent #importing the action enum

"""State Variable Enum (with 2 friendly agents and 1 opponent)"""
X_POSITION, Y_POSITION, ORIENTATION, BALL_PROXIMITY, BALL_ANGLE, ABLE_KICK, CENTER_PROXIMITY, GOAL_ANGLE, \
      GOAL_OPENING, OPPONENT_PROXIMITY, FRIEND1_GOAL_OPPENING, FRIEND2_GOAL_OPPENING, \
      FRIEND1_OPP_PROXIMITY, FRIEND2_OPP_PROXIMITY, FRIEND1_OPENING, FRIEND2_OPENING, \
      FRIEND1_PROXIMITY, FRIEND1_ANGLE, FRIEND1_NUMBER, FRIEND2_PROXIMITY, FRIEND2_ANGLE, FRIEND2_NUMBER, \
      OPP_PROXIMITY, OPP_ANGLE, OPP_NUMBER = range(25)



def translateAction(action, stateFeatures):
    """Defines the nearest and farthest friendly agents, 
    then return the PASS action with the correct parameter"""
    nearest = 0
    farthest = 0
    
    if(stateFeatures[FRIEND1_PROXIMITY] > stateFeatures[FRIEND2_PROXIMITY]):
        nearest = stateFeatures[FRIEND1_NUMBER]
        farthest = stateFeatures[FRIEND2_NUMBER]
    else:
        nearest = stateFeatures[FRIEND2_NUMBER]
        farthest = stateFeatures[FRIEND1_NUMBER]
    actionRet = Agent.PASS
    
    if(action==Agent.PASSnear):
        argument = nearest
    elif(action==Agent.PASSfar):
        argument = farthest
        
    return actionRet,argument
    
    
