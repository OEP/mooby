import unittest
import mooby


class LexTestCase(unittest.TestCase):

    def test_tokenize1(self):
        result = mooby.tokenize('Hello, world!')
        expected = ['Hello,', 'world!']
        self.assertEqual(expected, result)

    def test_phrasify1(self):
        result = mooby.phrasify('I am Sam. Sam I am.')
        expected = [
            'I am Sam.',
            'Sam I am.',
        ]
        self.assertEqual(expected, result)
