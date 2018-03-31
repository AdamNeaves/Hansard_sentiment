import re
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string


def sentence_split(text):
    # because NLTK's sentence tokenizer recognises hon. as the end of a sentence, unlike mr. or mrs., we need to
    # replace that with something it can handle
    regex_hon = re.compile(r'\bhon\.', re.IGNORECASE)
    text = re.sub(regex_hon, "honorable", text)
    text = text.replace('\n', '')
    return sent_tokenize(text)


def extract_name(text):
    # find a name in a sentence or piece of text
    # will assume the first name given that includes an honorific (mr., Mrs, etc) is the correct name
    # words = word_tokenize(text)  # splits the sentence into a list of words
    # words = nltk.pos_tag(words)  # tags the words with their categorization such as nouns, verbs, etc
    punctuation = string.punctuation  # we want to get all the text from Mr/Mrs etc till it finds some punctuation
    punctuation = punctuation.replace("-", "")  # however, - and . are valid parts of a name, so we still want them
    punctuation = punctuation.replace(".", "")
    name_rex = re.compile(r'(\bMr\.|\bMrs\.|\bSir|\bDr\.)[^()\n][^{}]+'.format(punctuation), re.IGNORECASE)  # regex to find all honorifics. hopefully
    names = []
    # for chunk in nltk.ne_chunk(words):
    #     if type(chunk) == nltk.tree.Tree:
    #         print("CHUNK: ", chunk)
    #         if chunk.label() == 'PERSON':  # if chunk type is "person" then its a name, add to the list
    #             name = ' '.join([c[0] for c in chunk]).strip()
    #             name = name
    #             # print("NAME: '{}'".format(name))
    #
    #             names.append(name)
    #             if re.match(name_rex, name):
    #                 return name
    # return names[-1]  # possibility the name does not include a specified honorific, so just return last name found
    match = re.search(name_rex, text)
    if match:
        return match.group(0).strip()
    else:
        return text


def name_match(name_one, name_two):
    if name_one == name_two:
        return True  # if they are the exact same then of course they match
    # if they are not the exact same, that doesn't quite mean they are different
    # could be a full name vs just surname (Mr John Smith vs Mr Smith)
    # so check if name two contains the surname from name one?
    # also, potentially make sure the first names are the same too. If we have John Smith and Matt Smith we need to
    # make sure their separate speech is catagorised separately
    words = name_one.split()
    surname = words[-1]
    if surname in name_two:
        # surname in both names? probs same person
        return True
    # try the reverse just to make sure
    words = name_two.split()
    surname = words[-1]
    if surname in name_one:
        return True
    else:
        return False
