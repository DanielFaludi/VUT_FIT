FILE=xfalud00
PYTHON=/usr/bin/python3

build:
	echo "No need to build a python script, try 'make run'"

run:
	${PYTHON} ${CURDIR}/${FILE}.py $(port)
