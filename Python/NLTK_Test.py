import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')

string = """
The Parliamentary Secretary to the Ministry of Agriculture, Fisheries and Food (Mr. Jerry Wiggin)
        """

# STOLEN FULLY FROM
# https://github.com/acrosson/nlp/blob/master/information-extraction.py


def ie_preprocess(document):
    print("ORIGINAL SENTENCE:\n", document)
    document = ' '.join([i for i in document.split()])  # if i not in stop])
    print("sentence has been split: \n", document)
    sentences = nltk.sent_tokenize(document)
    print("sentence tokenized: \n", sentences)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    print("sentence word tokenized:\n", sentences)
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    print("sentence pos_tagged:\n", sentences)
    return sentences


def extract_names(document):
    names = []
    sentences = ie_preprocess(document)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            print("Sentence NE_chunked:\n", chunk)
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names


names = extract_names(string)
for name in names:
    print(name)
