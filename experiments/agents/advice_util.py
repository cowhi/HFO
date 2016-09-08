# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 14:18:57 2016

@author: Felipe Leno
This file implements methods to make the communication between advisees and advisors
This agent communicates through text files. Of course this only works if all agents are executed in the same pc.
TODO: an actual message passing implementation
"""
import os
from time import sleep
import numpy as np


#When the agent asks for advice, it will create a file named by its uNum in this folder
#The file content will be the state
askFolder = "messages/ask/" 
#When an agent gives advice it will create a file in this folder.
#The file name will be <uNumAdvisee>-<uNumAdvisor> and the content is the advised action
adviceFolder = "messages/advice/"

#The time the agent waits for advice (ms)
askTimeout = 20.0


def ask_advice(uNum,state):
     """This method is executed when the advisee asks for advice.
       A file is created in the askFolder with the uNum, the agent waits for a while
       in order to wait for advice, then reads the response file in adviceFolder and erases
       all files, returning the advised action
       uNum - the Uniform number of the advisee
       state - the advisee state after it is processed in the statespace_util methods
       """
     askFilePath = askFolder+str(uNum)
     fileSay = open(askFilePath, 'w+')
     stateString = ""
     for x in state:
         stateString = stateString + str(x) + ";"
         
     fileSay.write(stateString)
     fileSay.close()
     
     sleep(askTimeout/1000)
     
     #Starts erasing the file
     os.remove(askFilePath)
     
     #reads if there is any advice to be read
     advice = []
     for fileD in os.listdir(adviceFolder):
            adviseeNum = int(fileD.split("-")[0]) #The first number in the file is the advisee
            #Check if this advice is for the local agent
            if(adviseeNum == uNum):
                #Read the advice and delete the file
                fileR = open(adviceFolder+fileD)
                line = fileR.readline()
                advice.append(line)
                os.remove(adviceFolder+fileD)
     return advice
    
def verify_advice(uNum):
    """This method should be executed to verify if another agent is asking for advice
    uNum - The uNum of the potential advisor
    The returns of this method is a list of uNums and states of advisees"""
    requirements = []
    #Checks the folder
    for fileD in os.listdir(askFolder):
        #only reads advice requirements of other agents        
        if(uNum!=int(fileD)):
            #Check if the agent has already advised for that advice request
            if not os.path.exists(adviceFolder+fileD+"-"+str(uNum)):
                try:             
                    fileR = open(askFolder+fileD)
                    state = fileR.readline()
                    requirements.append([int(fileD),state])
                except IOError:
                    pass
    return requirements
    
def give_advice(uNumAdvisee,uNumAdvisor,action):
    """This method is executed when the agent is giving advice
        A file is created in the adviceFolder named as <advisee>-<advisor>
        The file content is the action suggestion
    """
    filePath = adviceFolder+str(uNumAdvisee)+"-"+str(uNumAdvisor)
    fileAd= open(filePath, 'w+')
    fileAd.write(str(action))
    fileAd.close()
    
def recover_state(textualState):
    """ Transforms a text state read in an advice file to the numpy matrix"""    
    splittedState = textualState.split(";")[:-1]#Remove last empty element
    splittedState = np.asfarray(splittedState, dtype='float')
    return splittedState
    
    
    
    