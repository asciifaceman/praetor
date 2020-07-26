# Some basic stuff for interacting with nameko

.PHONY: run

run:
	nameko shell --config nameko.yml

run-stream:
	nameko run stream --config nameko.yml

