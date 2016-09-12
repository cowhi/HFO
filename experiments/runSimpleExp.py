# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 09:59:59 2016

@author: leno
"""
import subprocess
from threading import Thread

from time import sleep
import time



numberRuns = 10
start = 0
agent = "Torrey" 



def thread_server(command): 
    try:
        print "Starting server...."
        subprocess.check_call(command,shell='True')
    except subprocess.CalledProcessError:
        print "Failed Server... Starting Over"
        global okThreads
        okThreads = False
    
    
def thread_agent(command):
    try:
        print "Starting Agent...."
        subprocess.check_call(command,shell='True')
    except subprocess.CalledProcessError:
        print "Failed Agent... Starting Over"
        global okThreads
        okThreads = False
    
    




def runExp(trial,agent):
    resultPath = "/home/leno/HFO/HFO-master/log/"
    sourcePath = 'python /home/leno/Dropbox/DO\ -\ Felipe\ Leno\ da\ Silva/Artigos/NovoArtigo/HFO/experiments/experiment.py '
    serverPath = "/home/leno/HFO/HFO-master/bin/HFO "
    
    experimentAgentParam = "-p 12341 -s 12345  -i 10 -d 100 -t 500 -l "+resultPath
    serverParam = "--offense-agents=3 --defense-npcs=1 --fullstate --headless --trials=5500 --port 12341 --frames-per-trial 200"
    
    serverScript = serverPath + serverParam
    global okThreads
    okThreads = True
   
    
    experimentRunAgent = experimentAgentParam + "t"+str(trial)+"/"+agent + " -a "+agent
    agentScript = sourcePath + experimentRunAgent
    threadServer = Thread(target = thread_server, args=(serverScript,))
    threadAgent1 = Thread(target = thread_agent, args=(agentScript,))
    threadAgent2 = Thread(target = thread_agent, args=(agentScript,))
    threadAgent3 = Thread(target = thread_agent, args=(agentScript,))
        
    threadServer.start()
    sleep(5)
    threadAgent1.start()
    sleep(5)
    threadAgent2.start()
    sleep(5)
    threadAgent3.start()
         
    #Wait for server
    #threadServer.join()
    threadAgent1.join()
    threadAgent2.join()
    threadAgent3.join()
    
    return okThreads 
    
    
    
n=start
start_time = time.time()
while n<numberRuns:
    subprocess.call("killall -9 rcssserver",shell='True')
    run_time = time.time()
    ok = runExp(n+1,agent)
    if ok:
        n = n+1
        print "Run "+str(n)+" OK Run Time: " + str(time.time() - run_time) 



print "End of Experiment -- Total Time: "+ str(time.time()- start_time)



    
    








