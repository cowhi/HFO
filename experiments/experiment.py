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
from cmac import CMAC


from agents.agent import Agent

AGENT = None
hfo = None
cmac = None

def get_args():
    parser = argparse.ArgumentParser(
            description="Agent parameter"
    )
    parser.add_argument('-a','--agent',default='Dummy')
    parser.add_argument('-i','--evaluation_interval',type=int, default=5)
    parser.add_argument('-d','--evaluation_duration',type=int, default=5)
    parser.add_argument('-l','--log_file',default='Dummy_1_1')
    return parser.parse_args()


def transformFeatures(features):
    ''' From continuous to discrete using CMAC '''
    data = []
    for feature in features:
        quantized_features = cmac.quantize(feature)
        data.append([pts])
    return data

def getReward(status):
    """The Reward Function returns -1 when a defensive agent captures the ball,
    +1 when the agent's team scores a goal and 0 otherwise"""
    if(status == CAPTURED_BY_DEFENSE):
         return -1.0
    elif(status == GOAL):
         return 1.0
    return 0.0


def main():
    print('New agent called')

    print('***** Loading HFO environment')
    hfo = HFOEnvironment()

    print('***** Connecting to HFO server')
    hfo.connectToServer(HIGH_LEVEL_FEATURE_SET,
                      'bin/teams/base/config/formations-dt', 6000,
                      'localhost', 'base_left', False)

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
    print('***** '+ parameter.agent +' Agent online')

    """
    print('***** Setting up result log files')
    train_csv_file = open(parameter.log_file+"_train", "wb")
    train_csv_writer = csv.writer(train_csv_file)
    train_csv_writer.writerow(("trial","frames_trial","goals_trial"))
    train_csv_file.flush()
    eval_csv_file = open(parameter.log_file+"_eval", "wb")
    eval_csv_writer = csv.writer(eval_csv_file)
    eval_csv_writer.writerow(("trial","goal_percentage","avg_goal_time"))
    eval_csv_file.flush()
    """

    print('***** Initializing discretization with CMAC')
    cmac = CMAC(1,0.5,0.1)

    print('***** Start training')
    for trial in itertools.count():
        print('***** Starting trial %d' % trial)
        status = IN_GAME
        frame = 0
        while status == IN_GAME:
            # count frames
            frame += 1
            # rember last status (necessary?)
            old_status = status
            # Get current state features
            features = hfo.getState()
            #print('********** features [%s]: %s' % (str(type(features)), str(features)))
            # Transform features with tile encoding
            #state = transformFeatures(features)
            state = features
            #print('********** State: %s' % str(state))
            # Select action in regard to state
            action = AGENT.select_action(state)
            #print('********** Action: %s' % str(action))
            # Advance the environment and get the game status
            hfo.act(action)
            status = hfo.step()
            #print('********** Status after frame %d: %s' % (frame, hfo.statusToString(status)))
            reward = getReward(status)
            #print('********** Reward: %s' % str(reward))
        # Check the outcome of the trial
        print('***** Trial ended with %s'% hfo.statusToString(status))
        """
        # save stuff
        train_csv_writer.writerow((trial,frame,reward))
        train_csv_file.flush()

        # perform an evaluation trial

        if(trial % parameter.evaluation_interval == 0):
            print('***** Running evaluation trials')
            AGENT.setExploring(False)
            goals = 0.0
            time_to_goal = 0.0

            for eval_trials in range(1,parameter.evaluation_duration):
                eval_frame = 0
                eval_status = IN_GAME
                while eval_status == IN_GAME:
                    eval_frame += 1
                    eval_state = hfo.getState()
                    eval_action = AGENT.select_action(eval_state)
                    hfo.act(eval_action)
                    eval_status = hfo.step()
                    if(eval_status == GOAL):
                        goals += 1.0
                        time_to_goal += eval_frame
                        print('********** GGGGOOOOOOOOOOLLLL: %s in %s' % (str(goals), str(time_to_goal)))
            goal_percentage = 100*goals/parameter.evaluation_duration
            if (goals != 0):
                avg_goal_time = time_to_goal/goals
            else:
                avg_goal_time = 0.0
            print('***** Goal Percentage: '+ str(goal_percentage))
            print('***** Average Time to Goal: '+ str(avg_goal_time))
            eval_csv_writer.writerow((trial,"{:.2f}".format(goal_percentage),"{:.2f}".format(avg_goal_time)))
            eval_csv_file.flush()
            AGENT.setExploring(True)
        """
        # Quit if the server goes down
        if status == SERVER_DOWN:
            hfo.act(QUIT)
            print('***** Shutting down agent')
            break
    """
    eval_csv_file.close()
    train_csv_file.close()
    """



if __name__ == '__main__':
    main()
