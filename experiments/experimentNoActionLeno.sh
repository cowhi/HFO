pkill -f  sh\ ru* 
pkill -f python\ exp*
pkill -f python\ /home/leno/HFO*
killall -9 rcssserver

sh runSimpleExpServer.sh 13445 10 > serverAdHocVisit.log &
sleep 5
sh runSimpleExpAgent.sh 13445 AdHocVisit 1 10 > logTestMetric.log &

sh runSimpleExpServer.sh 14445 10 > serverAdHocVisit.log &
sleep 5
sh runSimpleExpAgent.sh 14445 AdHocVisit 11 20 > logTestMetric.log &

sh runSimpleExpServer.sh 15445 10 > serverAdHocVisit.log &
sleep 5
sh runSimpleExpAgent.sh 15445 AdHocVisit 21 30 > logTestMetric.log &

sh runSimpleExpServer.sh 16445 10 > serverAdHocVisit.log &
sleep 5
sh runSimpleExpAgent.sh 16445 AdHocVisit 31 40 > logTestMetric.log &

sh runSimpleExpServer.sh 17445 10 > serverAdHocVisit.log &
sleep 5
sh runSimpleExpAgent.sh 17445 AdHocVisit 41 50 > logTestMetric.log &
# --
sh runSimpleExpServer.sh 13945 10 > serverAdHocTD.log &
sleep 5
sh runSimpleExpAgent.sh 13945 AdHocTD 1 10 > logTestMetric2.log &

sh runSimpleExpServer.sh 14945 10 > serverAdHocTD.log &
sleep 5
sh runSimpleExpAgent.sh 14945 AdHocTD 11 20 > logTestMetric2.log &

sh runSimpleExpServer.sh 15945 10 > serverAdHocTD.log &
sleep 5
sh runSimpleExpAgent.sh 15945 AdHocTD 21 30 > logTestMetric2.log &

sh runSimpleExpServer.sh 16945 10 > serverAdHocTD.log &
sleep 5
sh runSimpleExpAgent.sh 16945 AdHocTD 31 40 > logTestMetric2.log &

sh runSimpleExpServer.sh 17945 10 > serverAdHocTD.log &
sleep 5
sh runSimpleExpAgent.sh 17945 AdHocTD 41 50 > logTestMetric2.log &
