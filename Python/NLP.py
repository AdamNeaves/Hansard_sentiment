import re
import csv
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.classify import NaiveBayesClassifier
from nltk.sentiment import SentimentAnalyzer
import pickle
from nltk.sentiment.util import *
import string
import random

print("USING NLTK VERSION {}".format(nltk.__version__))

all_words = []


def sentence_split(text):
    # because NLTK's sentence tokenizer recognises hon. as the end of a sentence, unlike mr. or mrs., we need to
    # replace that with something it can handle
    regex_hon = re.compile(r'\bhon\.', re.IGNORECASE)
    regex_percent = re.compile(r'\bper cent\.', re.IGNORECASE)  # also NLTK see "cent." as end of sentence so fix that
    regex_sentence_end = re.compile(r'([a-z])\.([A-Z])')  # some sentences have no space separating. Fix that also
    text = re.sub(regex_hon, "honorable", text)
    text = re.sub(regex_percent, "percent", text)
    text = re.sub(regex_sentence_end, r'\1. \2', text)  # this will miss those times when a sentence ends with a caps letter
    text = text.replace('\n', ' ')
    return sent_tokenize(text)


def extract_name(text):
    # find a name in a sentence or piece of text
    # will assume the first name given that includes an honorific (mr., Mrs, etc) is the correct name
    punctuation = string.punctuation  # we want to get all the text from Mr/Mrs etc till it finds some punctuation
    punctuation = punctuation.replace("-", "")  # however, - and . are valid parts of a name, so we still want them
    punctuation = punctuation.replace(".", "")
    name_rex = re.compile(r'(\bMr[ .]|\bMrs[ .]|\bSir[ .]|\bDr[ .])[^{}\\\n]+'.format(punctuation), re.IGNORECASE)  # regex to find all honorifics. hopefully
    # tried using NLTKs NE_CHUNK to find the name but that didn't work as consistently as the regex option
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
        except IndexError:
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
        except IndexError:
            print("ERROR: Index out of bounds.")
            print("Name causing error: {}".format(name_two))
            raise

    if forname_one and forname_two:
        # TODO: Should recognise that A. Neaves and Adam Neaves are the same, so match A. to Adam
        same_forname = forname_one == forname_two
    else:
        same_forname = True

    same_surname = surname_one == surname_two
    same_hom = hon_one == hon_two  # TODO: honorifics may or may not have a period (Mr. or Mr), check for this
    return same_surname and same_forname and same_hom


def create_sentiment_model(pos_sentences, neg_sentences, model_save=None, train_percent=0.9):
    features = create_feature_set(pos_sentences, neg_sentences)  # get the list of features
    #  shuffles the feature set for us before returning so it can be used
    print("Splitting feature set into testing/training sets")
    num_in_train_set = int(len(features)*train_percent)
    training_set = features[:num_in_train_set]  # training set will be first x percent of feature list
    testing_set  = features[num_in_train_set:]  # testing set will be everything that remains#
    print("Number of training sentences: {}".format(len(training_set)))
    print("Number of testing sentences:  {}".format(len(testing_set)))
    print("TRAINING CLASSIFIER: PLEASE BE PATIENT")
    classifier = NaiveBayesClassifier.train(training_set)
    print("Classifier accuracy: {}%".format(nltk.classify.accuracy(classifier, testing_set)*100))
    print("Classifier 10 Most informative Features:")
    classifier.show_most_informative_features(10)
    if model_save:
        print("Saving model to {}".format(model_save))
        save_classifier = open(model_save, "wb")
        pickle.dump(classifier, save_classifier)
        save_classifier.close()
    else:
        print("No save location for the model: it will be lost after program closes!")
    return classifier


def create_feature_set(pos_doc, neg_doc):
    print("Converting annotated data to feature lists")
    global all_words
    # our features will be a list of words, with true or false, saying if that word is in the sentence

    # get every word used in both positive and negative sentences
    with open(pos_doc, 'r', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row_words = word_tokenize(row['Sentence'])
            all_words = all_words + row_words

    with open(neg_doc, 'r', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row_words = word_tokenize(row['Sentence'])
            all_words = all_words + row_words

    # order words by frequency
    all_words = nltk.FreqDist(all_words)

    all_words = list(all_words.most_common())[:3000]  # get the 3000 most frequent words (in theory?)
    # print(all_words)

    feature_sets = []

    with open(pos_doc, 'r', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sentence = row['Sentence']
            feature_sets.append((convert_sentence_to_features(sentence), row['Sentiment']))

    with open(neg_doc, 'r', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sentence = row['Sentence']
            feature_sets.append((convert_sentence_to_features(sentence), row['Sentiment']))

    print("{} sentences turned to feature lists".format(len(feature_sets)))
    # print(feature_sets)
    random.shuffle(feature_sets)
    return feature_sets


def convert_sentence_to_features(sentence):
    global all_words
    words = set(word_tokenize(sentence))
    filtered_words = []
    for word in words:
        if word not in stopwords.words('english'):
            # do we care if the word is a stop word? maybe
            filtered_words.append(word)
    features = {}

    for w in all_words:  # for each word in the list of 3000 most common words
        features[w[0]] = (w[0] in filtered_words)  # add word to features, with True if the word is in the sentence, else false

    return features  # so this ends up as a dict, with the words as keys, and True or False as values
# its possible that just "true" and "false" isn't good enough, and could be improved? perhaps a count?

