for I in $(seq 1 1 10)
do
	for J in $(seq 1 1 10)
	do
		/home/leno/HFO/bin/HFO --offense-agents=3 --defense-npcs=1 --fullstate --headless --trials=6050 --port=12345 --frames-per-trial=200
	done
done
