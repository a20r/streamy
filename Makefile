
all: *.py depend
	@python run.py

depend: requirements.txt
	@brew install pip
	@sudo pip install -r requirements.txt

