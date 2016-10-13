pkill -f  sh\ ru* 
pkill -f python\ exp*
pkill -f python\ /home/leno/HFO*
killall -9 rcssserver

sh runSimpleExpServer.sh 22445 50 > log/serverAdHocVisitAction.log &
sleep 5
sh runSimpleExpAgent.sh 22445 AdHocVisitAction 1 50 > log/logAdHocVisitAction.log &

sh runSimpleExpServer.sh 22945 50 > log/serverAdHocTDAction.log &
sleep 5
sh runSimpleExpAgent.sh 22945 AdHocTDAction 1 50 > log/logAdHocTDAction.log &

sh runSimpleExpServer.sh 22645 50 > log/serverTorreyAction.log &
sleep 5
sh runSimpleExpAgent.sh 22645 Torrey 1 50 > log/logTorreyAction.log &


