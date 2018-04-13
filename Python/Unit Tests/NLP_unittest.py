import unittest
import NLP


class NlpTestCase(unittest.TestCase):

    def setUp(self):
        pass  # nothing to set up

    def test_sentence_split_normal(self):
        test_string = "This is a test. These sentences should be split properly."
        expected_result = ["This is a test.",
                           "These sentences should be split properly."]
        self.assertEqual(NLP.sentence_split(test_string), expected_result)

    def test_sentence_split_hon(self):
        test_string = "This is a Test of the effects of the word Hon. Gentleman. This is a special case."
        expected_result = ["This is a Test of the effects of the word honorable Gentleman.",
                           "This is a special case."]
        self.assertEqual(NLP.sentence_split(test_string), expected_result)

    def test_sentence_split_missing_space(self):
        test_string = "This is a test of correcting errors.There is no space between sentences but it should still work"
        expected_result = ["This is a test of correcting errors.",
                           "There is no space between sentences but it should still work"]
        self.assertEqual(NLP.sentence_split(test_string), expected_result)


if __name__ == '__main__':
    unittest.main(verbosity=2)  # verbosity of 2 gives readout of tests that run and in what order
