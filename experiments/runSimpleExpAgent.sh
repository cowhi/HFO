for I in $(seq 1 1 10)
do
	python experiment.py -t 1000 -d 50 -r $I -i 10 -a1 AdHocTD -a2 AdHocTD -a3 AdHocTD
	sleep 10
	python experiment.py -t 1000 -d 50 -r $I -i 10 -a1 AdHocVisit -a2 AdHocVisit -a3 AdHocVisit
	sleep 10
	python experiment.py -t 1000 -d 50 -r $I -i 10 -a1 SARSATile -a2 SARSATile -a3 SARSATile
	sleep 10
	python experiment.py -t 1000 -d 50 -r $I -i 10 -a1 Torrey -a2 Torrey -a3 Torrey
	sleep 10
	python experiment.py -t 1000 -d 50 -r $I -i 10 -a1 Dummy -a2 Dummy -a3 Dummy
	sleep 10
done



