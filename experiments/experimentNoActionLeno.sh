pkill -f  sh\ ru* 
pkill -f python\ exp*
pkill -f python\ /home/leno/HFO*
killall -9 rcssserver

sh runSimpleExpServer.sh 43945 5 > serverEpisodeSharing.log &
sleep 5
sh runSimpleExpAgent.sh 43945 EpisodeSharing 1 5 > logEpisodeSharing.log &

sh runSimpleExpServer.sh 44945 5 > serverEpisodeSharing.log &
sleep 5
sh runSimpleExpAgent.sh 44945 EpisodeSharing 6 10 > logEpisodeSharing.log &

sh runSimpleExpServer.sh 45945 5 > serverEpisodeSharing.log &
sleep 5
sh runSimpleExpAgent.sh 45945 EpisodeSharing 11 15 > logEpisodeSharing.log &

sh runSimpleExpServer.sh 46945 5 > serverEpisodeSharing.log &
sleep 5
sh runSimpleExpAgent.sh 46945 EpisodeSharing 16 20 > logEpisodeSharing.log &

sh runSimpleExpServer.sh 47945 5 > serverEpisodeSharing.log &
sleep 5
sh runSimpleExpAgent.sh 47945 EpisodeSharing 21 25 > logEpisodeSharing.log &

sh runSimpleExpServer.sh 46985 5 > serverEpisodeSharing.log &
sleep 5
sh runSimpleExpAgent.sh 46985 EpisodeSharing 26 30 > logEpisodeSharing.log &

sh runSimpleExpServer.sh 47045 5 > serverEpisodeSharing.log &
sleep 5
sh runSimpleExpAgent.sh 47045 EpisodeSharing 31 35 > logEpisodeSharing.log &

sh runSimpleExpServer.sh 49945 5 > serverEpisodeSharing.log &
sleep 5
sh runSimpleExpAgent.sh 49945 EpisodeSharing 36 40 > logEpisodeSharing.log &

sh runSimpleExpServer.sh 46925 5 > serverEpisodeSharing.log &
sleep 5
sh runSimpleExpAgent.sh 46925 EpisodeSharing 41 45 > logEpisodeSharing.log &

sh runSimpleExpServer.sh 47245 5 > serverEpisodeSharing.log &
sleep 5
sh runSimpleExpAgent.sh 47245 EpisodeSharing 46 50 > logEpisodeSharing.log &


#sh runSimpleExpServer.sh 13445 3 > serverAdHocVisit.log &
#sleep 5
#sh runSimpleExpAgent.sh 13445 AdHocVisit 8 10 > logTestMetric.log &

#sh runSimpleExpServer.sh 14445 3 > serverAdHocVisit.log &
#sleep 5
#sh runSimpleExpAgent.sh 14445 AdHocVisit 18 20 > logTestMetric.log &

#sh runSimpleExpServer.sh 15445 3 > serverAdHocVisit.log &
#sleep 5
#sh runSimpleExpAgent.sh 15445 AdHocVisit 28 30 > logTestMetric.log &

#sh runSimpleExpServer.sh 16445 3 > serverAdHocVisit.log &
#sleep 5
#sh runSimpleExpAgent.sh 16445 AdHocVisit 38 40 > logTestMetric.log &

#sh runSimpleExpServer.sh 17445 3 > serverAdHocVisit.log &
#sleep 5
#sh runSimpleExpAgent.sh 17445 AdHocVisit 48 50 > logTestMetric.log &
# --
#sh runSimpleExpServer.sh 13945 5 > serverAdHocTD.log &
#sleep 5
#sh runSimpleExpAgent.sh 13945 AdHocTD 1 5 > logTestMetric2.log &

#sh runSimpleExpServer.sh 14945 5 > serverAdHocTD.log &
#sleep 5
#sh runSimpleExpAgent.sh 14945 AdHocTD 6 10 > logTestMetric2.log &

#sh runSimpleExpServer.sh 15945 5 > serverAdHocTD.log &
#sleep 5
#sh runSimpleExpAgent.sh 15945 AdHocTD 11 15 > logTestMetric2.log &

#sh runSimpleExpServer.sh 16945 5 > serverAdHocTD.log &
#sleep 5
#sh runSimpleExpAgent.sh 16945 AdHocTD 16 20 > logTestMetric2.log &

#sh runSimpleExpServer.sh 17945 5 > serverAdHocTD.log &
#sleep 5
#sh runSimpleExpAgent.sh 17945 AdHocTD 21 25 > logTestMetric2.log &

#sh runSimpleExpServer.sh 23945 5 > serverAdHocTD.log &
#sleep 5
#sh runSimpleExpAgent.sh 23945 AdHocTD 26 30 > logTestMetric2.log &

#sh runSimpleExpServer.sh 24945 5 > serverAdHocTD.log &
#sleep 5
#sh runSimpleExpAgent.sh 24945 AdHocTD 31 35 > logTestMetric2.log &

#sh runSimpleExpServer.sh 25945 5 > serverAdHocTD.log &
#sleep 5
#sh runSimpleExpAgent.sh 25945 AdHocTD 36 40 > logTestMetric2.log &

#sh runSimpleExpServer.sh 26945 5 > serverAdHocTD.log &
#sleep 5
#sh runSimpleExpAgent.sh 26945 AdHocTD 41 45 > logTestMetric2.log &

#sh runSimpleExpServer.sh 27945 5 > serverAdHocTD.log &
#sleep 5
#sh runSimpleExpAgent.sh 27945 AdHocTD 46 50 > logTestMetric2.log &
