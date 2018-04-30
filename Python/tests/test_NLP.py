
import unittest
import NLP


class NLPSentenceSplitTestCase(unittest.TestCase):
    """Tests for the NLP Module's Sentence Splitter Function"""
    def setUp(self):
        self.longMessage = True
        pass  # nothing to set up

    def tearDown(self):
        pass  # nothing to tear down

    def test_sentence_split_single_sentence(self):
        test_string = "This test string only has one sentence, and so should not be split"
        expected_result = ["This test string only has one sentence, and so should not be split"]
        self.assertEqual(NLP.sentence_split(test_string), expected_result)

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

    def test_sentence_split_percent(self):
        test_string = "This is a test of correcting errors. The word per cent. should be replaced and not split on"
        expected_result = ["This is a test of correcting errors.",
                           "The word percent should be replaced and not split on"]
        self.assertEqual(NLP.sentence_split(test_string), expected_result)

    def test_sentence_split_contains_quote(self):
        test_string = 'This test contains a "quote" inside it. This should not cause it to split'
        expected_result = ['This test contains a "quote" inside it.',
                           'This should not cause it to split']
        self.assertEqual(NLP.sentence_split(test_string), expected_result)


class NLPNameExtractTestCase(unittest.TestCase):
    """Tests for the NLP Module's Name Extractor Function"""
    # NAME EXTRACTOR TESTS##############################################################################################
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_extract_name_mr(self):
        test_string = "The Name that should be discovered is Mr. John Brown"
        expected_result = "Mr. John Brown"
        self.assertEqual(NLP.extract_name(test_string), expected_result)

        test_string = "The Name that should be discovered is Mr John Brown"
        expected_result = "Mr John Brown"
        self.assertEqual(NLP.extract_name(test_string), expected_result)

    def test_extract_name_mrs(self):
        test_string = "The Name that should be discovered is Mrs. Jane Brown"
        expected_result = "Mrs. Jane Brown"
        self.assertEqual(NLP.extract_name(test_string), expected_result)

        test_string = "The Name that should be discovered is Mrs Jane Brown"
        expected_result = "Mrs Jane Brown"
        self.assertEqual(NLP.extract_name(test_string), expected_result)
        
    def test_extract_name_dr(self):
        test_string = "The Name that should be discovered is Dr. Jane Brown"
        expected_result = "Dr. Jane Brown"
        self.assertEqual(NLP.extract_name(test_string), expected_result)

        test_string = "The Name that should be discovered is Dr Jane Brown"
        expected_result = "Dr Jane Brown"
        self.assertEqual(NLP.extract_name(test_string), expected_result)

    def test_extract_name_sir(self):
        test_string = "The Name that should be discovered is Sir. John Brown"
        expected_result = "Sir. John Brown"
        self.assertEqual(NLP.extract_name(test_string), expected_result)

        test_string = "The Name that should be discovered is Sir John Brown"
        expected_result = "Sir John Brown"
        self.assertEqual(NLP.extract_name(test_string), expected_result)

    def test_extract_name_no_honorific(self):
        test_string = "There is no Honorific in this sentence, so it should all be returned."

        self.assertEqual(NLP.extract_name(test_string), test_string)

    def test_extract_name_only_name(self):
        test_string = "Mr. Thomas Ridgewell"

        self.assertEqual(NLP.extract_name(test_string), test_string)


class NLPNameMatchTestCase(unittest.TestCase):
    """Tests for the NLP Module's Name Matching Function"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_name_match_same(self):
        test_name_one = "Mr Thomas Ridgewell"
        self.assertTrue(NLP.name_match(test_name_one, test_name_one))

    def test_name_match_diff_format_1(self):
        test_name_one = "Mr. Thomas Ridgewell"
        test_name_two = "Mr. Ridgewell"
        self.assertTrue(NLP.name_match(test_name_one, test_name_two))

    def test_name_match_diff_format_2(self):
        test_name_one = "Mr. Thomas Ridgewell"
        test_name_two = "Mr. T. Ridgewell"
        self.assertTrue(NLP.name_match(test_name_one, test_name_two))

    def test_name_match_diff_format_3(self):
        test_name_one = "Mr. Thomas Ridgewell"
        test_name_two = "Mr. Ridgewell"
        self.assertTrue(NLP.name_match(test_name_one, test_name_two))

    def test_name_match_diff_names_1(self):
        test_name_one = "Mr. Thomas Ridgewell"
        test_name_two = "Sir Jones Smith"
        self.assertFalse(NLP.name_match(test_name_one, test_name_two))

    def test_name_match_diff_names_2(self):
        test_name_one = "Mr. Thomas Ridgewell"
        test_name_two = "Mr. Elliot Ridgewell"
        self.assertFalse(NLP.name_match(test_name_one, test_name_two))

    def test_name_match_diff_names_3(self):
        test_name_one = "Mr Thomas Ridgewell"
        test_name_two = "Mrs Ridgewell"
        self.assertFalse(NLP.name_match(test_name_one, test_name_two))


class NLPSentenceFeatureSetConverterTestCase(unittest.TestCase):

    def setUp(self):
        # we need to create the "all_words" thing specifically for this set of tests
        pass

    def tearDown(self):
        pass

    # def test_convert_sentence_feature(self):
    #     test_sentence = "This is a test of the sentence to feature converter"
    #     expected_result = ["This", "is", "a", "test", "of", "the", "sentence", "to", "feature", "converter"]
    #     self.assertEqual(NLP.convert_sentence_to_features(test_sentence), expected_result)


if __name__ == '__main__':
    # unittest.main runs all tests cases in alphabetical order. So thats nice
    unittest.main(verbosity=2)  # verbosity of 2 gives readout of tests that run and in what order
