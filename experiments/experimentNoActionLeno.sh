pkill -f  sh\ ru* 
pkill -f python\ exp*
pkill -f python\ /home/leno/HFO*
killall -9 rcssserver
#sleep 10
#sh runSimpleExpServer.sh 12345 1 > server1sarsa.log &
#sh runSimpleExpServer.sh 12345 10 > server1dummy.log &
#sleep 5
#sh runSimpleExpAgent.sh 12345 SARSATile 50 50 > logSarsa.log &
#sh runSimpleExpAgent.sh 12345 Dummy 10 > logDummy.log &

#sh runSimpleExpServer.sh 12445 10 > serverAdhocvisit.log &
#sleep 5
#sh runSimpleExpAgent.sh 12445 AdHocVisit 4 13 > logAdhocvisit.log &
sh runSimpleExpServer.sh 13445 50 > serverAdHocVisit.log &
sleep 5
sh runSimpleExpAgent.sh 13445 AdHocVisit 1 50 > logTestMetric.log &

sh runSimpleExpServer.sh 13945 50 > serverAdHocTD.log &
sleep 5
sh runSimpleExpAgent.sh 13945 AdHocTD 1 50 > logTestMetric2.log &
#sh runSimpleExpAgent.sh 12445 Dummy 10 > logAdhocvisit.log &

#sh runSimpleExpServer.sh 12545 10 > serverAdhocTD.log &
#sleep 5
#sh runSimpleExpAgent.sh 12545 AdHocTD 9 18 > logAdHocTD.log &

#sh runSimpleExpServer.sh 12645 6 > serverTorrey.log &
#sleep 5
#sh runSimpleExpAgent.sh 12645 Torrey 45 50 > logTorrey.log &


#sh runSimpleExpServer.sh 13145 50 > serverDummy.log &
#sleep 5
#sh runSimpleExpAgent.sh 13145 Dummy 1 50 > Dummy.log &
