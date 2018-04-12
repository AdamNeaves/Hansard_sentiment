# -*- coding: utf-8 -*-
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

import sys
import random
import os
import csv
import NLP
from bs4 import BeautifulSoup as bs


class ManualTagger:

    def __init__(self, root_dir):
        print("MANUAL TAGGER CLASS CREATED")
        self.files = []
        self.root_dir = root_dir
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith('.xml'):
                    print("adding {} to list".format(file))
                    self.files.append(file)
        self.file_count = 0

        data_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.dirname(data_dir)
        data_dir = os.path.join(data_dir, "Data")
        # print("DATA DIRECTORY: {}".format(data_dir))
        self.annotated_dir = os.path.join(data_dir, "Annotated Speech")
        if not os.path.exists(self.annotated_dir):
            print("MAKING ANNOTATED SPEECH DIR")
            os.makedirs(self.annotated_dir, exist_ok=True)
        self.pos_file = os.path.join(self.annotated_dir, "pos.csv")
        self.neg_file = os.path.join(self.annotated_dir, "neg.csv")

        if not os.path.exists(self.pos_file):
            with open(self.pos_file, 'a', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Sentence", "Sentiment", "Member", "Topic"])

        if not os.path.exists(self.neg_file):
            with open(self.neg_file, 'a', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Sentence", "Sentiment", "Member", "Topic"])

    def select_file(self):
        while True:  # need to search through multiple files till one that has not already been done
            rng = random.randint(0, len(self.files)-1)
            file = self.files[rng]
            xml = open(os.path.join(self.root_dir, file))
            soup = bs(xml, 'xml')
            speeches = soup.find_all('speech')
            stance = soup.find('stance').text.replace('\n', '')

            if (speeches is not None) and not stance:
                xml.close()
                return file
            else:
                #  if there are no speech tags we can ignore it, or if the stance has been set
                print(file, " IS INVALID FILE: Either no speech found, or stance already has been added")
                self.files.remove(file)
                xml.close()

    def read_file(self, file):
        # display = Display(self.pos_file, self.neg_file)
        xml = open(os.path.join(self.root_dir, file), encoding="utf-8")
        soup = bs(xml, 'xml')
        # FILE LAYOUT
        # <date>
        #     <member>
        #         <topic>
        #             <stance></stance>
        #             <speech>
        #                 words words words
        #             </speech>
        #             ...multiple speech available
        #         </topic>
        #         ...multiple topics available
        #     </member>
        #     ...multiple members available
        # </date>
        members = soup.find_all('member')
        for member in members:
            topics = member.find_all('topic')
            for topic in topics:
                speeches_text = topic.find_all('speech')

                self.display_speeches(member.get('membername'), topic.get('title'), speeches_text)
        xml.close()
        # this deletes the contents of the file in order to write so must be done just before writing to avoid data loss
        xml = open(os.path.join(self.root_dir, file), 'wb')
        print("WRITING CHANGES TO FILE")
        xml.write(soup.prettify(encoding='utf-8'))
        xml.close()

    def display_speeches(self, member, topic, speeches):
        sentences = []
        print("\nMember: ", member)
        print("Topic:  ", topic)
        for speech in speeches:
            sentences.extend(NLP.sentence_split(speech.text))  # get a list of all sentences from this speech
        for sentence in sentences:
            sentiment = ''
            while sentiment.upper() not in ["P", "N", "U"]:
                print(sentence)
                sentiment = input("Sentiment: (P)ositive, (N)egative, ne(U)tral :")
                if sentiment.upper() == "P":
                    with open(self.pos_file, 'a', encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([sentence, "POS", member, topic])
                    # pos_writer.writerow([sentence, "POS", member, topic])
                elif sentiment.upper() == "N":
                    with open(self.neg_file, 'a', encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([sentence, "NEG", member, topic])
                    # neg_writer.writerow([sentence, "NEG", member, topic])
                elif sentiment.upper() == "U":
                    pass
# end class ManualTagger


if __name__ == "__main__":
    print("Running: ", sys.argv[0])
    if len(sys.argv) == 1:
        print("No root directory provided. Please Provide directory as argument")
    else:
        if os.path.isdir(sys.argv[1]):
            print("Root Directory: ", sys.argv[1])
            tagger = ManualTagger(sys.argv[1])
            # display = Display()
            file = tagger.select_file()
            print("FILE SELECTED: ", file)
            tagger.read_file(file)
        else:
            print("FIRST ARGUMENT MUST BE DIRECTORY")
