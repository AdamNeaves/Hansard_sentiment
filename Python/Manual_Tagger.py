#  A tool used to manually tag the sentiment of the speech to create a training/testing dataset

# it will display all speech made by a specific member on a specific topic in a specific day
# the user will then be asked to say whether the speech sounds positive, negative, or neutral towards the topic.

# POTENTIAL FEATURES
# - pre-allocation of sentiment/stance using basic NLP stuff, ask user to correct
# - is it possible to use NLP to check if the topic is accurate? read through the speech, find a topic
# - allow user to correct errors in text. Sometimes the topic gets stuck in the member tag, for instance
# - how MUCH of the data should we convert into training data? obviously CANT do all of it
#   - do we limit the number of things we label?
#   - do we assume we won't over-label due to the amount of data available?

# POTENTIAL ISSUES
# - typos and misspelling in names and topics.
# - Find a way to make sure "Harry Smith" and "Mr Smith" are recognised as the same person
# - Conversations. If displaying all speech from one person, may loose context if we cant see replies


class ManualTagger:

    def __init__(self, files):
        print("MANUAL TAGGER CLASS CREATED")

        self.files = files

    def read_file(self):
        # find topic
        # find member
        # find all instances where topic and member are the same/similar enough (john smith == Mr. Smith)
        pass

