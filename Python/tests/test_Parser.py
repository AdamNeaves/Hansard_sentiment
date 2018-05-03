import unittest
import Speech_Parser_BS


class SpeechParserTest(unittest.TestCase):

    def setUp(self):
        self.Parser = Speech_Parser_BS.SpeechParser("./Test Data/Source Data/Test File")

    def tearDown(self):
        pass


