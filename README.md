# streamy

Live video broadcasting


## Install

Currently the best way is to clone the repo and install the dependencies:

    git clone git@github.com:wallarelvo/stremy.git
    pip install -r requirements.txt  # installs dependencies for playground

**Essential**, streamy uses `nltk`, you must download 
`maxent_treebank_pos_tagger` under "Models" by using `nltk.download()`:

    python  # launch python interpreter from the terminal
    >>> import nltk
    >>> nltk.download()

    # An NLTK GUI will appear that allows you to select corpuses and models to
    # download. Under "Models" double click on `maxent_treebank_pos_tagger`.
    # The GUI should automatically start downloading the model for you.


## Authors (in no particular order)
- Alex Waller
- Alexey Sazonov
- Chris Choi
- Nick Tikhonov
