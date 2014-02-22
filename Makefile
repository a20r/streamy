
all: *.py depend
	@python run.py

depend: requirements.txt
	@sudo brew install pip
	@sudo pip install -r requirements.txt

