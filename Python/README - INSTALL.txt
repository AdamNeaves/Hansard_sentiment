This project was developed and tested Using Python 3.5, running on Ubuntu 16.04 LTS, though it should work on any system running Python 3.

The following Packages are required for this project to run (some of these may be standard Packages):
-requests (for HTTP connection)
-zipfile
-random
-csv
-BeautifulSoup4 (bs4)
-re (regular expressions)
-NLTK
  -nltk.tokenize
  -nltk.sentiment.util
  -nltk.corpus
  -nltk.classify
-pickle
-numpy

-----TESTING------
This project contains some unit tests. To run them, please install py-test, and then excecute the following command from the Python directory:

python3 -m pytest -v

The output of which can be compared with Appendix A of the report, which is a log of the same command.

-----RUNNING------

Each file is designed to be run from the command line, using Python3. Most of the files accept at least one argument when running it:

SPEECH PARSER - python3 Speech_Parser_BS.py <ROOT DIRECTORY>
  - The Root Directory must be a directory containing a series of the Hansard Dataset.

MANUAL TAGGER - python3 Manual_tagger.py <ROOT DIRECTORY>
  - The Root Directory must be a directory containing Parsed Data. This is created by the Speech Parser.

SENTIMENT ANALYSER - python3 sentiment_analyser.py <ANNOTATED DIRECTORY> <SAVED MODEL LOCATION>
  - The Annotated Directory must be the directory containing the POS.csv and NEG.csv files. These are created by the Manual Tagger.
  - the Model Location must be the path of a saved model, ending with the file extension ".pickle". This file does not have to exist as it will be created by the model training.
