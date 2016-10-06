pkill -f  sh\ ru* 
pkill -f python\ exp*
pkill -f python\ /home/leno/HFO*
killall -9 rcssserver
#sleep 10
sh runSimpleExpServer.sh 12345 4 > server1sarsa.log &
#sh runSimpleExpServer.sh 12345 10 > server1dummy.log &
sleep 5
sh runSimpleExpAgent.sh 12345 SARSATile 46 50 > logSarsa.log &
#sh runSimpleExpAgent.sh 12345 Dummy 10 > logDummy.log &

#sh runSimpleExpServer.sh 12445 10 > serverAdhocvisit.log &
#sleep 5
#sh runSimpleExpAgent.sh 12445 AdHocVisit 4 13 > logAdhocvisit.log &
sh runSimpleExpServer.sh 12445 14 > serverTestMetric.log &
sleep 5
sh runSimpleExpAgent.sh 12445 TestMetric 37 50 > logTestMetric.log &

sh runSimpleExpServer.sh 12945 21 > serverTestMetric2.log &
sleep 5
sh runSimpleExpAgent.sh 12945 TestMetric2 30 50 > logTestMetric2.log &
#sh runSimpleExpAgent.sh 12445 Dummy 10 > logAdhocvisit.log &

#sh runSimpleExpServer.sh 12545 10 > serverAdhocTD.log &
#sleep 5
#sh runSimpleExpAgent.sh 12545 AdHocTD 9 18 > logAdHocTD.log &

sh runSimpleExpServer.sh 12645 8 > serverTorrey.log &
sleep 5
sh runSimpleExpAgent.sh 12645 Torrey 43 50 > logTorrey.log &
