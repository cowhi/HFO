#!/usr/bin/env python
# encoding: utf-8

# Before running this program, first Start HFO server:
# $> ./bin/HFO --offense-agents 1

import argparse
import sys
import os
import csv
import random, itertools
from hfo import *
#from cmac import CMAC


from agents.agent import Agent
from statespace_util import *

AGENT = None
hfo = None

def get_args():
    parser = argparse.ArgumentParser(
            description="Agent parameter"
    )
    parser.add_argument('-a','--agent',default='Dummy')
    parser.add_argument('-t','--learning_trials',type=int, default=10)
    parser.add_argument('-i','--evaluation_interval',type=int, default=5)
    parser.add_argument('-d','--evaluation_duration',type=int, default=5)
    parser.add_argument('-l','--log_file',default='Dummy_1_1')
    return parser.parse_args()

'''
def get_reward(status):
    """The Reward Function returns -1 when a defensive agent captures the ball,
    +1 when the agent's team scores a goal and 0 otherwise"""
    if(status == CAPTURED_BY_DEFENSE):
         return -1.0
    elif(status == GOAL):
         return 1.0
    return 0.0


def execute_action(hfo, action):
    """Executes the action in the HFO server"""
    #If the action is not one of the default ones, it needs translation
    if action in range(15):
        hfo.act(action)
    else:
        #In the statespace_util file
        action, parameter = translate_action(action, hfo.getState())
        hfo.act(action, parameter)

def get_local_features(features):
    """Returns a state in which the friendly agents are sorted by their distance"""
    #In the statespace_util file
    return get_transformed_features(features)
'''

def main():
    print('New agent called')

    print('***** Loading agent implementation')
    parameter = get_args()
    try:
        AgentClass = getattr(
                __import__('agents.' + (parameter.agent).lower(),
                        fromlist=[parameter.agent]),
                parameter.agent)
    except ImportError:
        sys.stderr.write("ERROR: missing python module: " + parameter.agent + "\n")
        sys.exit(1)
    AGENT = AgentClass()
    print('***** %s: %s Agent online' % (str(AGENT.unum), str(parameter.agent)))


    print('***** %s: Setting up result log files' % str(AGENT.unum))
    train_csv_file = open(parameter.log_file+"_train", "wb")
    train_csv_writer = csv.writer(train_csv_file)
    train_csv_writer.writerow(("trial","frames_trial","goals_trial"))
    train_csv_file.flush()
    eval_csv_file = open(parameter.log_file+"_eval", "wb")
    eval_csv_writer = csv.writer(eval_csv_file)
    eval_csv_writer.writerow(("trial","goal_percentage","avg_goal_time"))
    eval_csv_file.flush()

    print('***** %s: Start training' % str(AGENT.unum))
    for trial in range(1,parameter.learning_trials+1):
        print('***** %s: Starting Learning Trial %d' % (str(AGENT.unum),trial))
        status = AGENT.IN_GAME
        frame = 0
        # initialize
        state = AGENT.get_transformed_features(AGENT.hfo.getState())
        action = AGENT.select_action(state)
        while status == AGENT.IN_GAME:
            # count frames
            frame += 1
            # rember last status (necessary?)
            #old_status = status
            #Get a state in the agent's point of view
            #state = get_transformed_features(hfo.getState())
            #print('********** State: %s' % str(state))
            # Select action in regard to state
            #action = AGENT.select_action(state)
            #Execute the action in the environment
            #execute_action(hfo,action)
            #print('********** Action: %s' % str(action))
            # Advance the environment and get the game status
            #status = hfo.step()
            #print('********** Status after frame %d: %s' % (frame, hfo.statusToString(status)))
            #reward = get_reward(status)
            #print('********** Reward: %s' % str(reward))
            #statePrime = get_transformed_features(hfo.getState())

            #AGENT.observe_reward(state,action,reward,statePrime)
            status, state, agent = AGENT.step(state, action)

        # Check the outcome of the trial
        print('***** %s: Trial ended with %s'% (str(AGENT.unum), AGENT.hfo.statusToString(status)))
        reward = AGENT.get_reward(status)
        # save stuff
        train_csv_writer.writerow((trial,frame,reward))
        train_csv_file.flush()

        # perform an evaluation trial
        if(trial % parameter.evaluation_interval == 0):
            print('***** %s: Running evaluation trials' % str(AGENT.unum) )
            AGENT.set_exploring(False)
            goals = 0.0
            time_to_goal = 0.0

            for eval_trials in range(1,parameter.evaluation_duration+1):
                eval_frame = 0
                eval_status = AGENT.IN_GAME
                state = AGENT.get_transformed_features(AGENT.hfo.getState())
                action = AGENT.select_action(state)
                while eval_status == AGENT.IN_GAME:
                    eval_frame += 1
                    eval_status, state, agent = AGENT.step(state, action)
                    #eval_state = get_local_features(hfo.getState())
                    #eval_action = AGENT.select_action(eval_state)
                    #execute_action(hfo,eval_action)
                    #eval_status = hfo.step()
                    if(eval_status == AGENT.GOAL):
                        goals += 1.0
                        time_to_goal += eval_frame
                        print('********** %s: GGGGOOOOOOOOOOLLLL: %s in %s' % (str(AGENT.unum), str(goals), str(time_to_goal)))
            goal_percentage = 100*goals/parameter.evaluation_duration
            if (goals != 0):
                avg_goal_time = time_to_goal/goals
            else:
                avg_goal_time = 0.0
            print('***** %s: Goal Percentage: %s' % (str(AGENT.unum), str(goal_percentage)))
            print('***** %s: Average Time to Goal: %s' % (str(AGENT.unum), str(avg_goal_time)))
            eval_csv_writer.writerow((trial,"{:.2f}".format(goal_percentage),"{:.2f}".format(avg_goal_time)))
            eval_csv_file.flush()
            AGENT.set_exploring(True)

        # Quit if the server goes down
        if status == AGENT.SERVER_DOWN:
            AGENT.hfo.act(QUIT)
            print('***** %s: Shutting down agent' % str(AGENT.unum))
            break

    eval_csv_file.close()
    train_csv_file.close()


if __name__ == '__main__':
    main()
