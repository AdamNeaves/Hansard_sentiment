
from bs4 import BeautifulSoup as bs
import os
import sys
import time


class SpeechParser:

    def __init__(self, root_dir):
        self.dir = root_dir
        parsed_dir = os.path.dirname(self.dir)
        base_name  = os.path.basename(self.dir)
        parsed_dir = os.path.join(os.path.dirname(parsed_dir), "Parsed Speech", base_name)
        print("PARSED DIRECTORY: ", parsed_dir)
        self.dest =  parsed_dir  # open(os.path.join(parsed_dir, '{}_parsed.xml'.format(base_name)), 'wb')

        if not(os.path.exists(parsed_dir)):
            os.makedirs(parsed_dir, exist_ok=True)

        self.files = []

    def parse_speeches(self, word_soup):
        # finds all member speeches in the provided soup, returning them in a better organised xml soup
        new_soup = bs()
        # new_soup.is_xml = True
        speech_count = 0
        for contribution in word_soup.find_all('membercontribution'):

            parent = contribution.parent
            member = parent.find('member')
            topic = parent.parent.find('title')

            if not member or not topic:
                continue  # no member or topic means we don't want to use this speech

            for unwanted_tag in contribution.find_all(['image', 'col']):  # remove unwanted tags
                unwanted_tag.decompose()

            for unwanted_tag in member.find_all(['image', 'col']):  # remove unwanted tags
                unwanted_tag.decompose()

            for unwanted_tag in topic.find_all(['image', 'col']):  # remove unwanted tags
                unwanted_tag.decompose()

            # date_tag   = new_soup.new_tag('date')    # create new tags for the soup to contain info
            topic_tag  = new_soup.new_tag('topic')   # we don't need tags for member cause we can
            stance_tag = new_soup.new_tag('stance')  # copy it from the original xml
            speech_tag = new_soup.new_tag('speech')

            new_soup.append(speech_tag)
            speech_soup = new_soup.contents[len(new_soup.contents)-1]
            # speech_soup.append(date_tag)
            # speech_soup.date.append(date.get('format'))

            speech_soup.append(topic_tag)
            speech_soup.topic.append(topic.text)

            speech_soup.append(member)

            speech_soup.append(stance_tag)

            speech_text = contribution.text.replace('\n', '')
            speech_soup.append(speech_text)
            speech_count += 1
            # print("SPEECH:\n", speech_soup.prettify())
        # print("        SPEECH COUNT: ", speech_count)
        return new_soup

    def find_files(self):
        for root, dirs, files in os.walk(self.dir):
            for file in files:
                if file.endswith('.xml'):
                    print("adding {} to list".format(file))
                    self.files.append(file)
        print("FILES FOUND: ", len(self.files))

    def parse_files(self):

        # ~~~~~~~~~~~~~~~~~~~PSEUDOCODE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # FOR EACH FILE
        #   FOR EACH DATE TAG
        #       IF(FILE FOR DATE EXISTS)
        #           LOAD FILE CONTENTS INTO DATE_SOUP
        #       ELSE
        #           CREATE FILE
        #           CREATE DATE_SOUP
        #       FIND ALL SPEECH IN TAG
        #       ADD SPEECH TO DATE_SOUP
        #       SAVE SOUP TO FILE (OVERWRITE)

        for file in self.files:
            start_time = time.time()
            print("START NEW FILE: ", file)
            xml = open(os.path.join(self.dir, file), 'r')  # open XML file
            origin_soup = bs(xml, 'xml')  # open XML file as soup
            date_tag_count = 0
            for date in origin_soup.find_all('date'):

                if "written" not in date.parent.title.text.lower():  # checking for written questions, we dont want them
                    date_file_path = os.path.join(self.dest, "{}.xml".format(date.get('format')))
                    if not os.path.exists(date_file_path):
                        print("CREATING FILE FOR DATE ", date.get("format"))
                        date_tag_count += 1                     # increase count of file
                        date_file = open(date_file_path, 'wb')  # file doesnt exist so we can just create without
                        date_soup = bs(features='xml')          # worrying that we are losing any data
                        date_tag = date_soup.new_tag('date', format=date.get('format'))
                        date_soup.append(date_tag)

                    else:
                        print("OPENING FILE ", date.get('format'), 'xml')
                        date_file = open(date_file_path, 'rb')  # open in read mode
                        date_soup = bs(date_file, 'xml')        # get contents into soup object
                        date_file.close()                       # close file
                        date_file = open(date_file_path, 'wb')  # open file in write mode, which deletes all contents

                    target_soup = date.parent
                    gen_soup = self.parse_speeches(target_soup)
                    date_soup.find('date', attrs={}).append(gen_soup)       # append found speech to the date tag
                    date_file.write(date_soup.prettify(encoding='utf-8'))   # write to file
                    date_file.close()

            xml.close()
            print("FILE {} FINISHED PARSING IN {} SECONDS: ".format(file, time.time() - start_time))
            print("FOUND A TOTAL OF {} UNIQUE DATES".format(date_tag_count))
# end of class SpeechParser


print("Running: ", sys.argv[0])
if len(sys.argv) == 1:
    print("No root directory provided. Please Provide directory as argument")
else:
    begin_time = time.time()
    if os.path.isdir(sys.argv[1]):
        print("Root Directory: ", sys.argv[1])
        parser = SpeechParser(sys.argv[1])
        parser.find_files()
        parser.parse_files()
        print("PARSE FINISHED. TOOK {} SECONDS".format(time.time() - begin_time))
    else:
        print("FIRST ARGUMENT MUST BE DIRECTORY")
