import unittest
import mooby


class BrainTestCase(unittest.TestCase):

    def setUp(self):
        self.brain = mooby.Brain()

    def test_to_dict1(self):
        self.brain.learn_phrase('I am Sam.')
        result = self.brain.to_dict()
        expected = {
            'order': 1,
            'graph': {
                None: [('I',)],
                ('I',): [('am',)],
                ('am',): [('Sam.',)],
                ('Sam.',): [None],
            },
        }
        self.assertEqual(expected, result)

    def test_from_dict1(self):
        d = {
            'order': 1,
            'graph': {},
        }
        result = mooby.Brain.from_dict(d)
        self.assertEqual(1, result.order)

    def test_from_dict2(self):
        d = {
            'order': 1,
            'graph': {},
            'graphx': {},
        }
        with self.assertRaises(ValueError):
            mooby.Brain.from_dict(d)

    def test_from_dict3(self):
        d = {
            'order': 1,
        }
        with self.assertRaises(KeyError):
            mooby.Brain.from_dict(d)
