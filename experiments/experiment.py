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




def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--number_agents',type=int, default=3)
    parser.add_argument('-a1','--agent1',  default='Dummy')
    parser.add_argument('-a2','--agent2',  default='Dummy')
    parser.add_argument('-a3','--agent3',  default='Dummy')
    parser.add_argument('-a4','--agent4',  default='Dummy')
    parser.add_argument('-a5','--agent5',  default='Dummy')
    parser.add_argument('-a6','--agent6',  default='Dummy')
    parser.add_argument('-a7','--agent7',  default='Dummy')
    parser.add_argument('-a8','--agent8',  default='Dummy')
    parser.add_argument('-a9','--agent9',  default='Dummy')
    parser.add_argument('-a10','--agent10',default='Dummy')
    parser.add_argument('-a11','--agent11',default='Dummy')
    parser.add_argument('-t','--learning_trials',type=int, default=10)
    parser.add_argument('-i','--evaluation_interval',type=int, default=5)
    parser.add_argument('-d','--evaluation_duration',type=int, default=5)
    parser.add_argument('-s','--seed',type=int, default=12345)
    parser.add_argument('-l','--log_file',default='./LOG/')
    parser.add_argument('-p','--port',type=int, default=12345)
    parser.add_argument('-r','--number_trial',type=int, default=1)
    return parser.parse_args()

