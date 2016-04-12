from . import tokenize, phrasify
import random


class Brain(object):

    def __init__(self, order=1):
        self.order = order
        self._graph = {}
        self._rng = random.Random()

    def learn_phrase(self, phrase):
        tokens = tokenize(phrase)
        if not tokens:
            return
        i = 0
        t0 = None
        while i < len(tokens):
            t1 = tuple(tokens[i:i+self.order])
            self._associate(t0, t1)
            t0 = t1
            i += self.order
        self._associate(t1, None)

    def learn(self, corpus):
        for phrase in phrasify(corpus):
            self.learn_phrase(phrase)

    def utter(self):
        if not self._graph:
            return None
        utterance = []
        tokens = self._next(None)
        while tokens is not None:
            utterance.extend(tokens)
            tokens = self._next(tokens)
        return utterance

    def speak(self):
        utterance = self.utter()
        return ' '.join(utterance)

    def _next(self, token):
        t = self._graph[token]
        if t is None:
            return t
        return self._rng.choice(t)

    def _associate(self, t1, t2):
        bag = self._graph.setdefault(t1, [])
        bag.append(t2)
