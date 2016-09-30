pkill -f  sh\ ru* 
pkill python\ exp*
killall -9 rcssserver
sleep 10
sh runSimpleExpServer.sh 12345 10 > server1sarsa.log &
sleep 5
sh runSimpleExpAgent.sh 12345 SARSATile 10 > logSarsa.log &

sh runSimpleExpServer.sh 12445 10 > serverAdhocvisit.log &
sleep 5
sh runSimpleExpAgent.sh 12445 AdHocVisit 10 > logAdhocvisit.log &
#sh runSimpleExpAgent.sh 12445 Dummy 10 > logAdhocvisit.log &

sh runSimpleExpServer.sh 12545 10 > serverAdhocTD.log &
sleep 5
sh runSimpleExpAgent.sh 12545 AdHocTD 10 > logAdHocTD.log &

sh runSimpleExpServer.sh 12645 10 > serverTorrey.log &
sleep 5
sh runSimpleExpAgent.sh 12645 Torrey 10 > logTorrey.log &
