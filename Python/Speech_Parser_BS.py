
from bs4 import BeautifulSoup as bs
import textwrap
import os

rootdir = 'E:\Documents\-Uni Documents\Year 3\Final Project\Hansard Dataset\S5'


def print_speeches(word_soup, date):
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


for root, dirs, files in os.walk(rootdir):
    for file in files:
        print("Reading {}".format(file))
        xml = open(os.path.join(root, file), 'r')
        soup = bs(xml, "xml")
        # we only want to see the oral questions. written ones will be too hard to get sentiment from
        # however, the oral questions tag does not exist in all the data
        for date in soup.find_all('date'):

            if "written" not in date.parent.title.text.lower():
                soup = date.parent
                print_speeches(soup, date)
            else:
                print("WRITTEN QUESTIONS. NOT APPLICABLE TO SENTIMENT")




