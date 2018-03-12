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

import textwrap
import sys
import random
import os
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

    def select_file(self):
        while True:  # need to search through multiple files till one that has not already been done
            rng = random.randint(0, len(self.files)-1)
            file = self.files[0]#rng] # removed random nature for texting, for now
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
                del self.files[rng]
                xml.close()

    def read_file(self, file):
        display = Display()
        xml = open(os.path.join(self.root_dir, file))
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
                display.display_speeches(member, topic.get('title'), speeches_text)
                member = display.display_menu()
# end class ManualTagger


class Display:
    options_menu = "1: Mark Sentiment\n" \
                   "2: Edit Member\n" \
                   "3: Edit Subject\n" \
                   "Q: Quit\n" \
                   ":"
    options_dict = dict()

    def __init__(self, window_width=70):
        print("INITIALIZING DISPLAY")
        self.width = window_width
        self.options_dict = {"1": self.mark_sentiment,
                             "2": self.edit_member,
                             "3": self.edit_subject,
                             "Q": self.quit}
        self.move_on = False

        self.member_soup = bs()
        self.topic_title = ""

    def display_speeches(self, member, topic, speeches):
        pass
        self.member_soup = member
        self.topic_title = topic
        print("\nMember: ", member.get('membername'))

        print("Topic:  ", topic)
        i = 1
        for speech in speeches:
            print("Speech ", i, ":")
            for line in textwrap.wrap(speech.text, self.width):
                print(line)
            i += 1

    def display_menu(self):
        self.move_on = False
        while not self.move_on:
            try:
                new_input = input(self.options_menu).upper()
                self.options_dict[new_input]()
            except KeyError:
                print("{} NOT VALID INPUT".format(new_input))
        return self.member_soup

    def mark_sentiment(self):
        print("MARK SENTIMENT")
        sentiment_opt = "1: Mark as Positive\n" \
                        "2: Mark as Negative\n" \
                        "3: Mark as Neutral\n" \
                        "4: Mark as Unknown\n" \
                        "Q: Return to Menu\n" \
                        ":"
        self.move_on = True

        stance_tag = self.member_soup.find('stance')
        if not stance_tag:
            stance_tag = self.member_soup.new_tag('stance')
            topic_tag = self.member_soup.find('topic', attrs={'title': self.topic_title})
            topic_tag.append(stance_tag)

        valid = False
        while not valid:
            new_input = input(sentiment_opt).upper()
            if new_input == '1':
                print("MARKING AS POSITIVE")
                stance_tag.append("POS")
                valid = True
                pass
            elif new_input == '2':
                print("MARKING AS NEGATIVE")
                stance_tag.append("NEG")
                valid = True
                pass
            elif new_input == '3':
                print("MARKING AS NEUTRAL")
                stance_tag.append("NEU")
                valid = True
                pass
            elif new_input == '4':
                print("MARKING AS UNKNOWN")
                stance_tag.append("UKN")
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

    def edit_subject(self):
        print("EDIT SUBJECT")

    def quit(self):
        quit_input = input("Are You Sure you want to quit? \nAll Changes to this file will be lost. \nY/N: ").upper()
        if quit_input == 'Y':
            quit()
# end class Display


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
