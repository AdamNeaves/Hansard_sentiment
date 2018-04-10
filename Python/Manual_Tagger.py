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

        data_dir = os.path.dirname(os.path.dirname(root_dir))
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
        display = Display(self.pos_file, self.neg_file)
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

                display.display_speeches(member.get('membername'), topic.get('title'), speeches_text)

                # member_name, topic_title, sentiment = display.display_menu()
                #
                # if not member_name == member.get('membername'):
                #     # member name has been edited
                #     member['membername'] = member_name
                #
                # if not topic_title == topic.get('title'):
                #     # topic title has been edited
                #     topic['title'] = topic_title
                #
                # stance_tag = topic.find('stance')
                # if not stance_tag:
                #     # for whatever reason the stance tag does not exist. we need to make it
                #     stance_tag = soup.new_tag('stance')
                #     topic.append(stance_tag)
                # stance_tag.append(sentiment)  # mark the sentiment in the XML
        xml.close()
        # this deletes the contents of the file in order to write so must be done just before writing to avoid data loss
        xml = open(os.path.join(self.root_dir, file), 'wb')
        print("WRITING CHANGES TO FILE")
        xml.write(soup.prettify(encoding='utf-8'))
        xml.close()
# end class ManualTagger


class Display:
    options_menu = "1: Mark Sentiment\n" \
                   "2: Edit Member\n" \
                   "3: Edit Subject\n" \
                   "Q: Quit\n" \
                   ":"
    options_dict = dict()

    def __init__(self, pos_file, neg_file, window_width=70):
        print("INITIALIZING DISPLAY")
        self.width = window_width
        self.options_dict = {"1": self.mark_sentiment,
                             "2": self.edit_member,
                             "3": self.edit_subject,
                             "Q": self.quit}
        self.move_on = False

        self.member_name = ""
        self.topic_title = ""
        self.sentiment = ""

        self.pos_file = pos_file
        self.neg_file = neg_file

    def display_speeches(self, member, topic, speeches):
        self.member_name = member
        self.topic_title = topic
        sentences = []
        # open_pos_file = open(self.pos_file, 'a', encoding="utf-8")
        # open_neg_file = open(self.neg_file, 'a', encoding="utf-8")
        # pos_writer = csv.writer(open_pos_file)
        # neg_writer = csv.writer(open_neg_file)

        print("\nMember: ", member)
        print("Topic:  ", topic)
        for speech in speeches:
            sentences.extend(NLP.sentence_split(speech.text))
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
        # open_pos_file.close()
        # open_neg_file.close()

    def display_menu(self):
        self.move_on = False
        while not self.move_on:
            new_input = input(self.options_menu).upper()
            try:
                self.options_dict[new_input]()
            except KeyError:
                print("{} NOT VALID INPUT".format(new_input))
        return self.member_name, self.topic_title, self.sentiment

    def mark_sentiment(self):
        print("MARK SENTIMENT")
        sentiment_opt = "1: Mark as Positive\n" \
                        "2: Mark as Negative\n" \
                        "3: Mark as Neutral\n" \
                        "4: Mark as Unknown\n" \
                        "Q: Return to Menu\n" \
                        ":"
        self.move_on = True

        valid = False
        while not valid:
            new_input = input(sentiment_opt).upper()
            if new_input == '1':
                print("MARKING AS POSITIVE")
                self.sentiment = "POS"
                valid = True
                pass
            elif new_input == '2':
                print("MARKING AS NEGATIVE")
                self.sentiment = "NEG"
                valid = True
                pass
            elif new_input == '3':
                print("MARKING AS NEUTRAL")
                self.sentiment = "NEU"
                valid = True
                pass
            elif new_input == '4':
                print("MARKING AS UNKNOWN")
                self.sentiment = "UKN"
                valid = True
                pass
            elif new_input == 'Q':
                print("RETURNING TO MENU")
                self.move_on = False
                valid = True
                pass
            else:
                print("INVALID INPUT. TRY AGAIN")
        # end while loop

    def edit_member(self):
        print("EDIT MEMBER")
        print("Current Member Name: ", self.member_name)
        new_name = input("Input New Name:")
        self.member_name = new_name

    def edit_subject(self):
        print("EDIT SUBJECT")
        print("Current Subject Title: ", self.topic_title)
        new_topic = input("Input new Subject:")
        self.topic_title = new_topic

    def quit(self):
        quit_input = input("Are You Sure you want to quit? \nAll Changes to this file will be lost. \nY/N: ").upper()
        if quit_input == 'Y':
            quit()
# end class Display


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
