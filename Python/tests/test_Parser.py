import unittest
import Speech_Parser_BS
import os
from lxml.doctestcompare import LXMLOutputChecker
import lxml
from doctest import Example


class SpeechParserTest(unittest.TestCase):

    def setUp(self):
        self.Parser = Speech_Parser_BS.SpeechParser("./Test Data/Source Data/Test File")
        self.Parser.find_files()

    def tearDown(self):
        directory = ".\Test Data\Parsed Speech\Test File"
        for file in os.listdir(directory):
            os.remove(os.path.join(directory,file))
        os.rmdir(directory)

    def test_parser_find_files(self):
        expected_array = ["test_file.xml"]
        self.assertEqual(expected_array, self.Parser.files)

    @unittest.skip("Unable to find way to compare XML trees")
    def test_parser_parse_files(self):

        self.Parser.parse_files()
        self.assertEqual()


