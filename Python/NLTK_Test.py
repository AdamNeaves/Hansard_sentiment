import NLP
import os
from bs4 import BeautifulSoup as bs

name = "Mr. Geoffrey Robinson (Coventry, North-West)"
other_name = "Mr. Geoffrey Robinson"
paragraph = """
 As the right hon. Gentleman knows, consumer protection is a matter for my right hon. Friend the Secretary of State for 
 Trade and Industry. The right hon. Gentleman will have noticed that the Bank of England recently issued a letter to all
 lending institutions urging them to observe prudent lending measures in their lending. My hon. Friend the Minister for 
 Housing, Urban Affairs and Construction has echoed that point to the building societies in respect of lending for 
 housing. It is important that these institutions observe prudent lending policies. I believe that, coupled with 
 prudence by those who borrow, that is the best way to deal with the matter.
    """
print("NAME FROM NLP: ", NLP.extract_name(name))
print("OTHER NAME   : ", NLP.extract_name(other_name))

sentences = NLP.sentence_split(paragraph)
i = 1
for sent in sentences:
    print(i, ": ", sent)
    i += 1

# name_one = input("Enter Name One:")
# name_two = input("Enter Name Two:")
# print(name_one, " and ", name_two , " same person?: ", NLP.name_match(name_one, name_two))

input("Waiting for input to start name list...")

root_dir = "E:\Documents\-Uni Documents\Year 3\Final Project\Data\Parsed Speech\Test_Set"
file = "Name_match_test.xml"

xml = open(os.path.join(root_dir, file))
soup = bs(xml, 'xml')

members = soup.find_all('member')
member_names = []
for member in members:
    original_name = member.get('membername')
    name = NLP.extract_name(original_name)
    print("Original Name: {}".format(original_name))
    print("Found Name:    {}".format(name))
    previous_seen = False
    for mem_name in member_names:
        if NLP.name_match(name, mem_name):
            print("NAME MATCH: {} IS {}".format(name, mem_name))
            previous_seen = True
            break
    if not previous_seen:
        member_names.append(name)
    print(" ")

