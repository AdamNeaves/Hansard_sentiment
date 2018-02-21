
from bs4 import BeautifulSoup as bs
import textwrap
import os
import sys


class SpeechParser:

    def parse_speeches(self, word_soup, date, file_name):
        new_soup = bs()
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

            date_tag   = new_soup.new_tag('date')    # create new tags for the soup to contain info
            topic_tag  = new_soup.new_tag('topic')   # we don't need tags for member cause we can
            stance_tag = new_soup.new_tag('stance')  # copy it from the original xml
            speech_tag = new_soup.new_tag('speech')

            new_soup.append(speech_tag)
            speech_soup = new_soup.contents[len(new_soup.contents)-1]
            speech_soup.append(date_tag)
            speech_soup.date.append(date.get('format'))

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

    def print_speeches(self, word_soup, date):
        # for now, print each members name, then their speech, just to test
        for tag in word_soup.find_all('membercontribution'):
            parent = tag.parent
            member = parent.find('member')
            subject = parent.parent.title
            for image in tag.find_all('image'):
                image.decompose()
            for col in tag.find_all('col'):
                col.decompose()
            print("DATE:    {}".format(date.get('format')))
            print("SUBJECT: {}".format(subject.text))
            print("MEMBER:  {}".format(member.text))
            print("SPEECH:  ")
            for line in textwrap.wrap(tag.text, 140):
                print(line)
            input("MORE...\n")
        return

    def __init__(self, root_dir):
        self.dir = root_dir
        parsed_dir = os.path.dirname(self.dir)
        base_name  = os.path.basename(self.dir)
        parsed_dir = os.path.join(os.path.dirname(parsed_dir), "Parsed Speech")
        print("PARSED DIRECTORY: ", parsed_dir)
        self.dest = open(os.path.join(parsed_dir, '{}_parsed.xml'.format(base_name)), 'wb')

        self.files = []

    def find_files(self):
        for root, dirs, files in os.walk(self.dir):
            for file in files:
                if file.endswith('.xml'):
                    print("adding {} to list".format(file))
                    self.files.append(file)
        print("FILES: ", self.files)

    def parse_files(self):
        soup = bs(features='xml')
        series_tag = soup.new_tag('series')
        soup.append(series_tag)
        print("PRE-FIND SERIES\n", soup.prettify())
        parsed_soup = soup.find('series')
        print("FIND SERIES\n", parsed_soup.prettify())

        for file in self.files:
            file_tag = soup.new_tag('file', id=file)
            parsed_soup.append(file_tag)
        print(parsed_soup.prettify())

        for file in self.files:
            print("NEW FILE: ", file)
            xml = open(os.path.join(self.dir, file), 'r')  # open XML file
            origin_soup = bs(xml, 'xml')  # open XML file as soup

            for date in origin_soup.find_all('date'):
                # print("    NEW DATE: ", date.text)
                if "written" not in date.parent.title.text.lower():  # checking for written questions, we dont want them
                    target_soup = date.parent
                    gen_soup = self.parse_speeches(target_soup, date, file)
                    # print(gen_soup.prettify())
                    parsed_soup.find(attrs={'id': file}).append(gen_soup)
                #    print(parsed_soup.prettify())
            xml.close()
            print(parsed_soup.prettify())

        self.dest.write(soup.prettify(encoding='utf-8'))
# end of class SpeechParser


print("Running: ", sys.argv[0])
if len(sys.argv) == 1:
    print("No root directory provided. Please Provide directory as argument")
else:
    if os.path.isdir(sys.argv[1]):
        print("Root Directory: ", sys.argv[1])
        parser = SpeechParser(sys.argv[1])
        parser.find_files()
        parser.parse_files()
    else:
        print("FIRST ARGUMENT MUST BE DIRECTORY")
