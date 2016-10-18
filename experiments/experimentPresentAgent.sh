#pkill -f  sh\ ru* 
#pkill -f python\ exp*
#pkill -f python\ /home/leno/HFO*
#killall -9 rcssserver
#sleep 10
#sh runSimpleExpServer.sh 32355 32 &
#sh runSimpleExpServer.sh 12345 10 > server1dummy.log &
#sleep 5
#sh runMultipleAlgExp.sh 32355 SARSATile SARSATile SARSATileLoading 19 50 /home/leno/HFO/experiments/agentData/FilesWithTrainedAgent/ &

sh runSimpleExpServer.sh 34455 48 > /home/leno/HFO/experiments/agentData/FilesWithTrainedAgent/serverTorrey.log &
sleep 5
sh runMultipleAlgExp.sh 34455 Torrey Torrey TorreyLoading 3 50 /home/leno/HFO/experiments/agentData/FilesWithTrainedAgent/ &

#sh runSimpleExpServer.sh 35455 50 > /home/leno/HFO/experiments/agentData/FilesWithTrainedAgent/serverVisit.log &
#sleep 5
#sh runMultipleAlgExp.sh 35455 AdHocVisit AdHocVisit AdHocVisitLoading 1 50 /home/leno/HFO/experiments/agentData/FilesWithTrainedAgent/ &

#sh runSimpleExpServer.sh 36455 50 > /home/leno/HFO/experiments/agentData/FilesWithTrainedAgent/serverTD.log &
#sleep 5
#sh runMultipleAlgExp.sh 36455 AdHocTD AdHocTD AdHocTDLoading 1 50 /home/leno/HFO/experiments/agentData/FilesWithTrainedAgent/ &


