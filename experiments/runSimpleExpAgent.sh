# $1 is the port, $2 the agent, and $3 the number of repetitions python experiment.py -t 3000 -d 100 -r $I -i 10 -a1 $2 -a2 $2 -a3 $2 -p $1

for I in $(seq 1 1 $3)
do
	python experiment.py -t 3000 -d 50 -r $I -i 10 -a1 $2 -a2 $2 -a3 $2 -p $1
	sleep 20
done



