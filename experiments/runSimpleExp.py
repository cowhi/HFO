# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 09:59:59 2016

@author: leno
"""
import subprocess
from threading import Thread

from time import sleep
import time


def thread_server(command):
    try:
        print "Starting server...."
        subprocess.check_call(command,shell='True')
    except subprocess.CalledProcessError:
        print "Failed... Starting Over"
        global okThreads
        okThreads = False
    subprocess.call("killall -9 rcssserver",shell='True')
    
def thread_agent(command):
    try:
        print "Starting Agent...."
        subprocess.check_call(command,shell='True')
    except subprocess.CalledProcessError:
        print "Failed... Starting Over"
        global okThreads
        okThreads = False
    
    

resultPath = "/home/leno/HFO/HFO-master/log/"
sourcePath = 'python /home/leno/Dropbox/DO\ -\ Felipe\ Leno\ da\ Silva/Artigos/NovoArtigo/HFO/experiments/experiment.py '
serverPath = "/home/leno/HFO/HFO-master/bin/HFO "

experimentAgentParam = "-p 12341 -s 12345  -i 10 -d 100 -t 500 -l /home/leno/HFO/HFO-master/log/"
serverParam = "--offense-agents=3 --defense-npcs=1 --fullstate --headless --trials=5500 --port 12341 --frames-per-trial 200"

serverScript = serverPath + serverParam

agentForExp = "SARSA"
#Including agent dependent parameters




numberRuns = 2

suc = 0

start_time = time.time()

while suc<numberRuns:
    global okThreads
    okThreads = True
    run_time = time.time()
    
    experimentRunAgent = experimentAgentParam + "t"+str(suc+1)+"/"+agentForExp + " -a "+agentForExp
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
    threadServer.join()
    threadAgent1.join()
    threadAgent2.join()
    threadAgent3.join()
    
    if okThreads:
        suc = suc+1
        print "Run "+str(suc)+" OK Run Time: " + str(time.time() - run_time)     
    
    
    


print "End of Experiment -- Total Time: "+ str(time.time()- start_time)



    
    








