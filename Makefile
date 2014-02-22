
all: *.py depend
	@python run.py

depend: requirements.txt
	@sudo pip install -r requirements.txt