'''
def get_reward(status):
    """The Reward Function returns -1 when a defensive agent captures the ball,
    +1 when the agent's team scores a goal and 0 otherwise"""
    if(status == CAPTURED_BY_DEFENSE):
         return -1.0
    elif(status == GOAL):100
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

def build_agents():
    """Builds and returns the agent objects as specified by the arguments"""
    agents = []    
    
    
    parameter = get_args()
    
    for i in range(parameter.number_agents):
        agentName = getattr(parameter,"agent"+str(i+1))
        try:
           AgentClass = getattr(
                __import__('agents.' + (agentName).lower(),
                        fromlist=[agentName]),
                agentName)
        except ImportError:
           sys.stderr.write("ERROR: missing python module: " +agentName + "\n")
           sys.exit(1)
    
        AGENT = AgentClass(seed=parameter.seed, port=parameter.port)
        agents.append(AGENT)
    return agents
    

def main():
    print('New agent called')

    print('***** Loading agent implementation')
    agents = build_agents()
    #print('***** %s: %s Agent online' % (str(AGENT.unum), str(parameter.agent)))
    print('***** %s: Agents online --> %s')
   # print('***** %s: Agents online --> %s' % (str(AGENT.unum), str(AGENT)))
   # print('***** %s: Setting up train log files' % str(AGENT.unum))
    #train_csv_file = open(parameter.log_file + "_" + str(AGENT.unum) + "_train", "wb")
    
    #Initiate agent Threads    
    global okThreads
    okThreads = True
    
    agentThreads = []
    
    #Initiating agent
    for i in range(parameter.number_agents):
        agentThreads[i] = Thread(target = thread_agent, args=(agent[i],agents,i,parameter))
    
    #Waiting for program termination
    for i in range(parameter.number_agents):
        agentThreads[i].join()
    

    
    
def thread_agent(agentObj,allAgents,agentIndex,mainParameters):
    """This method is executed by each thread in the system and corresponds to the control
    of one playing agent"""
      
    #Building Log folder name
      
    logFolder = mainParameters.log_file + getattr(parameter,"agent"+str(i+1))+"/_0_"+str(parameter.number_trial)+"_AGENT_"+str(agentIndex)+"_RESULTS"
    
    train_csv_file = open(logFolder + "_train", "wb")
    train_csv_writer = csv.writer(train_csv_file)
    train_csv_writer.writerow(("trial","frames_trial","goals_trial","used_budget"))
    train_csv_file.flush()
    print('***** %s: Setting up eval log files' % str(agentObj.unum))
    #eval_csv_file = open(parameter.log_file + "_" + str(AGENT.unum) + "_eval", "wb")
    eval_csv_file = open(logFolder + "_eval", "wb")
    eval_csv_writer = csv.writer(eval_csv_file)
    eval_csv_writer.writerow(("trial","goal_percentage","avg_goal_time","used_budget"))
    eval_csv_file.flush()
    
    #Setups advising
    agentObj.setupAdvising(agentIndex,allAgents)

    print('***** %s: Start training' % str(AGENT.unum))
    for trial in range(0,parameter.learning_trials+1):
        # perform an evaluation trial
        if(trial % parameter.evaluation_interval == 0):
            #print('***** %s: Running evaluation trials' % str(AGENT.unum) )
            agentObj.set_exploring(False)
            goals = 0.0
            time_to_goal = 0.0
            for eval_trials in range(1,parameter.evaluation_duration+1):
                eval_frame = 0
                eval_status = agentObj.IN_GAME
                stateFeatures = agentObj.hfo.getState()
                state = agentObj.get_transformed_features(stateFeatures)
                #action = AGENT.select_action(tuple(stateFeatures), state)
                action = agentObj.select_action(stateFeatures, state)
                while eval_status == agentObj.IN_GAME:
                    eval_frame += 1
                    eval_status, state, action = agentObj.step(state, action)
                    if(eval_status == agentObj.GOAL):
                        goals += 1.0
                        time_to_goal += eval_frame
                        #print('********** %s: GGGGOOOOOOOOOOLLLL: %s in %s' % (str(AGENT.unum), str(goals), str(time_to_goal)))
            goal_percentage = 100*goals/parameter.evaluation_duration
            #print('***** %s: Goal Percentage: %s' % (str(AGENT.unum), str(goal_percentage)))
            if (goals != 0):
                avg_goal_time = time_to_goal/goals
            else:
                avg_goal_time = 0.0
            #print('***** %s: Average Time to Goal: %s' % (str(AGENT.unum), str(avg_goal_time)))
            # save stuff
            eval_csv_writer.writerow((trial,"{:.2f}".format(goal_percentage),"{:.2f}".format(avg_goal_time),str(AGENT.get_used_budget())))
            eval_csv_file.flush()
            agentObj.set_exploring(True)
            # reset agent trace
            agentObj.stateActionTrace = {} 
           
        
        #print('***** %s: Starting Learning Trial %d' % (str(AGENT.unum),trial))
        status = agentObj.IN_GAME
        frame = 0
        stateFeatures = agentObj.hfo.getState()
        state = agentObj.get_transformed_features(stateFeatures)
        #print('***** %s: state type: %s, len: %s' % (str(AGENT.unum), str(type(state)), str(len(state))))
        #action = AGENT.select_action(tuple(stateFeatures), state)
        action = agentObj.select_action(stateFeatures, state)
        #print "Selected action --- "+str(action)
        while status == agentObj.IN_GAME:
            frame += 1
            status, state, action = agentObj.step(state, action)
        #print('***** %s: Trial ended with %s'% (str(AGENT.unum), AGENT.hfo.statusToString(status)))
        #print('***** %s: Agent --> %s'% (str(AGENT.unum), str(AGENT)))
        reward = agentObj.get_reward(status)
        # save stuff
        train_csv_writer.writerow((trial,frame,reward,str(agentObj.get_used_budget())))
        train_csv_file.flush()
        agentObj.stateActionTrace = {}



        # Quit if the server goes down
        if status == agentObj.SERVER_DOWN:
            agentObj.hfo.act(QUIT)
            print('***** %s: Shutting down agent' % str(agentObj.unum))
            break
    print('***** %s: Agent --> %s'% (str(agentObj.unum), str(agentObj)))
    eval_csv_file.close()
    train_csv_writer.writerow(("-","-",str(agentObj)))
    train_csv_file.flush()
    train_csv_file.close()


if __name__ == '__main__':
    main()
