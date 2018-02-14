
from bs4 import BeautifulSoup as bs
import textwrap

file = open("E:\Documents\-Uni Documents\Year 3\Final Project\Hansard Dataset\S6\S6CV0001P0.xml")

soup = bs(file, "xml")

# we only want to see the oral questions. written ones will be too hard to get sentiment from
soup = soup.find('oralquestions')
# for now, print each members name, then their speech, just to test
for tag in soup.find_all('membercontribution'):
    parent = tag.parent
    member = parent.find('member')
    print("MEMBER: {}".format(member.text))
    print("SPEECH:")
    for line in textwrap.wrap(tag.text, 140):
        print(line)
    input("MORE...\n")
