#Stops all HFO related Processes
pkill -f  sh\ ru* 
pkill -f python\ exp*
pkill -f python\ /home/ruben/HFO*
killall -9 rcssserver

sh runSimpleExpServerRuben.sh 22445 10 > log/serverAdHocVisitAction.log &
sleep 5
sh runSimpleExpAgentRuben.sh 22445 AdHocVisitAction 1 10 > log/logAdHocVisitAction.log &

sh runSimpleExpServerRuben.sh 23445 10 > log/serverAdHocVisitAction.log &
sleep 5
sh runSimpleExpAgentRuben.sh 23445 AdHocVisitAction 11 20 > log/logAdHocVisitAction.log &

sh runSimpleExpServerRuben.sh 24445 10 > log/serverAdHocVisitAction.log &
sleep 5
sh runSimpleExpAgentRuben.sh 24445 AdHocVisitAction 21 30 > log/logAdHocVisitAction.log &

sh runSimpleExpServerRuben.sh 25445 10 > log/serverAdHocVisitAction.log &
sleep 5
sh runSimpleExpAgentRuben.sh 25445 AdHocVisitAction 31 40 > log/logAdHocVisitAction.log &

sh runSimpleExpServerRuben.sh 26445 10 > log/serverAdHocVisitAction.log &
sleep 5
sh runSimpleExpAgentRuben.sh 26445 AdHocVisitAction 41 50 > log/logAdHocVisitAction.log &

# -- 

sh runSimpleExpServerRuben.sh 32945 10 > log/serverAdHocTDAction.log &
sleep 5
sh runSimpleExpAgentRuben.sh 32945 AdHocTDAction 1 10 > log/logAdHocTDAction.log &

sh runSimpleExpServerRuben.sh 33945 10 > log/serverAdHocTDAction.log &
sleep 5
sh runSimpleExpAgentRuben.sh 33945 AdHocTDAction 11 20 > log/logAdHocTDAction.log &

sh runSimpleExpServerRuben.sh 34945 10 > log/serverAdHocTDAction.log &
sleep 5
sh runSimpleExpAgentRuben.sh 34945 AdHocTDAction 21 30 > log/logAdHocTDAction.log &

sh runSimpleExpServerRuben.sh 35945 10 > log/serverAdHocTDAction.log &
sleep 5
sh runSimpleExpAgentRuben.sh 35945 AdHocTDAction 31 40 > log/logAdHocTDAction.log &

sh runSimpleExpServerRuben.sh 36945 10 > log/serverAdHocTDAction.log &
sleep 5
sh runSimpleExpAgentRuben.sh 36945 AdHocTDAction 41 50 > log/logAdHocTDAction.log &