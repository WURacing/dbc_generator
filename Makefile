 
.PHONY: install
install:
	pip3 install -r requirements.txt

.PHONY: test
test:
	Make is not configured to run any tests

.PHONY: run
run:
	python3 ./dbc_generator server.py