
all: *.py depend
	@python run.py

depend: requirements.txt
	@sudo easy_install pip
	@sudo pip install -r requirements.txt

