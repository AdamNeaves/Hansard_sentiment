import NLP
import pickle
import os
import sys


class HansardSentimentAnalyser:

    def __init__(self, model_save, annotated_dir, retrain=False):
        if not retrain:
            print("Loading model from {}".format(model_save))
            try:
                classifier_f = open(model_save, 'rb')
                self.classifier = pickle.load(classifier_f)
                classifier_f.close()
            except OSError as e:
                print("Error: classifer not found at {}. Try again".format(e.filename))

                raise
        else:
            print("CREATING CLASSIFIER")
            self.classifier = NLP.create_sentiment_model(os.path.join(annotated_dir, "pos.csv"),
                                                         os.path.join(annotated_dir, "neg.csv"),
                                                         model_save=model_save)

    def analyse(self, sentence):
        sentence_features = NLP.convert_sentence_to_features(sentence)
        classified = self.classifier.prob_classify(sentence_features)
        # prob = round(classified.prob(classified.max()), 2)
        # print("Sentence is {} at a probability of {}".format(classified.max(), prob))
        return classified


if __name__ == "__main__":
    # run if main file
    annotated_directory = ''
    model_location = ''
    try:
        if os.path.isdir(sys.argv[1]):
            annotated_directory = sys.argv[1]
        else:
            print("Arg 1 not a valid directory!")
            print("Arg 1: {}".format(sys.argv[1]))
            exit()
        if "pickle" in sys.argv[2]:
            model_location = sys.argv[2]
        else:
            print("Arg 2 not a valid model location")
            print("Arg 2: {}".format(sys.argv[2]))
            exit()

        sentiment_analyser = HansardSentimentAnalyser(model_location, annotated_directory, True)
    except IndexError:
        print("Not enough arguments to create the sentiment analysis! Try again")
        raise

    while True:
        input_sentence = input("Please input a sentence to analyse:")
        sentence_class = sentiment_analyser.analyse(input_sentence)
        prob = round(sentence_class.prob(sentence_class.max()), 2)
        print("Sentence is {} at a probability of {}".format(sentence_class.max(), prob))




