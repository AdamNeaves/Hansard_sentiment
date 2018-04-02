import re
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.classify import NaiveBayesClassifier
# from nltk.sentiment.util import *
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
    # tried using NLTKs NE_CHUNK to find the name but that didnt work as consistently as the regex option
    match = re.search(name_rex, text)
    if match:
        return match.group(0).strip()  # return the whole matched text
    else:
        return text  # can't match with the regex? Just return the full text then


def name_match(name_one, name_two):
    # we assume the name has already been extracted using the above function. Maybe we should use that now anyway?
    if name_one == name_two:
        return True  # if they are the exact same then of course they match
    # if they are not the exact same, that doesn't quite mean they are different
    # could be a full name vs just surname (Mr John Smith vs Mr Smith)
    # so check if name two contains the surname from name one?
    # also, potentially make sure the first names are the same too. If we have John Smith and Matt Smith we need to
    # make sure their separate speech is categorised separately

    name_one_words = name_one.split()
    name_two_words = name_two.split()

    # ideally, names will always be either 2 or three words, one honorific at the start, and a surname at the end
    # with maybe a forename between the two
    if len(name_one_words) == 2:
        # two words means honorific and surname, right? right
        hon_one = name_one_words[0]
        forname_one = None
        surname_one = name_one_words[1]
    elif len(name_one_words) == 3:
        hon_one = name_one_words[0]
        forname_one = name_one_words[1]
        surname_one = name_one_words[2]
    else:
        try:
            hon_one = name_one_words[0]
            surname_one = name_one_words[-1]
            forname_one = None
        except IndexError as e:
            print("ERROR: Index out of bounds. Is the name blank?")
            print("Name causing error: {}".format(name_one))
            raise

    if len(name_two_words) == 2:
        # two words means honorific and surname, right? right
        hon_two = name_two_words[0]
        forname_two = None
        surname_two = name_two_words[1]
    elif len(name_two_words) == 3:
        hon_two = name_two_words[0]
        forname_two = name_two_words[1]
        surname_two = name_two_words[2]
    else:
        try:
            hon_two = name_two_words[0]
            surname_two = name_two_words[-1]
            forname_two = None
        except IndexError as e:
            print("ERROR: Index out of bounds.")
            print("Name causing error: {}".format(name_two))
            raise

    if forname_one and forname_two:
        same_forname = forname_one == forname_two
    else:
        same_forname = True

    same_surname = surname_one == surname_two
    same_hom = hon_one == hon_two
    return same_surname and same_forname and same_hom

