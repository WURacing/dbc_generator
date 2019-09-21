 
.PHONY: install
install:
	pip3 install -r requirements.txt

.PHONY: test
test:
	pytest test_packet.py

.PHONY: run
run:
	python3 ./dbc_generator server.py