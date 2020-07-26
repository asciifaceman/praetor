# Some basic stuff for interacting with nameko

.PHONY: shell run run-stream

shell:
	nameko shell --config nameko.yml

run-stream:
	nameko run stream --config nameko.yml

